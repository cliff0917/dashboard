from dash import html
import feffery_antd_components as fac

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "50px",
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 0rem",
    "background-color": "#FFFFFF",
}

sidebar = html.Div(
        [
            fac.AntdSider(
                [
                    html.Div(
                        [
                            fac.AntdMenu(
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key':  '/Home',
                                            'title': 'Home',
                                            'icon': 'antd-home',
                                            'href': '/Home',
                                        },
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key':  '/Discover',
                                            'title': 'Discover',
                                            'icon': 'antd-global',
                                            'href': '/Discover',
                                        },
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key':  '/Security-Events',
                                            'title': 'Security-Events',
                                            'icon': 'antd-bar-chart',
                                            'href': '/Security-Events',
                                        },
                                    },
                                ],
                                mode='inline'
                            )
                        ],
                        style={
                            'height': '100%',
                            'overflowY': 'auto',
                        }
                    )
                ],
                collapsible=True,
                style={
                    'backgroundColor': 'rgb(240, 242, 245)'
                }
            ),
        ],
        id='sider-demo',
        style=SIDEBAR_STYLE
    )
