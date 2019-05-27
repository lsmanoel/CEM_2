# Axes

## Axes =[list of Axis]
```python
file_example = {
    'Eut': 'ALL0001 - 13.05',
    'File': '../13.05/ALL0001/F0001CH1.CSV',
    'Photo': '../13.05/img/all0001_13_5.jpg',
    'Legend': 'ALL0001 - 13.05',
    'Signal Freq': 2e6
}

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
	'Eut': file_example['Eut'],
	'File' : file_example['File'],
	'Photo': file_example['Photo'],
	'Legend': file_example['Legend'],
	'Signal Freq': file_example['Signal Freq']
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

## Files =[list of File]	
```python
file_example = {
    'Eut': 'ALL0001 - 13.05',
    'File': '../13.05/ALL0001/F0001CH1.CSV',
    'Photo': '../13.05/img/all0001_13_5.jpg',
    'Legend': 'ALL0001 - 13.05',
    'Signal Freq': 2e6
}

**files_example =[list of file_example]**	
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
```	
