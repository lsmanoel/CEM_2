#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from PySide2.QtCore import Slot
# from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import QObject
from PySide2.QtQml import qmlRegisterType
import json


class Comparison(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self)
        self._filename = None
        self._experiment_folder = None
        self._experiments_list = None

    @property
    def experiments(self):
        # print('python:')
        # print(self._experiments_list[0]['file_list'])
        # json.dumps()
        return self._experiments_list

    @Property(str)
    def experiments_title(self):
        el = self._experiments_list.copy()
        for i, l in enumerate(el):
            el[i]['file_list'] = json.dumps(l['file_list'])
        return json.dumps(el)

    @Slot(str)
    def load(self, filename, experiment_folder='13.05'):
        self._filename = filename
        self._experiment_folder = experiment_folder

        df = pd.read_csv(self._filename, encoding='UTF-8')
        df.replace(np.nan, '', regex=True, inplace=True)

        def combineIntoDict(name):
            cols = [f'Board {name}', f'Legend {name}', f'File {name}']
            df[name] = df.apply(lambda row: {
                'Eut': row[cols[0]],
                'Legend': row[cols[1]],
                'File': row[cols[2]],
                'Photo': 'none',
                'Signal Freq': 2E6,
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
                        data['Photo'] = f'../{self._experiment_folder}/img/all{n}_13_5.jpg'
                        file_list.append(data)
                else:
                    info_dict.update({key: data})

            experiments_list.append({
                'info_dict': info_dict,
                'file_list': file_list,
            })

        self._experiments_list = experiments_list
