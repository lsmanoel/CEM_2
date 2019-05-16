import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

from scipy import fftpack
from scipy.signal import blackman
#from scipy.signal import hann

#===============================================================
# **************************************************************
# **************************************************************
class StackAxes:
	def __init__(self,
				 file_list=None, 
				 data_list=None, 
				 fs=None):

		self._fs = None
		self._Ts = None
		self._file_list = None
		self._axes_list = None

		if fs is not None:
			self._fs = fs
			self._Ts = 1/fs

		elif file_list is not None:
			self._file_list = file_list
			# ==================================================
			# -- > Estrutura data_list
			#
			#	axes_list [index]{}
			#		'info'		: info_dict 
			#		'axes'		: axes_dict
			#		
			#		info_dict{...}
	        #    		'Record Length'		: record_length
	        #    		'Sample Interval'	: sample_interval
	        #    		'Source'			: source
	        #    		'Vertical Units'	: vertical_units
	        #    		'Vertical Scale'	: vertical_scale
	        #    		'Vertical Offset'	: vertical_offset
	        #    		'Horizontal Units'	: horizontal_units
	        #    		'Horizontal Scale'	: horizontal_scale
	        #    		'Pt Fmt'			: pt_fmt
	        #    		'Yzero'				: yzero
	        #    		'Probe Atten'		: probe_atten
	        #    		'Model Number'		: model_number
	        #    		'Serial Number'		: serial_number
	        #    		'Firmware Version'	: firmware_version
			#
			#		axes_dict{}
			#			'time'		: time_dict						
			#			'freq'		: freq_dict					 	
			#			
			#			time_dict{}
			#				't'			: data_dict  
			#				'x'			: data_dict 
			#
			#			freq_dict{}
			#				'f'			: data_dict 	  	 		 		    
			#				'H'			: data_dict 			 		 
			#				'H_dB'		: data_dict 				
			#		
			#				data_dict{}
			#					'array'			: [np.array] 
			#					'config_plot'	: config_plot_dict
			#					
			#					config_plot_dict{}
			#						'legend'		: string
			#						'title'			: string
			#						'xlabel'		: string
			#						'ylabel'		: string
			#					
			self._axes_list = self.file2data_list(self._file_list)
			# =====================================================

		elif axes_list is not None:
			self._axes_list = axes_list

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def read_tek_tds1012_csv(self, filename):
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

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def file2data_list(	self,
						file_list,
						normalize=None,
						window=None,
						fs=None):


		print("file_list_2_data_list()")

		# ==================================================
		# -- > Estrutura data_list
		#	
		# ==================================================
		#	data_list [index]{'info', 'data'}
		#		'info'		: info_dict 
		#		'axes'		: axes_dict
		axes_list = []

		for file in file_list:
			t, x, info_dict = self.read_tek_tds1012_csv(file)

			if fs is None:
				self._Ts = info_dict['Sample Interval']	
				self._fs = 1/self._Ts

			else:
				self._fs = fs
				self._Ts = 1/fs

			N = len(x)
			w = blackman(N)

			# --------------------------------------------------
			time_dict = {
				't'			:np.linspace(0.0, N * self._Ts, N) * 1E6,
				'x'			:x,
			}

			freq_dict = {
				'f'			:np.linspace(0.0, self._fs, N),
				'H'			:fftpack.fft(x * w),
				'H_dB'		:20*np.log10(abs(fftpack.fft(x * w)))
			}

			axes_dict = {
				'time' 		:time_dict,
				'freq'		:freq_dict
			}
			
			# --------------------------------------------------
			axes_list.append({
				'info'		:info_dict, 
				'axes'		:axes_dict
			})
			# ==================================================

		# --------------------------------------------------
		print("len(axes_list): ", len(axes_list))
		# ==================================================
		return axes_list	

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def normalize_data_list(self, 
							data_list,
							master=None):

		print("normalize_data_list()")


	@property
	def file_list(self):
		return self._file_list

	@file_list.setter
	def file_list(self, value):
		self._file_list = value

	@property
	def data_list(self):
		return self._data_list

	@data_list.setter
	def data_list(self, value):
		self._data_list = value
	
	@property
	def fs(self):
		return self._fs

	@fs.setter
	def fs(self, value):
		self._fs = value
		self._Ts = 1/value

	@property
	def Ts(self):
		return self._fs

	@Ts.setter
	def Ts(self, value):
		self._Ts = value
		self._fs = 1//value

#===============================================================
# **************************************************************
# **************************************************************
class PlotDataList(DataList):
	"""docstring for DataList"""
	def __init__(self, 
				 file_list=None, 
				 data_list=None, 
				 fs=None):

		super().__init__(file_list=file_list, 
						 data_list=data_list, 
						 fs=fs)

		self.plot_data_list()

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def plot_data_list(self,
					   plot_mode='freq_dB'):

		print("plot_data_list()")

		# ==================================================
		if plot_mode is None:
			fig, ax = plt.subplots(1, 1, figsize=(6,4))

			for data in self.data_list: 
				ax.plot(data['axes']['time']['t'], data['axes']['time']['x'])
		
			ax.set_xlabel('Tempo (us)')
			ax.set_ylabel('Amplitude (V)')
		# -------------------------------------------------
		else:
			if plot_mode == 'freq':
				fig, ax = plt.subplots(2, 1, figsize=(6,8))

				for data in self.data_list:
					ax[0].plot(data['axes']['time']['t'], data['axes']['time']['x'])
					ax[1].plot(data['axes']['freq']['f'], data['axes']['freq']['H'])

				ax[0].set_xlabel('Tempo (us)')
				ax[0].set_ylabel('Amplitude (V)')
				ax[1].set_xlabel('Freq (MHz)')
				ax[1].set_ylabel('Amplitude (linear)')
				ax[1].set_xlim([0, 125])
			# -------------------------------------------------
			elif plot_mode == 'freq_dB':
				fig, ax = plt.subplots(2, 1, figsize=(6,8))
				for data in self.data_list:
					ax[0].plot(data['axes']['time']['t'], data['axes']['time']['x'])
					ax[1].plot(data['axes']['freq']['f'], data['axes']['freq']['H_dB'])

				ax[0].set_xlabel('Tempo (us)')
				ax[0].set_ylabel('Amplitude (V)')
				ax[1].set_xlabel('Freq (MHz)')
				ax[1].set_ylabel('Amplitude (dB)')
				ax[1].set_xlim([0, self.fs//2])
		# ==================================================
		plt.show()

#===============================================================
# **************************************************************
# **************************************************************				
print(">>> >>> >>> TestE <<< <<< <<<")

filename_a = '../13.05/ALL0000/F0000CH1.CSV'
filename_b = '../13.05/ALL0001/F0001CH1.CSV'
filename_c = '../13.05/ALL0002/F0002CH1.CSV'
filename_d = '../13.05/ALL0003/F0003CH1.CSV'

file_list = [filename_a, filename_b, filename_c, filename_d]

data_list_1 = PlotDataList(file_list)

# data_list_1.ab_plot(filename_a, filename_b, 'BNC', 'COAX', normalize=False)
# data_list_1.ab_plot(filename_a, filename_b, 'COAX', 'Placa 1') 
# data_list_1.file_list_2_data_list(file_list) 

print(">>> >>> >>> EndTe <<< <<< <<<")