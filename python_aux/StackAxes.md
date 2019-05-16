# StackAxes

```python
axes_list [axes_index]{
	'info': info_dict, 
	'axes': axes_dict
}

	info_dict{
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
		'File Name' : file_name
	}

	axes_dict{
		'time': time_dict,						
		'freq': freq_dict					 	
	}

		time_dict{}
			'plot': plot_dict,
			't': [np.array],
			'x': [np.array]

		freq_dict{}
			'plot': plot_dict,  				
			'f': [np.array],	  	 		 		    
			'H': [np.array],			 		 
			'H_dB': [np.array]

```
				
