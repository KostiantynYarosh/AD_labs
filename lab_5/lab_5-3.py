import dash
from dash import dcc, html, Input, Output
import numpy as np

INIT_AMPLITUDE = 1.0
INIT_FREQUENCY = 1.0
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_DISPERSION = 0.1
SHOW_NOISE = True
BASE_NOISE = np.random.normal(0, 1, 1000)

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_dispersion, show_noise=True):
    t = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(2 * np.pi * frequency * t + phase)

    if show_noise:
        scaled_noise = noise_mean + np.sqrt(noise_dispersion) * BASE_NOISE
        y += scaled_noise

    return t, y

def simple_moving_average_filter(signal, window_size):
    filtered_signal = np.convolve(signal, np.ones(window_size) / window_size, mode='valid')
    return np.concatenate((signal[:window_size-1], filtered_signal))

def exponential_filter(signal, alpha):
    filtered_signal = np.zeros_like(signal)
    filtered_signal[0] = signal[0]
    for i in range(1, len(signal)):
        filtered_signal[i] = alpha * signal[i] + (1 - alpha) * filtered_signal[i-1]
    return filtered_signal


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='original-signal-plot'),
    ], style={'width': '48%','height': '40%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='filtered-signal-plot'),
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Amplitude'),
        dcc.Slider(id='amp-slider', min=0.1, max=5.0, step=0.1, value=INIT_AMPLITUDE, marks={}, verticalHeight=0),
        html.Label('Frequency'),
        dcc.Slider(id='freq-slider', min=0.1, max=5.0, step=0.1, value=INIT_FREQUENCY, marks={}, verticalHeight=0),
        html.Label('Phase'),
        dcc.Slider(id='phase-slider', min=-np.pi, max=np.pi, step=0.2, value=INIT_PHASE, marks={}, verticalHeight=0),
        html.Label('Noise (Mean)'),
        dcc.Slider(id='noise-mean-slider', min=-1.0, max=1.0, step=0.1, value=INIT_NOISE_MEAN, marks={}, verticalHeight=0),
        html.Label('Noise (Dispersion)'),
        dcc.Slider(id='noise-disp-slider', min=0.0, max=1.0, step=0.1, value=INIT_NOISE_DISPERSION, marks={}, verticalHeight=0),
        dcc.Checklist(id='show-noise-check', options=[{'label': 'Show Noise', 'value': 'show'}], value=['show']),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Simple Moving Average', 'value': 'sma'},
                {'label': 'Exponential Filter', 'value': 'exponential'}
            ],
            value='sma'
        ),
        html.Label('Window Size'),
        dcc.Slider(id='window-size-slider', min=2, max=20, step=1, value=1),
        html.Label('Alpha'),
        dcc.Slider(id='alpha-slider', min=0, max=1.0, step=0.1, value=0.1),
        html.Button('Reset', id='reset-button', n_clicks=0, style={'margin-top': '20px', 'margin-right': '10px', 'padding': '15px 30px', 'font-size': '16px'}),
        html.Button('New Noise', id='new-noise-button', n_clicks=0, style={'margin-top': '20px', 'padding': '15px 30px', 'font-size': '16px'}),
    ], style={'margin': '30px'})
])

@app.callback(
    [
        Output('original-signal-plot', 'figure'),
        Output('filtered-signal-plot', 'figure'),
        Output('amp-slider', 'value'),
        Output('freq-slider', 'value'),
        Output('phase-slider', 'value'),
        Output('noise-mean-slider', 'value'),
        Output('noise-disp-slider', 'value'),
        Output('show-noise-check', 'value'),
        Output('filter-dropdown', 'value')
    ],
    [
        Input('amp-slider', 'value'),
        Input('freq-slider', 'value'),
        Input('phase-slider', 'value'),
        Input('noise-mean-slider', 'value'),
        Input('noise-disp-slider', 'value'),
        Input('show-noise-check', 'value'),
        Input('filter-dropdown', 'value'),
        Input('window-size-slider', 'value'),
        Input('alpha-slider', 'value'),
        Input('reset-button', 'n_clicks'),
        Input('new-noise-button', 'n_clicks')
    ]
)
def update_plots(amplitude, frequency, phase, noise_mean, noise_dispersion, show_noise, filter_type, window_size, alpha, reset_clicks, new_noise_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'reset-button':
        amplitude = INIT_AMPLITUDE
        frequency = INIT_FREQUENCY
        phase = INIT_PHASE
        noise_mean = INIT_NOISE_MEAN
        noise_dispersion = INIT_NOISE_DISPERSION
        show_noise = ['show']
        filter_type = 'sma'
        window_size = 10
        alpha = 0.1

    if button_id == 'new-noise-button':
        global BASE_NOISE, filtered_y
        BASE_NOISE = np.random.normal(0, 1, 1000)

    t, y = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_dispersion, 'show' in show_noise)
    if filter_type == 'sma':
        filtered_y = simple_moving_average_filter(y, window_size)
    elif filter_type == 'exponential':
        filtered_y = exponential_filter(y, alpha)

    original_signal_fig = {
        'data': [
            {'x': t, 'y': y, 'type': 'line', 'name': 'Original Signal', 'line': {'color': 'blue'}}
        ],
        'layout': {
            'xaxis': {'title': 'Time (s)'},
            'yaxis': {'title': 'Amplitude'},
            'title': 'Original Signal'
        }
    }

    filtered_signal_fig = {
        'data': [
            {'x': t, 'y': filtered_y, 'type': 'line', 'name': 'Filtered Signal', 'line': {'color': 'green'}}
        ],
        'layout': {
            'xaxis': {'title': 'Time (s)'},
            'yaxis': {'title': 'Amplitude'},
            'title': 'Filtered Signal'
        }
    }

    return original_signal_fig, filtered_signal_fig, amplitude, frequency, phase, noise_mean, noise_dispersion, show_noise, filter_type


if __name__ == '__main__':
    app.run_server(debug=True)