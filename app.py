import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import assets.config as config
from collector import Collector
from analyzer import Analyzer


# App Instance
app = dash.Dash(name=config.APP_NAME, external_stylesheets=[dbc.themes.LUX])
app.title = config.APP_NAME


select_queues = [
    dbc.DropdownMenuItem('Screencast'),
    dbc.DropdownMenuItem('Webcam')
]

graph_queues = [
    dbc.DropdownMenuItem('All'),
    dbc.DropdownMenuItem('Screencast'),
    dbc.DropdownMenuItem('Webcam')
]


# App body
# IDs:
#   n-queues, times-to-run,   run,
#   n-graph,  download-excel, plot,
#   title

body = dbc.Col(children=[
    # input
    dbc.Row(children=[
        dbc.Col(dbc.Row(dbc.Button("Run", id="run", color="primary")), width=2, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Testing queues", html_for="n-queues", style={"width": "50%"}),
            dbc.Row(dbc.DropdownMenu(id="n-queues", label="Queues", children=select_queues), style={"width": "50%"})
        ], style={'display': 'flex', 'align-items': 'center'}), width=2, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Times to run", html_for="times-to-run", style={"width": "50%"}),
            dbc.Input(id="times-to-run", placeholder="times to run", type="number", value="1", style={"width": "50%"}),
        ], style={'display': 'flex', 'align-items': 'center'}), width=2, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Graph output", html_for="n-graph", style={"width": "50%"}),
            dbc.DropdownMenu(id="n-graph", label=graph_queues[0].children, children=graph_queues,
                             style={"width": "50%"})
        ], style={'display': 'flex', 'align-items': 'center'}), width=2, style={"margin-right": "50px"})
    ], style={"margin": "0 0 30px 0"}),

    # output
    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Textarea(style={"height": "100%", "width": "100%", "resize": "none"}, readOnly=True)
        ], width=3),
        dbc.Col(children=[
            dbc.Spinner([
                # title
                html.H6(id="title"),
                # download
                dbc.Badge(html.A('Download', id='download-excel', download="tables.xlsx", href="", target="_blank"),
                          color="success", pill=True),
                # plot
                dcc.Graph(id="plot")
            ], color="primary", type="grow")
        ], width=9)
    ])
])


@app.callback(output=[dash.Output(component_id="title", component_property="children"),
                      dash.Output(component_id="plot", component_property="figure"),
                      dash.Output(component_id="download-excel", component_property="href")],
              inputs=[dash.Input(component_id="run", component_property="n_clicks")],
              state=[dash.State("n_queues", "value"), dash.State("n_graph", "value"),
                     dash.State("times_to_run", "value")])
def execute(n_clicks, n_queues, n_graph, times_to_run):
    try:
        print(n_clicks, n_graph)  # ToDo: Checkout
        analyzer = Analyzer(config.TEST_PATH)
        collector = Collector()
        collector.setup(config.TEST_PATH, n_queues, times_to_run)
        results = analyzer.run(collector.run(), 'temp')
        return results
    except Exception as e:
        print(e)


# App main layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1(config.APP_NAME, id="nav-pills", style={"margin": "10px 0 30px 0"}),
    body
])


if __name__ == "__main__":
    app.run_server(debug=True, host=config.APP_HOST, port=config.APP_PORT)
