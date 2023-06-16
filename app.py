import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State

import assets.config as config
from collector import Collector
from analyzer import Analyzer


# App Instance
app = dash.Dash(name=config.APP_NAME, external_stylesheets=[dbc.themes.LUX])
app.title = config.APP_NAME


select_queues = [
    {'label': 'Screencast', 'value': 'screencast_queue'},
    {'label': 'Webcam', 'value': 'webcam_queue'}
]

value_to_label = {
    'screencast_queue': 'Screencast',
    'webcam_queue': 'Webcam'
}

graph_queues = [
    {'label': 'All', 'value': 'all'}
]


# App body
# IDs:
#   n-graph, times-to-run,
#   n-queues, run, plot

body = dbc.Col(children=[
    # input
    dbc.Row(children=[
        dbc.Col(dbc.Row(dbc.Button("Run", id="run", color="primary")), width=2, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Testing queues", html_for="n-queues", style={"width": "30%"}),
            dcc.Dropdown(id='n-queues', className='dash-bootstrap', options=select_queues, multi=True, clearable=False,
                         style={"flex-grow": "1"}),
        ], style={'display': 'flex', 'align-items': 'center'}), width=3, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Times to run", html_for="times-to-run", style={"width": "50%"}),
            dbc.Input(id="times-to-run", type="number", min=0, max=10, step=1, value=1, style={"width": "50%"}),
        ], style={'display': 'flex', 'align-items': 'center'}), width=2, style={"margin-right": "50px"}),

        dbc.Col(html.Div(children=[
            dbc.Label("Graph output", html_for="n-graph", style={"width": "50%"}),
            dbc.Select(id="n-graph", options=graph_queues, value=graph_queues[0], style={"flex-grow": "1"})
        ], style={'display': 'flex', 'align-items': 'center'}), width=2, style={"margin-right": "50px"})
    ], style={"margin": "0 0 30px 0"}),

    # output
    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Textarea(id="text-area", style={"height": "100%", "width": "100%", "resize": "none"}, readOnly=True)
        ], width=3),
        dbc.Col(children=[
            dbc.Spinner(dcc.Graph(id="plot"), color="primary", type="grow")
        ], width=9)
    ])
])


@app.callback(Output("n-graph", "options"), Input("n-queues", "value"))
def update_graph_queue_list(queues):
    result = [{'label': 'All', 'value': 'all'}]
    for i in queues:
        result.append({'label': value_to_label[i], 'value': i})
    return result


@app.callback(Output("text-area", "value"), Output("plot", "figure"),
              Input("run", "n_clicks"),
              State("n-queues", "value"), State("times-to-run", "value"))
def execute(n_clicks, queues, times_to_run):
    if queues is not None:
        try:
            collector = Collector()
            collector.setup(config.TEST_PATH, queues, times_to_run)
            analyzer = Analyzer(config.TEST_PATH, queues)
            results = analyzer.run(collector.run())
            print(results)
        except Exception as e:
            print('Exception: ', e)


# App main layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1(config.APP_NAME, id="nav-pills", style={"margin": "10px 0 30px 0"}),
    body
])


if __name__ == "__main__":
    app.run_server(debug=True, host=config.APP_HOST, port=config.APP_PORT)
