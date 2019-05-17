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
#plt.rcParams['axes.facecolor'] = 'black'


# ===============================================================
# **************************************************************
# **************************************************************
class StackAxes:
    def __init__(self,
                 file_list=None,
                 axes_list=None,
                 fs=None):

        self._fs = None
        self._Ts = None
        self._file_list = None
        self._axes_list = None

        if fs is not None:
            self._fs = fs
            self._Ts = 1 / fs

        elif file_list is not None:
            self._file_list = file_list
            self._axes_list = self.file2axes_list(self._file_list)

        elif axes_list is not None:
            self._axes_list = axes_list

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read_tek_tds1012_csv(self, file_name):
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
                'File Name': None,
                'Board': None,
                'Legend': None,
            }

        return np.array(raw_x), np.array(raw_y), info

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def file2axes_list(	self,
                        file_list,
                        normalize=None,
                        window=None,
                        fs=None):

        print("file2axes_list()")

        axes_list = []

        if window is None:
            w = 1

        for file in file_list:
            t, x, info_dict = self.read_tek_tds1012_csv(file['File Name'])
            
            info_dict['Board'] = file['Board']
            info_dict['File Name'] = file['File Name']
            info_dict['Legend'] = file['Legend']

            if fs is None:
                self._Ts = info_dict['Sample Interval']
                self._fs = 1 / self._Ts

            else:
                self._fs = fs
                self._Ts = 1 / fs

            # Considering a fundamental freq. of 2 MHz for the signal
            F_signal = 2E6
            T_signal = 1 / F_signal

            # Get the number of samples to perfectly match F_signal
            N = int(((len(x) * self._Ts) // T_signal) *
                    round(T_signal / self._Ts))

            x = x[:N]

            xfft = np.fft.rfft(x * w, N)

            # --------------------------------------------------
            time_dict = {
                't'	: np.linspace(0.0, N * self._Ts, N) * 1E6,
                'x': x,
            }

            freq_dict = {
                'f': np.linspace(0, self._fs / 2, len(xfft)) * 1E-6,
                'H': xfft,
                'H_dB': 20 * np.log10(abs(xfft))
            }

            axes_dict = {
                'time': time_dict,
                'freq': freq_dict
            }

            # --------------------------------------------------
            axes_list.append({
                'info': info_dict,
                'axes': axes_dict
            })

        # --------------------------------------------------
        print("len(axes_list): ", len(axes_list))
        # ==================================================
        return axes_list

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def normalize_axes_list(self,
                            axes_list,
                            master=None):

        print("normalize_axes_list()")

    @property
    def file_list(self):
        return self._file_list

    @file_list.setter
    def file_list(self, value):
        self._file_list = value

    @property
    def axes_list(self):
        return self._axes_list

    @axes_list.setter
    def axes_list(self, value):
        self._axes_list = value

    @property
    def fs(self):
        return self._fs

    @fs.setter
    def fs(self, value):
        self._fs = value
        self._Ts = 1 / value

    @property
    def Ts(self):
        return self._fs

    @Ts.setter
    def Ts(self, value):
        self._Ts = value
        self._fs = 1 // value


# ===============================================================
# **************************************************************
# **************************************************************
class PlotAxesList(StackAxes):
    def __init__(self,
                 file_list=None,
                 axes_list=None,
                 fs=None):

        super().__init__(file_list=file_list,
                         axes_list=axes_list,
                         fs=fs)

        # self.plot_axes_list()

    # ===========================================================
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def plot_axes_list(self,
                       plot_mode=None):

        print("plot_axes_list()")

        axes_name = []
        # ==================================================
        if plot_mode is None:
            fig, ax = plt.subplots(1, 1, figsize=(6, 4))

            for i, axes in enumerate(self.axes_list):
                ax.plot(axes['axes']['time']['t'], axes['axes']['time']['x'])
                axes_name.append(axes['info']['Legend'])

            ax[0].set_xlim([4.6, 5.6])
            ax.legend(axes_name)
            ax.set_xlabel('Tempo (us)')
            ax.set_ylabel('Amplitude (V)')
        # -------------------------------------------------
        else:
            if plot_mode == 'freq':
                fig, ax = plt.subplots(2, 1, figsize=(6, 8))

                for axes in self.axes_list:
                    ax[0].plot(axes['axes']['time']['t'],
                               axes['axes']['time']['x'])
                    ax[1].plot(axes['axes']['freq']['f'],
                               axes['axes']['freq']['H'])
                    axes_name.append(axes['info']['Legend'])

                # ax[0].set_xlim([4.6, 5.6])
                ax[0].legend(axes_name)
                ax[0].set_xlabel('Tempo (us)')
                ax[0].set_ylabel('Amplitude (V)')
                ax[1].set_xlabel('Freq (MHz)')
                ax[1].set_ylabel('Amplitude (linear)')
            # -------------------------------------------------
            elif plot_mode == 'freq_dB':
                fig, ax = plt.subplots(2, 1, figsize=(6, 8))
                for axes in self.axes_list:
                    ax[0].plot(axes['axes']['time']['t'],
                               axes['axes']['time']['x'])
                    ax[1].plot(axes['axes']['freq']['f'],
                               axes['axes']['freq']['H_dB'])
                    axes_name.append(axes['info']['Legend'])
                
                # ax[0].set_xlim([4.6, 5.6])
                ax[0].legend(axes_name)
                ax[0].set_xlabel('Tempo (us)')
                ax[0].set_ylabel('Amplitude (V)')
                ax[1].set_xlabel('Freq (MHz)')
                ax[1].set_ylabel('Amplitude (dB)')
        # ==================================================
        plt.show()

    @staticmethod
    def testbench():
        print(">>> >>> >>> TesTE <<< <<< <<<")
        file_list=[]

        file_list.append({
        	    'Board': 'Board A',
                'File Name': '../13.05/ALL0000/F0000CH1.CSV',
                'Legend': 'Board A'})

        file_list.append({
        	    'Board': 'Board B',
                'File Name': '../13.05/ALL0001/F0001CH1.CSV',
                'Legend': 'Board B'})

        file_list.append({
        	    'Board': 'Board C',
                'File Name': '../13.05/ALL0002/F0002CH1.CSV',
                'Legend': 'Board C'})


        file_list.append({
        	    'Board': 'Board D',
                'File Name': '../13.05/ALL0003/F0003CH1.CSV',
                'Legend': 'Board D'})

        
        axes_list = PlotAxesList(file_list)
        
        axes_list.plot_axes_list(plot_mode='freq_dB')
        
        print(">>> >>> >>> EndTE <<< <<< <<<")



# ===============================================================
# **************************************************************
# **************************************************************
PlotAxesList.testbench()