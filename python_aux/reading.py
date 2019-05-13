#!/usr/bin/env python3
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
from scipy.signal import blackman
#from scipy.signal import hann

def read_tek_tds1012_csv(filename):
    raw_x = []
    raw_y = []

    with open(filename, 'r') as csvfile:
        c = csv.reader(csvfile)

        in_header = True
        for row in c:
            if in_header:
                if row[0] == 'Record Length':
                    record_length = float(row[1])
                if row[0] == 'Sample Interval':
                    sample_interval = float(row[1])
                if row[0] == 'Source':
                    source = str(row[1])
                if row[0] == 'Vertical Units':
                    vertical_units = str(row[1])
                if row[0] == 'Vertical Scale':
                    vertical_scale = float(row[1])
                if row[0] == 'Vertical Offset':
                    vertical_offset = float(row[1])
                if row[0] == 'Horizontal Units':
                    horizontal_units = str(row[1])
                if row[0] == 'Horizontal Scale':
                    horizontal_scale = float(row[1])
                if row[0] == 'Pt Fmt':
                    pt_fmt = str(row[1])
                if row[0] == 'Yzero':
                    yzero = float(row[1])
                if row[0] == 'Probe Atten':
                    probe_atten = float(row[1])
                if row[0] == 'Model Number':
                    model_number = str(row[1])
                if row[0] == 'Serial Number':
                    serial_number = str(row[1])
                if row[0] == 'Firmware Version':
                    firmware_version = str(row[1])
                    in_header = False
            else:
                raw_x.append(float(row[3]))
                raw_y.append(float(row[4]))

        info = {
            'Record Length': record_length,
            'Sample Interval': sample_interval,
            'Source': source,
            'Vertical Units': vertical_units,
            'Vertical Scale': vertical_scale,
            'Vertical Offset': vertical_offset,
            'Horizontal Units': horizontal_units,
            'Horizontal Scale': horizontal_scale,
            'Pt Fmt': pt_fmt,
            'Yzero': yzero,
            'Probe Atten': probe_atten,
            'Model Number': model_number,
            'Serial Number': serial_number,
            'Firmware Version': firmware_version,
        }

    return np.array(raw_x), np.array(raw_y), info

def print_dict(dict):
    for key, value in dict.items():
        print(f'\t{key}: {value}')

def measurements(y):
    measurements = {
        'Max': np.amax(y),
        'Min': np.amin(y),
        'Pk-Pk': np.ptp(y),
        'Mean': np.mean(y),
        'RMS': np.sqrt(np.mean(np.square(y))),
    }

    return measurements

def ab_plot(file_a, file_b, name_a='A', name_b='B', normalize=True):
    x_a, y_a, info_a = read_tek_tds1012_csv(file_a)
    x_b, y_b, info_b = read_tek_tds1012_csv(file_b)


    Ts_a = info_a['Sample Interval']
    Ts_b = info_b['Sample Interval']
    Fs_a = 1/Ts_a
    Fs_b = 1/Ts_b

    N_a = len(y_a)
    N_b = len(y_b)
    w_a = blackman(N_a)
    w_b = blackman(N_b)
    x_a = np.linspace(0.0, N_a * Ts_a, N_a) * 1E6
    x_b = np.linspace(0.0, N_b * Ts_b, N_b) * 1E6
    yf_a = fftpack.fft(y_a * w_a)
    yf_b = fftpack.fft(y_b * w_b)
    yf_a = 20 * np.log10(abs(yf_a[:N_a//2]))
    yf_b = 20 * np.log10(abs(yf_b[:N_b//2]))
    xf_a = np.linspace(0.0, Fs_a/2, int(N_a/2))
    xf_b = np.linspace(0.0, Fs_b/2, int(N_b/2))

    norm = np.max(y_a)/np.max(y_b)

    fig, ax = plt.subplots(2, 1)
    ax[0].set_title(f'Comparação {name_a} e {name_b}')
    ax[0].plot(x_a, y_a, linewidth=0.5, antialiased=None)
    ax[0].plot(x_b, y_b, linewidth=0.5, antialiased=None)
    if normalize:
        ax[0].plot(x_b, y_b * norm, lw=0.5, aa=None, color='gray', alpha=0.5)
    ax[0].set_xlabel('Tempo (us)')
    ax[0].set_ylabel('Amplitude (V)')
    if normalize:
        ax[0].legend([name_a, name_b, f'{name_b} * {np.round(norm, 2)}'])
    else:
        ax[0].legend([name_a, name_b])
    ax[1].plot(xf_a, yf_a, linewidth=0.5, antialiased=None)
    ax[1].plot(xf_b, yf_b, linewidth=0.5, antialiased=None)
    ax[1].set_xlabel('Freq (Hz)')
    ax[1].set_ylabel('Amplitude (dB)')
    ax[1].legend([name_a, name_b])

    plt.show()

    print(f'Info for {name_a}:')
    print_dict(info_a)
    print(f'Info for {name_b}:')
    print_dict(info_b)
    print(f'Time Measurements for {name_a}:')
    print_dict(measurements(y_a))
    print(f'FFT Measurements for {name_a}:')
    print_dict(measurements(yf_a))
    print(f'Time Measurements for {name_b}:')
    print_dict(measurements(y_b))
    print(f'FFT Measurements for {name_b}:')
    print_dict(measurements(yf_b))


# A/B examples:

filename_a = '03.05/ALL0000/F0000CH1.CSV'
filename_b = '03.05/ALL0001/F0001CH1.CSV'
ab_plot(filename_a, filename_b, 'BNC', 'COAX', normalize=False)

filename_a = '03.05/ALL0000/F0000CH1.CSV'
filename_b = '03.05/ALL0004/F0004CH1.CSV'
ab_plot(filename_a, filename_b, 'COAX', 'Placa 1')

