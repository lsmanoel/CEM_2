#!/usr/bin/env python3.7
import pandas as pd
import numpy as np


class Comparison:
    def __init__(self, filename, experiment_folder):
        self._filename = filename
        self._experiment_folder = experiment_folder
        self._experiments_list = self.load()

    @property
    def experiments(self):
        return self._experiments_list

    def load(self):
        df = pd.read_csv(self._filename, encoding='UTF-8')
        df.replace(np.nan, '', regex=True, inplace=True)

        def combineIntoDict(name):
            cols = [f'Board {name}', f'Legend {name}', f'File {name}']
            df[name] = df.apply(lambda row: {
                'Board': row[cols[0]],
                'Legend': row[cols[1]],
                'File': row[cols[2]],
            }, axis=1)
            df.drop(cols, axis=1, inplace=True)

        for char in ['A', 'B', 'C']:
            combineIntoDict(char)

        experiments_list = []
        for observation in df.transpose().to_dict().values():
            file_list = []
            info_dict = {}
            for key, data in zip(observation.keys(), observation.values()):
                if key is 'A' or key is 'B' or key is 'C':
                    if data['File'] is not '':
                        n = ''.join(filter(str.isdigit, data['File']))
                        data['File'] = f'../{self._experiment_folder}/ALL{n}/F{n}CH1.CSV'
                        file_list.append(data)
                else:
                    info_dict.update({key: data})

            experiments_list.append({
                'info_dict': info_dict,
                'file_list': file_list,
            })

        return experiments_list
