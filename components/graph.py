from dash import dcc

from statics import get_one_day

bar_chart, _, msg, df = get_one_day()
dataCnt = msg.split(' ')[0]

graph = dcc.Graph(
    figure=bar_chart,
    id='graph', clickData=None, hoverData=None,
    config={
        'staticPlot': False,     # True, False
        'scrollZoom': True,      # True, False
        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
        'showTips': True,       # True, False
        'displayModeBar': True,  # True, False, 'hover'
        'watermark': True,
        'modeBarButtonsToRemove': ['pan2d','select2d'],
    },
    style={'border':'1px black solid', 'zIndex':1, "frameMargins": 55,},
)