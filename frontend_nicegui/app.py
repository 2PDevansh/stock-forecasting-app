from nicegui import ui, run
import requests

API_BASE = 'http://127.0.0.1:5000'

COMPANY_OPTIONS = {
    "India": ["TCS", "Reliance", "Adani", "HDFC"],
    "Japan": ["Toyota", "Honda", "Sony", "Nintendo"],
    "China": ["Alibaba", "Xiaomi", "JD.com Inc", "Tencent"],
}

state = {
    'country': None,
    'company': None,
    'days': 5,
    'prediction': None,
    'grsi': None,
    'loading_grsi': False,
}

# ---------------- HELPERS ----------------
def risk_color(v):
    if v < 30:
        return '#145a32'
    if v < 70:
        return '#9c640c'
    return '#7b241c'


def risk_text(v):
    if v < 30:
        return 'Low geopolitical risk'
    if v < 100:
        return 'Moderate geopolitical risk'
    return 'High geopolitical risk'


# ---------------- API ----------------
async def predict_price():
    if not state['company']:
        ui.notify('Select a company first', color='negative')
        return

    try:
        res = await run.io_bound(
            requests.post,
            f'{API_BASE}/predict',
            json={'company': state['company'], 'days': state['days']},
            timeout=30,
        )
        res.raise_for_status()
        state['prediction'] = res.json()
    except Exception as e:
        ui.notify(f'Prediction failed: {e}', color='negative')

    content.refresh()


async def fetch_grsi():
    if not state['company']:
        ui.notify('Select a company first', color='negative')
        return

    state['loading_grsi'] = True
    content.refresh()

    try:
        res = await run.io_bound(
            requests.get,
            f'{API_BASE}/grsi',
            params={'company': state['company']},
            timeout=20,
        )
        res.raise_for_status()
        state['grsi'] = res.json()
    except Exception as e:
        ui.notify(f'GRSI error: {e}', color='negative')
        state['grsi'] = None
    finally:
        state['loading_grsi'] = False

    content.refresh()


# ---------------- UI ----------------
@ui.refreshable
def content():
    ui.add_css("""
    body {
        font-family: "Times New Roman", Times, serif;
        background: linear-gradient(135deg, #fdfcfb, #e2d1c3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.94);
        border-radius: 18px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.15);
    }

    .action-btn {
        letter-spacing: 0.4px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    }
    """)

    with ui.column().classes('items-center p-12 w-full'):
        ui.label('Stock Forecast & GeoRisk Dashboard') \
            .classes('text-4xl font-bold text-gray-900 mb-8')

        # ---------- INPUT CARD ----------
        with ui.card().classes(
            'glass-card w-full max-w-3xl p-8'
        ):
            ui.select(
                list(COMPANY_OPTIONS),
                label='Country',
                value=state['country'],
                on_change=lambda e: set_country(e.value),
            ).classes('w-full mb-4')

            if state['country']:
                ui.select(
                    COMPANY_OPTIONS[state['country']],
                    label='Company',
                    value=state['company'],
                    on_change=lambda e: set_company(e.value),
                ).classes('w-full mb-4')

            ui.number(
                label='Days to Forecast',
                min=1,
                max=100,
                value=state['days'],
                on_change=lambda e: set_days(e.value),
            ).classes('w-44 mb-6')

            with ui.row().classes('gap-5'):
                ui.button(
                    'Predict Price',
                    on_click=predict_price,
                ).classes(
                    'action-btn bg-[#1f3a5f] text-white px-8 py-3 rounded-xl font-semibold'
                )

                bg_color = '#7b241c'
                if state['grsi']:
                    bg_color = risk_color(state['grsi']['GRSI'])

                with ui.button(on_click=fetch_grsi) \
                    .style(f'background:{bg_color}') \
                    .classes(
                        'action-btn text-white px-8 py-3 rounded-xl min-w-[320px]'
                    ):

                    if state['loading_grsi']:
                        ui.label('Loading GeoRisk Index...').classes('font-semibold')

                    elif not state['grsi']:
                        ui.label('Show GeoRisk Index').classes('font-semibold')

                    else:
                        g = state['grsi']
                        with ui.column().classes('items-start'):
                            ui.label(
                                f"GeoRisk Index — {g['company']}"
                            ).classes('font-semibold')

                            ui.label(
                                f"{g['GRSI']:.2f}"
                            ).classes('text-3xl font-bold')

                            ui.label(
                                risk_text(g['GRSI'])
                            ).classes('text-xs opacity-90 mt-1')

        # ---------- RESULTS ----------
        if state['prediction']:
            p = state['prediction']
            with ui.card().classes(
                'glass-card mt-10 w-full max-w-4xl p-8'
            ):
                ui.label(f"Prediction Results — {p['company']}") \
                    .classes('text-2xl font-semibold mb-3')

                ui.label(f"Low Likely Price: {p['low_likely']:.2f}")
                ui.label(f"High Likely Price: {p['high_likely']:.2f}")

                if p.get('plot_url'):
                    ui.label('Actual vs Predicted Prices') \
                        .classes('mt-5 font-semibold')
                    ui.image(p['plot_url']) \
                        .classes('rounded-xl shadow-lg mt-3')

                ui.echart({
                    'xAxis': {
                        'type': 'category',
                        'data': [f'Day {i+1}' for i in range(len(p['forecast']))],
                    },
                    'yAxis': {'type': 'value'},
                    'series': [{
                        'data': p['forecast'],
                        'type': 'line',
                        'smooth': True,
                        'areaStyle': {},
                    }],
                }).classes('h-80 mt-5')


# ---------------- STATE ----------------
def set_country(v):
    state['country'] = v
    state['company'] = None
    state['grsi'] = None
    state['prediction'] = None
    content.refresh()


def set_company(v):
    state['company'] = v
    state['grsi'] = None
    content.refresh()


def set_days(v):
    state['days'] = int(v)
    content.refresh()


content()
ui.run()
