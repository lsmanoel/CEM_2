
# experiments_list
*experiments_list* is a list of dictionaries returned by `import_comparison_table()`.

The dicionaries inside this list is here mentioned as **experiments**. Each experiment has a **file_list** containing a list of dictionaries, and a **info** describing the goals of the experiment. 

```python
experiments_list[experiment_index] = {
    'info_dict': info_dict,
    'file_list': file_list
}

info_dict = {
    'Title': 'Experiment Title'
    'Category': 'Experiment Category',
    'Description': 'Experiment Description',
    'Observation': 'Observation of the experiment',
}

file_list[file_index] = {
    'Board': 'Board Name',
    'File Name': '../full/path/of/file.csv',
    'Legend': 'Legend of curve of file_index for this experiment'
}
```
