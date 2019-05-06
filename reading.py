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



##############################
# Gets data:

filename = '03.05/ALL0000/F0000CH1.CSV'
x, y, info = read_tek_tds1012_csv(filename)

print('\nInfo:')
for key, value in info.items():
    print(f'\t{key}: {value}')



##############################
# Plots in time and freq

Ts = info['Sample Interval']
Fs = 1/Ts

N = len(y)
w = blackman(N)
#w = hann(N)
x = np.linspace(0.0, N*Ts, N) * 1E6
yf = fftpack.fft(y * w)
yf = 20*np.log10(abs(yf[:N//2]))
xf = np.linspace(0.0, Fs/2, int(N/2))

fig, ax = plt.subplots(2, 1)
ax[0].plot(x, y, linewidth=0.8)
ax[0].set_xlabel('Tempo (us)')
ax[0].set_ylabel('Amplitude (V)')
ax[1].plot(xf, yf, linewidth=0.8)
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('Amplitude (dB)')

plt.show()



#############################
# Basic measurements

print('\nMeasurements:')
measurements = {
    'Max': np.amax(y),
    'Min': np.amin(y),
    'Pk-Pk': np.ptp(y),
    'Mean': np.mean(y),
    'RMS': np.sqrt(np.mean(np.square(y))),
}

for key, value in measurements.items():
    print(f'\t{key}: {value}')

