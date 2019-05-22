#!/usr/bin/env python3.7
import csv
import matplotlib.pyplot as plt
import numpy as np

# Plots configuration
# list of styles:

# plt.style.use('dark_background')

#  https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 10
plt.rcParams['figure.figsize'] = 10, 15
# To look as crispy as osciloscope images:
plt.rcParams['lines.linewidth'] = 0.01
plt.rcParams['lines.antialiased'] = False
# # plt.rcParams['axes.facecolor'] = 'black'


# ===============================================================
# **************************************************************
# **************************************************************
class Axis:
    def __init__(self):
        pass

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def file2axis(self,
                  file=None,
                  board=None,
                  legend=None,
                  window=1):

        print("file2axis()")

        if file is not None:
            t, sig, info_dict = self.read_csv(file['File'])

            Ts = info_dict['Sample Interval']
            fs = 1 / Ts
      
            info_dict['Eut'] = file['Eut']
            info_dict['File'] = file['File']
            info_dict['Legend'] = file['Legend']
            info_dict['Signal Freq'] = file['Signal Freq']
            sig_f = file['Signal Freq'];

            # **************************************************
            # --------------------------------------------------
            sig_T = 1/sig_f
            # Get the number of samples to perfectly match F_signal
            N = int(((len(sig) * Ts) // sig_T) *
                    round(sig_T / Ts))

            # --------------------------------------------------
            # **************************************************

            sig = sig[:N]
            t = np.linspace(0.0, N * Ts, N) * sig_f/2

            H = np.fft.rfft(sig * window, N)
            H_dB = 20 * np.log10(abs(H))
            f = np.linspace(0, fs / 2, len(H)) * 2/sig_f

            # --------------------------------------------------
            time_dict = {
                't': t, 
                'sig': sig
            }

            freq_dict = {
                'f': f ,
                'H': H,
                'H_dB': H_dB
            }

            data_dict = {
                'time': time_dict,
                'freq': freq_dict
            }

            if board is not None:
                info_dict['Board'] = board
            if legend is not None:
                info_dict['Legend'] = legend
            if sig_f is not None:
                info_dict['Signal Freq'] = sig_f
            if window is not None:
                info_dict['Window'] = window
            else:
                info_dict['Window'] = 1

            axis = {
                'info': info_dict, 
                'data': data_dict
            }

            return axis


    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Miscellaneous
    def read_csv(self, 
                 file_name, 
                 type="tek_tds1012"):# tds1012
        
        if type == "tek_tds1012":
            raw_x = []
            raw_y = []

            with open(file_name, 'r') as csv_file:
                c = csv.reader(csv_file)

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

                info_dict = {
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
                    'Eut': None,
                    'File': None,
                    'Legend': None,
                    'Signal Freq': None
                }

            return np.array(raw_x), np.array(raw_y), info_dict

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def measurements(axis):
        axis_measurements = {
            'Eut': axis['info']['Eut'],
            'Max': np.amax(axis['data']['time']['sig']),
            'Min': np.amin(axis['data']['time']['sig']),
            'Pk-Pk': np.ptp(axis['data']['time']['sig']),
            'Mean': np.mean(axis['data']['time']['sig']),
            'RMS': np.sqrt(np.mean((axis['data']['time']['sig'])**2)),
        }

        return axis_measurements

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def print_dict(dict):
        for key, value in dict.items():
            print(f'\t{key}: {value}')

# ===============================================================
# **************************************************************
# **************************************************************
class Axes(Axis):
    def __init__(self):
        pass

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def files2axes(self,
                   files,
                   window=1):

        print("file2axes")

        axes = []

        for file in files:
            axes.append(
                self.file2axis(file,
                               window=window)       
            )
        # --------------------------------------------------
        print("len(axes): ", len(axes))
        # ==================================================
        return axes


    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def measurements(axes):

        axes_measurements = []

        for axis in axes:
            axis_measurements = {
                'Eut': axis['info']['Eut'],
                'Max': np.amax(axis['data']['time']['sig']),
                'Min': np.amin(axis['data']['time']['sig']),
                'Pk-Pk': np.ptp(axis['data']['time']['sig']),
                'Mean': np.mean(axis['data']['time']['sig']),
                'RMS': np.sqrt(np.mean((axis['data']['time']['sig'])**2)),
            }
            axes_measurements.append(axis_measurements)

        return axes_measurements


    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def print_dict(dicts):
        for dict in dicts:
            print('___')
            for key, value in dict.items():
                print(f'\t{key}: {value}')


# ===============================================================
# **************************************************************
# **************************************************************
class PlotAxes(Axes):
    def __init__(self):
        pass
    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def plot_axes(self,
                  axes,
                  sig_f=None,
                  plot_mode=None):

        print("plot_axes()")

        axis_legend = []
        # ==================================================
        if plot_mode is None:
            fig, ax = plt.subplots(1, 1, figsize=(6, 4))

            for i, axis in enumerate(axes):
                ax.plot(axis['axis']['time']['t'], axes['axis']['time']['sig'])
                axis_legend.append(axis['info']['Legend'])

            ax[0].set_xlim([4.6, 5.6])
            ax.legend(axis_legend)
            ax.set_xlabel('Tempo (us)')
            ax.set_ylabel('Amplitude (V)')
        # -------------------------------------------------
        else:
            if plot_mode == 'freq':
                fig, ax = plt.subplots(2, 1, figsize=(6, 7))

                for axis in axes:
                    ax[0].plot(axis['data']['time']['t'],
                               axis['data']['time']['sig'])
                    ax[1].plot(axis['data']['freq']['f'],
                               axis['data']['freq']['H'])
                    axis_legend.append(axis['info']['Legend'])

                # ax[0].set_xlim([4.6, 5.6])
                ax[0].legend(axis_legend)
                ax[0].set_xlabel('Tempo (us)')
                ax[0].set_ylabel('Amplitude (V)')
                ax[1].set_xlabel('Freq (MHz)')
                ax[1].set_ylabel('Amplitude (linear)')
            # -------------------------------------------------
            elif plot_mode == 'freq_dB':
                fig, ax = plt.subplots(2, 1, figsize=(6, 7))
                for axis in axes:
                    ax[0].plot(axis['data']['time']['t'],
                               axis['data']['time']['sig'])
                    ax[1].plot(axis['data']['freq']['f'],
                               axis['data']['freq']['H_dB'])
                    axis_legend.append(axis['info']['Legend'])

                # ax[0].set_xlim([4.6, 5.6])
                ax[0].legend(axis_legend)
                ax[0].set_xlabel('Tempo (us)')
                ax[0].set_ylabel('Amplitude (V)')
                ax[1].set_xlabel('Freq (MHz)')
                ax[1].set_ylabel('Amplitude (dB)')
        # ==================================================
        plt.show()

    @staticmethod
    def testbench():
        print(">>> >>> >>> TesTE <<< <<< <<<")
        print("testbench()")

        files = []

        files.append({
            'Eut': 'Board A',
            'File': '../13.05/ALL0000/F0000CH1.CSV',
            'Legend': 'Board A',
            'Signal Freq': 2e6})

        files.append({
            'Eut': 'Board B',
            'File': '../13.05/ALL0001/F0001CH1.CSV',
            'Legend': 'Board B',
            'Signal Freq': 2e6})

        files.append({
            'Eut': 'Board C',
            'File': '../13.05/ALL0002/F0002CH1.CSV',
            'Legend': 'Board C',
            'Signal Freq': 2e6})

        files.append({
            'Eut': 'Board D',
            'File': '../13.05/ALL0003/F0003CH1.CSV',
            'Legend': 'Board D',
            'Signal Freq': 2e6})

        ploter = PlotAxes()
        axes = ploter.files2axes(files, window=1)
        ploter.print_dict(ploter.measurements(axes))
        ploter.plot_axes(axes, plot_mode='freq_dB')

        print(">>> >>> >>> EndTE <<< <<< <<<")


# ===============================================================
# **************************************************************
# **************************************************************

if __name__ == '__main__':
    PlotAxes.testbench()
