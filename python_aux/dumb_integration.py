#!/usr/bin/env python3.7

from Comparison import Comparison
from StackAxes import PlotAxesList
import json


def print_dict_utf8(dictionary):
    print(json.dumps(dictionary, sort_keys=True, indent=2, ensure_ascii=False))


comparison_csv = '../CEM - 03.05 - Comparison.csv'
comp1 = Comparison(comparison_csv, '13.05')

for i, experiment in enumerate(comp1.experiments):
    print(f'Experimento n°{i+1}:')
    print(f"Título: {experiment['info_dict']['Title']}")
    print(f"Descrição: {experiment['info_dict']['Description']}")
    print(f"Observação:' {experiment['info_dict']['Observation']}")
    print(f'Lista de Arquivos do experimento:')
    print_dict_utf8(experiment['file_list'])
    print('--------------------------------------------\n')

file_list = comp1.experiments[1]['file_list']
axes_list = PlotAxesList(file_list)
axes_list.plot_axes_list(plot_mode='freq_dB')
