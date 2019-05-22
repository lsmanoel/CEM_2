# Axes

```python
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
	'File Name' : file_name,
	'Board': board_name,
	'Legend': axes_legend,
}

data_dict = {
    'time': time_dict,
    'freq': freq_dict
}

time_dict = {
    't': t, 
    'sig': sig
}

freq_dict = {
    'f': f,
    'H': H,
    'H_dB': H_dB
}

axis = {
	'info': info_dict, 
	'data': data_dict
}

```
Axes =[list of Axis]		
