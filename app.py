import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

# Create the Dash app and add a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Aktuelle Belegung der Virtual Maschine", style={'font-size': '24px'}),
    dcc.RadioItems(
        id='name-radioitems',
        options=[
            {'label': 'Keine Auswahl', 'value': 'None'},
            {'label': 'Andreas Noel', 'value': 'Name1'},
            {'label': 'Simon Mailhammer', 'value': 'Name2'},
            {'label': 'Maximilian Müller', 'value': 'Name3'},
            {'label': 'Simon Hofmann', 'value': 'Name4'},
            {'label': 'Anderer Benutzer', 'value': 'Name5'}
        ],
        value='None'  # Default value
    ),
    html.H3("Wählen Sie die Zeitspanne (.5 bis 6 Stunden):", style={'font-size': '20px'}),
    dcc.Slider(
        id='time-slider',
        min=.5,
        max=6,
        step=0.1,
        value=2,  # Start value in hours
        marks={i: f'{i}h' for i in range(1, 7)}
    ),
    html.H3("Verstrichene Zeit seit Auswahl:", style={'font-size': '20px'}),
    html.Div(id='timer-display'),
    dbc.Progress(id='progress-bar', value=0, max=100, striped=True, animated=True, style={"height": "30px", 'width':'1000px', 'marginLeft': '20px'}),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1 second in milliseconds
        n_intervals=0
    ),
    html.Div(id='status-message', style={'font-size': '20px', 'marginTop': '20px'})
])

# Global variable to store the start time
start_time = None
time_limit = timedelta(hours=2)

# Callback function to update the timer display, progress bar, and status message
@app.callback(
    [Output('timer-display', 'children'),
     Output('progress-bar', 'value'),
     Output('status-message', 'children'),
     Output('status-message', 'style')],
    [Input('interval-component', 'n_intervals')],
    [State('name-radioitems', 'value'),
     State('time-slider', 'value')]
)
def update_timer(n_intervals, selected_name, slider_value):
    global start_time

    # Calculate the time span based on the slider value
    global time_limit
    time_limit = timedelta(hours=slider_value)

    if n_intervals == 0 or start_time is None:
        return "00:00:00", 0, "Virtual Maschine Frei", {'color': 'green'}

    # Calculate the elapsed time
    elapsed_time = datetime.now() - start_time
    elapsed_str = str(elapsed_time).split('.')[0]  # Format the time

    # Calculate the progress percentage
    progress_percentage = min((elapsed_time / time_limit) * 100, 100)

    # Check if the timer has expired or no name is selected
    if elapsed_time >= time_limit or selected_name == 'None':
        return elapsed_str, progress_percentage, "Virtual Maschine Frei", {'color': 'green'}

    # If a name is selected and the timer is running
    if selected_name and selected_name != 'None':
        return elapsed_str, progress_percentage, "Virtual Maschine belegt", {'color': 'red'}

    # Default case
    return elapsed_str, progress_percentage, "Virtual Maschine Frei", {'color': 'green'}

# Callback function to reset the interval when a new name is selected
@app.callback(
    Output('interval-component', 'n_intervals'),
    [Input('name-radioitems', 'value')]
)
def start_timer(selected_name):
    global start_time
    if selected_name != 'None':
        start_time = datetime.now()  # Set the start time
    return 0  # Reset the interval component

# Start the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
