import os
import getpass
import subprocess
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import webbrowser
import threading

# Funktion zur Ermittlung der Remote-Benutzer
def get_remote_users():
    try:
        result = subprocess.run(['query', 'user'], capture_output=True, text=True, check=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Abrufen der Benutzer: {e}"

# Benutzername des aktuellen Benutzers abrufen
benutzername = os.getlogin()
benutzername_01 = getpass.getuser()

# Dash App erstellen
app = Dash(__name__)

# Startzeit speichern
start_time = datetime.now()

# Layout der Dash App
app.layout = html.Div([
    html.H1(id='local-user', style={'text-align': 'center', 'color': 'black', 'fontSize': '18px'}),
    html.H1(id='getpass-user', style={'text-align': 'center', 'color': 'black', 'fontSize': '18px'}),
    html.H1(id='remote-users', style={'text-align': 'center', 'color': 'black', 'fontSize': '18px'}),
    html.H1(id='time', style={'text-align': 'center', 'color': 'black', 'fontSize': '18px'}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # 30 Sekunden in Millisekunden
        n_intervals=0
    )
])

# Callback-Funktion für die Aktualisierung der Benutzerinformationen
@app.callback(
    [Output('local-user', 'children'),
     Output('getpass-user', 'children'),
     Output('remote-users', 'children'),
     Output('time', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_users(n_intervals):
    # Berechnung der verstrichenen Zeit seit dem Start
    elapsed_time = datetime.now() - start_time
    elapsed_seconds = int(elapsed_time.total_seconds())
    elapsed_str = str(timedelta(seconds=elapsed_seconds))
    
    # Aktualisierung der Benutzerinformationen
    remote_users = get_remote_users()
    return (
        f'Lokaler Benutzer: {benutzername}',
        f'Benutzer durch getpass: {benutzername_01}',
        f'Remote-Benutzer:\n{remote_users}',
        f'Laufzeit: {elapsed_str}'
    )

# Funktion zum Starten des Dash-Servers und Öffnen des Browsers
def run_server():
    app.run_server(debug=True, use_reloader=False)

# Die URL der Dash-Anwendung
def open_browser():
    import time
    time.sleep(1)  # Warten, bis der Server vollständig gestartet ist
    webbrowser.open("http://127.0.0.1:8050/")

if __name__ == '__main__':
    # Starte den Dash-Server in einem separaten Thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    # Öffne den Browser
    open_browser()
