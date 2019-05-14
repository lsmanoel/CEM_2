#!/usr/bin/env python3
import pandas as pd
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
from scipy.signal import hann

plt.style.use('fivethirtyeight')
# plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.antialiased'] = False


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

    F_signal = 2E6
    T_signal = 1 / F_signal

    Ts_a = info_a['Sample Interval']
    Ts_b = info_b['Sample Interval']
    N_a = int(((len(x_a) * Ts_a) // T_signal) * round(T_signal / Ts_a))
    N_b = int(((len(x_b) * Ts_b) // T_signal) * round(T_signal / Ts_b))

    y_a = y_a[:N_a]
    y_b = y_b[:N_b]

    w_a = 1#hann(N_a)
    w_b = 1#hann(N_b)
    x_a = np.linspace(0.0, N_a * Ts_a, N_a) * 1E6
    x_b = np.linspace(0.0, N_b * Ts_b, N_b) * 1E6
    yf_a = abs(fftpack.rfft(y_a * w_a))
    fft_norm = max(yf_a)
    yf_a = 20 * np.log10(yf_a / fft_norm)
    yf_b = abs(fftpack.rfft(y_b * w_b))
    yf_b = 20 * np.log10(yf_b / fft_norm)

    xf_a = fftpack.rfftfreq(N_a, Ts_a) * 1E-6
    xf_b = fftpack.rfftfreq(N_b, Ts_b) * 1E-6

    norm = (np.max(y_a) - np.min(y_a)) / (np.max(y_b) - np.min(y_b))

    fig, ax = plt.subplots(2, 1)
    ax[0].set_title(f'Comparação {name_a} e {name_b}')
    ax[0].plot(x_a, y_a)
    ax[0].plot(x_b, y_b)
    if normalize:
        ax[0].plot(x_b, y_b * norm + np.mean(y_a), color='grey', alpha=0.5)
    ax[0].set_xlabel('Tempo (us)')
    ax[0].set_ylabel('Amplitude (V)')
    if normalize:
        ax[0].legend([name_a, name_b, f'{name_b} * {np.round(norm, 2)}'])
    else:
        ax[0].legend([name_a, name_b])
    ax[1].plot(xf_a, yf_a)
    ax[1].plot(xf_b, yf_b)
    ax[1].set_xlabel('Freq (MHz)')
    ax[1].set_ylabel('Amplitude (dB)')
    ax[1].set_xlim([0, 25])
    ax[1].legend([name_a, name_b])

    # Correlation:
    correlation = np.corrcoef(y_a, y_b)[1, 0]

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
    print(f'Correlation: {correlation}')


# A/B examples:

filename_a = '../13.05/ALL0000/F0000CH1.CSV'
filename_b = '../13.05/ALL0001/F0001CH1.CSV'
ab_plot(filename_a, filename_b, 'BNC', 'COAX')
'''
filename_a = '../13.05/ALL0000/F0000CH1.CSV'
filename_b = '../13.05/ALL0002/F0002CH1.CSV'
ab_plot(filename_a, filename_b, 'COAX', 'Placa 1')
'''

########################################################################
########################################################################
########################################################################


def print_dict_utf8(dictionary):
    print(json.dumps(dictionary, sort_keys=True, indent=2, ensure_ascii=False))


def import_comparison_table(filename):
    df = pd.read_csv(filename, encoding='UTF-8')
    df.replace(np.nan, '', regex=True, inplace=True)

    def combineIntoDict(name):
        cols = [f'Placa {name}', f'Legenda {name}', f'Arquivo {name}']
        df[name] = df.apply(lambda row: {
            'Placa': row[cols[0]],
            'Legenda': row[cols[1]],
            'Arquivo': row[cols[2]],
        }, axis=1)
        df.drop(cols, axis=1, inplace=True)

    combineIntoDict('A')
    combineIntoDict('B')
    combineIntoDict('C')

    return df.transpose().to_dict()


# Comparison table example:
csvtable = '../CEM - 03.05 - Comparações.csv'

data = import_comparison_table(csvtable)

print_dict_utf8(data)


# end
