from dash import dcc

from statics import get_statics
from components import collapse_item

df = collapse_item.df
bar_chart = get_statics(df)

graph = dcc.Graph(
    figure=bar_chart,
    id='graph', clickData=None, hoverData=None,
    config={
        'staticPlot': False,     # True, False
        'scrollZoom': True,      # True, False
        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
        'showTips': False,       # True, False
        'displayModeBar': True,  # True, False, 'hover'
        'watermark': True,
        'modeBarButtonsToRemove': ['pan2d','select2d'],
    },
    style={'border':'1px black solid', 'zIndex':5, "frameMargins": 55,},
)