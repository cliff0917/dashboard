from dash import dcc

from statics import get_one_day, get_area

bar_chart, _, msg, df = get_one_day()
dataCnt = msg.split(' ')[0]

area_chart = get_area('rule.level')

CONFIG={
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': True,
    'modeBarButtonsToRemove': ['pan2d','select2d'],
}

STYLE={'border':'1px black solid', 'zIndex':1}
STYLE2={'border':'1px black solid', 'zIndex':1, 'width':800, 'height':400}

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 23,
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '40%',
    'zIndex':1,
}

graph = dcc.Graph(
    figure=bar_chart,
    id='graph', clickData=None, hoverData=None,
    config=CONFIG, style=STYLE,
)

area_graph = dcc.Graph(
    figure=area_chart,
    id='area_chart', clickData=None, hoverData=None,
    config=CONFIG, style=DISPLAY_STYLE,
)