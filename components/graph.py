from dash import dcc

# from statics import get_init_bar
# from security_event_graph import get_init_area, get_init_pie

# bar_chart, _, msg, df = get_init_bar()
# dataCnt = msg.split(' ')[0]

# area_chart = get_init_area('rule.level')
# pie_chart = get_init_pie('rule.mitre.technique')

CONFIG={
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': True,
    'modeBarButtonsToRemove': ['pan2d','select2d'],
}

BAR_STYLE={'border':'1px black solid', 'zIndex':1}

AREA_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '50%',
    'zIndex':1,
}

PIE_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '46%',
    'zIndex':1,
}

graph = dcc.Graph(
    figure={},
    id='graph', clickData=None, hoverData=None,
    config=CONFIG, style=BAR_STYLE,
)

area_chart = dcc.Graph(
    figure={},
    id='area_chart', clickData=None, hoverData=None,
    config=CONFIG, style=AREA_STYLE,
)

pie_chart = dcc.Graph(
    figure={},
    id='pie_chart', clickData=None, hoverData=None,
    config=CONFIG, style=PIE_STYLE,
)

donut_chart = dcc.Graph(
    figure={},
    id='donut_chart', clickData=None, hoverData=None,
    config=CONFIG, style=PIE_STYLE,
)

se_bar_chart = dcc.Graph(
    figure={},
    id='se_bar_chart', clickData=None, hoverData=None,
    config=CONFIG, style=AREA_STYLE,
)