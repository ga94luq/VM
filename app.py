import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

# Erstellen Sie die Dash-App und fügen Sie ein Bootstrap-Theme hinzu
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout der Dash-App
app.layout = html.Div([
    html.H1("Timer für Namen"),
    dcc.RadioItems(
        id='name-radioitems',
        options=[
            {'label': 'Name 1', 'value': 'Name1'},
            {'label': 'Name 2', 'value': 'Name2'},
            {'label': 'Name 3', 'value': 'Name3'},
            {'label': 'Name 4', 'value': 'Name4'},
            {'label': 'Name 5', 'value': 'Name5'}
        ],
        value='Name1'  # Standardwert
    ),
    html.H3("Verstrichene Zeit seit Auswahl (Ablauf von 2h):"),
    html.Div(id='timer-display'),
    dbc.Progress(id='progress-bar', value=0, max=100, striped=True, animated=True, style={"height": "30px"}),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1 Sekunde in Millisekunden
        n_intervals=0
    )
])

# Globale Variable zum Speichern der Startzeit
start_time = None
two_hours = timedelta(hours=2)

# Callback-Funktion zum Starten des Timers bei Änderung des Namens
@app.callback(
    [Output('timer-display', 'children'),
     Output('progress-bar', 'value')],
    [Input('interval-component', 'n_intervals')],
    [State('name-radioitems', 'value')]
)
def update_timer(n_intervals, selected_name):
    global start_time

    if n_intervals == 0 or start_time is None:
        return "00:00:00", 0

    # Berechnung der verstrichenen Zeit
    elapsed_time = datetime.now() - start_time
    elapsed_str = str(elapsed_time).split('.')[0]  # Formatieren der Zeit

    # Berechnung des Fortschritts
    progress_percentage = min((elapsed_time / two_hours) * 100, 100)

    return elapsed_str, progress_percentage

@app.callback(
    Output('interval-component', 'n_intervals'),
    [Input('name-radioitems', 'value')]
)
def start_timer(selected_name):
    global start_time
    start_time = datetime.now()  # Startzeit setzen
    return 0  # Reset the interval component

# Starten Sie die Dash-App
if __name__ == '__main__':
    app.run_server(debug=True)
