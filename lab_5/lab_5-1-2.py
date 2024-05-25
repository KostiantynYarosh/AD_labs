import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

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

def filter_signal(y, cutoff_freq=0.5, order=4):
    b, a = signal.butter(order, cutoff_freq, btype='low', analog=False) #розрахунку коефіцієнтів фільтра Баттерворта
    filtered_y = signal.filtfilt(b, a, y) #застосовує фільтрацію вперед, а потім назад
    return filtered_y

def update(val):
    amplitude = amp_slider.val
    frequency = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_dispersion = noise_dispersion_slider.val
    cutoff_freq = cutoff_slider.val
    order = order_slider.val
    show_noise = checkbox.get_status()[0]

    t, y = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_dispersion, show_noise)
    filtered_y = filter_signal(y, cutoff_freq, order)

    line1.set_data(t, y)
    line2.set_data(t, filtered_y)

    fig.canvas.draw_idle()

def reset(event):
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_dispersion_slider.reset()
    update(None)

def generate_new_noise(event):
    global BASE_NOISE
    BASE_NOISE = np.random.normal(0, 1, 1000)
    update(None)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1.5, 1.5]})
plt.subplots_adjust(bottom=0.5, hspace=0.9)

t, y = harmonic_with_noise(INIT_AMPLITUDE, INIT_FREQUENCY, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_DISPERSION, SHOW_NOISE)
filtered_y = filter_signal(y)

line1, = ax1.plot(t, y, lw=2, color='b', label='Original Signal')
line2, = ax2.plot(t, filtered_y, lw=2, color='g', label='Filtered Signal')

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Harmonic with Noise')

ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Amplitude')
ax2.set_title('Filtered Harmonic')

amp_slider = Slider(plt.axes([0.2, 0.4, 0.65, 0.03]), 'Amplitude', 0.1, 5.0, valinit=INIT_AMPLITUDE, valstep=0.05)
freq_slider = Slider(plt.axes([0.2, 0.35, 0.65, 0.03]), 'Frequency', 0.1, 5.0, valinit=INIT_FREQUENCY, valstep=0.005)
phase_slider = Slider(plt.axes([0.2, 0.3, 0.65, 0.03]), 'Phase', -np.pi, np.pi, valinit=INIT_PHASE, valstep=0.1)
noise_mean_slider = Slider(plt.axes([0.2, 0.25, 0.65, 0.03]), 'Noise (Mean)', -1.0, 1.0, valinit=INIT_NOISE_MEAN, valstep=0.01)
noise_dispersion_slider = Slider(plt.axes([0.2, 0.2, 0.65, 0.03]), 'Noise (Dispersion)', 0.00, 1.0, valinit=INIT_NOISE_DISPERSION, valstep=0.01)
cutoff_slider = Slider(plt.axes([0.2, 0.15, 0.65, 0.03]), 'Cutoff Frequency', 0.01, 0.99, valinit=0.5, valstep=0.01)
order_slider = Slider(plt.axes([0.2, 0.1, 0.65, 0.03]), 'Filter Order', 1.0, 20.0, valinit=4, valstep=1)

checkbox = CheckButtons(plt.axes([0.3, 0.005, 0.2, 0.1]), ['Show Noise'], [SHOW_NOISE])

reset_button = Button(plt.axes([0.5, 0.005, 0.1, 0.1]), 'Reset')
reset_button.on_clicked(reset)

new_noise_button = Button(plt.axes([0.6, 0.005, 0.1, 0.1]), 'New Noise')
new_noise_button.on_clicked(generate_new_noise)

amp_slider.on_changed(update)
freq_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_dispersion_slider.on_changed(update)
cutoff_slider.on_changed(update)
order_slider.on_changed(update)
checkbox.on_clicked(update)

plt.show()