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

STYLE={'border':'1px black solid', 'zIndex':1, "frameMargins": 55}

graph = dcc.Graph(
    figure=bar_chart,
    id='graph', clickData=None, hoverData=None,
    config=CONFIG, style=STYLE,
)

area_graph = dcc.Graph(
    figure=area_chart,
    id='area_chart', clickData=None, hoverData=None,
    config=CONFIG, style=STYLE,
)