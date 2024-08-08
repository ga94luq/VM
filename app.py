import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Timer für Namen"),
    dcc.RadioItems(
        id='name-radioitems',
        options=[
            {'label': 'Andreas Noel', 'value': 'Name1'},
            {'label': 'Simon Mailhammer', 'value': 'Name2'},
            {'label': 'Maximilian Müller', 'value': 'Name3'},
            {'label': 'Simon Hofmann', 'value': 'Name4'},
            {'label': 'Anderer Benutzer', 'value': 'Name5'}
        ],
        value='Name1'  # Default value
    ),
    html.H3("Wählen Sie die Zeitspanne (.5 bis 6 Stunden):"),
    dcc.Slider(
        id='time-slider',
        min=.5,
        max=6,
        step=0.1,
        value=2,  # Start value in hours
        marks={i: f'{i}h' for i in range(1, 7)}
    ),
    html.H3("Verstrichene Zeit seit Auswahl:"),
    html.Div(id='timer-display'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1 second in milliseconds
        n_intervals=0
    )
])

# Global variable to store the start time
start_time = None
time_limit = timedelta(hours=2)

# Callback function to start the timer when the name is changed
@app.callback(
    Output('timer-display', 'children'),
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
        return "00:00:00"

    # Calculate the elapsed time
    elapsed_time = datetime.now() - start_time
    elapsed_str = str(elapsed_time).split('.')[0]  # Format the time

    return elapsed_str

@app.callback(
    Output('interval-component', 'n_intervals'),
    [Input('name-radioitems', 'value')]
)
def start_timer(selected_name):
    global start_time
    start_time = datetime.now()  # Set the start time
    return 0  # Reset the interval component

# Start the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
