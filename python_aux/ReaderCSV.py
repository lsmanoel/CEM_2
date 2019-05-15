import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

from scipy import fftpack
from scipy.signal import blackman
#from scipy.signal import hann
#from __future__ import fstrings

#===============================================================
# **************************************************************
# **************************************************************
class DataList:
	def __init__(self, file_list):

		self._file_list = file_list

		# ==================================================
		# -- > Estrutura data_list
		#
		#	data_list [index]{'info', 'data'}
		#		'info'		: info_dict 
		#		'axes'		: axes_dict
		#	
		#		axes_dict{'time', 'freq'}
		#			'time'		: time_dict						
		#			'freq'		: freq_dict					 	
		#		
		#			time_dict{'x'}  
		#				'x'			: [np.array]		 		    
		#		
		#			freq_dict{H', 'H_db'}	  	 		 		    
		#				'H'			: [np.array] 			 		 
		#				'H_dB'		: [np.array] 				
		#		
		self._data_list = self.file2data_list(file_list)
		# =====================================================

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
		data_list = []
		# ==================================================

		for file in file_list:
			x, y, info_dict = self.read_tek_tds1012_csv(file)

			if fs is None:
				Ts = info_dict['Sample Interval']	
				fs = 1/Ts
			else:
				Ts = 1/fs

			N = len(x)
			w = blackman(N)

			# =================================================
			#	axes_dict{'time', 'freq'}
			#		'time'		: time_dict						
			#		'freq'		: freq_dict	
			axes_dict = {
				'time' 		:np.linspace(0.0, N * Ts, N) * 1E6,
				'freq'		:np.linspace(0.0, fs/2, N)
			}
			# -------------------------------------------------
			#	time_dict{'x'}  
			#		'x'			: [np.array]		 		    
			time_dict = {
				'x'			:y,
			}
			# -------------------------------------------------
			#	freq_dict{H', 'H_db'}	  	 		 		    
			#		'H'			: [np.array] 			 		 
			#		'H_dB'		: [np.array]	
			freq_dict = {
				'H'			:fftpack.fft(y * w) ,
				'H_dB'		:20*np.log10(abs(fftpack.fft(y * w)))
			}
			# ==================================================
			data_list.append({
				'info'		:info_dict, 
				'axes'		:axes_dict
			})

		# --------------------------------------------------
		print("len(data_list): ", len(data_list))
		# ==================================================
		return data_list	

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def normalize_data_list(self, 
							data_list,
							master=None):

		print("normalize_data_list()")

	@property
	def data_list(self):
		return self._data_list

	@data_list.setter
	def data_list(self, value):
		self._data_list = value
	

#===============================================================
# **************************************************************
# **************************************************************
class PlotDataList(DataList):
	"""docstring for DataList"""
	def __init__(self, file_list):
		super().__init__(file_list)
		self.plot_data_list(self.data_list)

	#===========================================================
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	@staticmethod
	def plot_data_list(	data_list,
						nrow=None,
						ncol=None):

		if 	 ncol is None 		and nrow is None:
			ncol = 1
			nrow = len(data_list[0]['axes'])

		elif ncol is None 		and nrow is not None:
			ncol = len(data_list[0]['axes'])//nrow + 1

		elif ncol is not None 	and nrow is None:
			nrow = len(data_list[0]['axes'])//ncol + 1

		print("plot_data_list()")

		fig, ax = plt.subplots(nrow, ncol)
		plt.show()

#===============================================================
# **************************************************************
# **************************************************************				
print(">>> >>> >>> TestE <<< <<< <<<")

filename_a = '../03.05/ALL0000/F0000CH1.CSV'
filename_b = '../03.05/ALL0001/F0001CH1.CSV'
filename_c = '../03.05/ALL0000/F0002CH1.CSV'
filename_d = '../03.05/ALL0004/F0004CH1.CSV'

file_list = [filename_a, filename_b, filename_a, filename_d]

data_list_1 = PlotDataList(file_list)

# data_list_1.ab_plot(filename_a, filename_b, 'BNC', 'COAX', normalize=False)
# data_list_1.ab_plot(filename_a, filename_b, 'COAX', 'Placa 1') 
# data_list_1.file_list_2_data_list(file_list) 

print(">>> >>> >>> EndTe <<< <<< <<<")