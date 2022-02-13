import dash


from pages import page1, page2

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = page1.layout

if __name__ == '__main__':
    app.run_server(debug=True)
    """ pid = os.fork()
    if pid != 0:
        app.run_server()
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url) """