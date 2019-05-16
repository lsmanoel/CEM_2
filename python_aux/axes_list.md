# StackAxes

```python
axes_list [index]{}
	'info': info_dict 
	'axes': axes_dict
	
	info_dict{...}
		'Record Length: record_length
		'Sample Interval': sample_interval
		'Source': source
		'Vertical Units': vertical_units
		'Vertical Scale': vertical_scale
		'Vertical Offset': vertical_offset
		'Horizontal Units': horizontal_units
		'Horizontal Scale': horizontal_scale
		'Pt Fmt': pt_fmt
		'Yzero: yzero
		'Probe Atten': probe_atten
		'Model Number': model_number
		'Serial Number': serial_number
		'Firmware Version': firmware_version

	axes_dict{}
		'time': time_dict						
		'freq': freq_dict					 	
		
		time_dict{}
			't': data_dict  
			'x': data_dict 

		freq_dict{}
			'f': data_dict 	  	 		 		    
			'H': data_dict 			 		 
			'H_dB': data_dict 				
	
			data_dict{}
				'array': [np.array] # <------------- DATA
				'config_plot': config_plot_dict
				
				config_plot_dict{}
					'legend': string
					'title': string
					'xlabel': string
					'ylabel': string
```
				