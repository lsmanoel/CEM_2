#!/usr/bin/env python3.7
import matplotlib.pyplot as plt
import mpld3

from StackAxes import StackAxes

plt.rcParams['lines.linewidth'] = 0.9

# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""


class PlotAxesListWeb(StackAxes):
    def __init__(self,
                 file_list=None,
                 axes_list=None,
                 fs=None):

        super().__init__(file_list=file_list,
                         axes_list=axes_list,
                         fs=fs)

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

                mpld3.plugins.connect(fig, mpld3.plugins.MousePosition())

                mpld3.plugins.connect(fig, mpld3.plugins.PointLabelTooltip(
                    ax[0].get_lines()[0],
                    labels=list(axes['axes']['freq']['f'])
                ))

                # handles, labels = ax[1].get_legend_handles_labels()
                # interactive_legend = mpld3.plugins.InteractiveLegendPlugin(
                #     zip(handles, ax[1].collections),
                #     labels,
                #     alpha_unsel=0.5,
                #     alpha_over=1.5,
                #     start_visible=True)
                # mpld3.plugins.connect(fig, interactive_legend)

        # ==================================================

        mpld3.show()

    @staticmethod
    def testbench():
        print(">>> >>> >>> TesTE <<< <<< <<<")
        file_list = []

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

        axes_list = PlotAxesListWeb(file_list)

        axes_list.plot_axes_list(plot_mode='freq_dB')

        print(">>> >>> >>> EndTE <<< <<< <<<")


PlotAxesListWeb.testbench()
