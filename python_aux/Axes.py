#!/usr/bin/env python3.7
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PySide2.QtCore import Slot
from PySide2.QtCore import QObject
import json
import conf as CONF


# ===============================================================
# **************************************************************
# **************************************************************
class Axis(QObject):
    def __init__(self):
        QObject.__init__(self)
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
            info_dict['Photo'] = file['Photo']
            info_dict['Legend'] = file['Legend']
            info_dict['Signal Freq'] = file['Signal Freq']
            sig_f = file['Signal Freq']

            # **************************************************
            # --------------------------------------------------
            sig_T = 1 / sig_f
            # Get the number of samples to perfectly match F_signal
            N = int(((len(sig) * Ts) // sig_T) *
                    round(sig_T / Ts))

            # --------------------------------------------------
            # **************************************************

            sig = sig[:N]
            t = np.linspace(0.0, N * Ts, N) * sig_f / 2

            H = np.fft.rfft(sig * window, N)
            H_dB = 20 * np.log10(abs(H))
            f = np.linspace(0, fs / 2, len(H)) * 2 / sig_f

            # --------------------------------------------------
            time_dict = {
                't': t,
                'sig': sig
            }

            freq_dict = {
                'f': f,
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
                 type="tek_tds1012"):  # tds1012

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
                    'Photo': None,
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
        super().__init__()
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
                super().file2axis(file,
                                  window=window)
            )
        # --------------------------------------------------
        print("len(axes): ", len(axes))
        # print(axes)
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
        super().__init__()
        pass

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def plot_axes(axes,
                  sig_f=None,
                  plot_mode=None):

        print("plot_axes()")
        axis_legend = []
        # ==================================================
        if plot_mode is None:
            fig = plt.figure(constrained_layout=True, figsize=(6, 4))
            gs = GridSpec(8, 8, figure=fig)

            ax_a = fig.add_subplot(gs[:, :-1])
            ax_b = fig.add_subplot(gs[:, -1])

            for i, axis in enumerate(axes):
                ax_a.plot(axis['data']['time']['t'],
                          axis['data']['time']['sig'],
                          alpha=CONF.ALPHA)
                axis_measurements = Axis().measurements(axis)
                ax_b.bar(i, axis_measurements['RMS'])
                axis_legend.append(axis['info']['Legend'])

            ax_a.set_xlim([4.6, 5.6])
            ax_a.legend(axis_legend)
            ax_a.set_xlabel('Tempo (us)')
            ax_a.set_ylabel('Amplitude (V)')

            ax_b.set_ylabel('Amplitude (RMS)')
            plt.tight_layout()

        # -------------------------------------------------
        else:
            if plot_mode == 'freq':
                fig = plt.figure(figsize=(6, 3))

                for axis in axes:
                    plt.plot(axis['data']['freq']['f'],
                             axis['data']['freq']['H'],
                             alpha=CONF.ALPHA)
                    axis_legend.append(axis['info']['Legend'])

                plt.legend(axis_legend)
                plt.xlabel('Freq (MHz)')
                plt.ylabel('Amplitude (linear)')
                plt.tight_layout()
            # -------------------------------------------------
            elif plot_mode == 'freq_dB':
                fig = plt.figure(figsize=(6, 3))

                for axis in axes:
                    plt.plot(axis['data']['freq']['f'],
                             axis['data']['freq']['H_dB'],
                             alpha=CONF.ALPHA)
                    axis_legend.append(axis['info']['Legend'])

                plt.legend(axis_legend)
                plt.xlabel('Freq (MHz)')
                plt.ylabel('Amplitude (dB)')
                plt.tight_layout()
                # -------------------------------------------------
            elif plot_mode == 'photo':
                for axis in axes:
                    plt.figure(figsize=(6, 3))
                    image = plt.imread(axis['info']['Photo'])
                    plt.title(axis['info']['Legend'])
                    plt.imshow(image)
                    plt.grid(False)
                    plt.xticks([])
                    plt.yticks([])
                    plt.tight_layout()

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def files_example():
        files = []

        files.append({
            'Eut': 'ALL0001 - 13.05',
            'File': '../13.05/ALL0001/F0001CH1.CSV',
            'Photo': '../13.05/img/all0001_13_5.jpg',
            'Legend': 'ALL0001 - 13.05',
            'Signal Freq': 2e6})

        files.append({
            'Eut': 'ALL0002 - 13.05',
            'File': '../13.05/ALL0002/F0002CH1.CSV',
            'Photo': '../13.05/img/all0002_13_5.jpg',
            'Legend': 'ALL0002 - 13.05',
            'Signal Freq': 2e6})

        files.append({
            'Eut': 'ALL0003 - 13.05',
            'File': '../13.05/ALL0003/F0003CH1.CSV',
            'Photo': '../13.05/img/all0003_13_5.jpg',
            'Legend': 'ALL0003 - 13.05',
            'Signal Freq': 2e6})

        return files

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @Slot(str)
    def plot_file(self,
                  File=None):
        if File is None:
            files = PlotAxes().files_example()
        else:
            files = json.loads(File)

        axes = PlotAxes().files2axes(files, window=1)

        PlotAxes().print_dict(PlotAxes().measurements(axes))

        PlotAxes().plot_axes(axes, plot_mode='photo')
        PlotAxes().plot_axes(axes, plot_mode='freq_dB')
        PlotAxes().plot_axes(axes)

        plt.tight_layout()
        plt.show()

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def testbench():
        print(">>> >>> >>> TesTE <<< <<< <<<")
        print("testbench()")

        files = PlotAxes().files_example()

        axes = PlotAxes().files2axes(files, window=1)

        PlotAxes().print_dict(PlotAxes().measurements(axes))

        PlotAxes().plot_axes(axes, plot_mode='freq_dB')

        PlotAxes().plot_axes(axes)

        PlotAxes().plot_axes(axes, plot_mode='photo')

        plt.show()

        print(">>> >>> >>> EndTE <<< <<< <<<")


# ===============================================================
# **************************************************************
# **************************************************************

if __name__ == '__main__':
    PlotAxes.plot_file()
