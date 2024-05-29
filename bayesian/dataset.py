import pandas as pd
import numpy as np
import re


FEATURE_SIZE = 18

def read_txt_and_save_to_csv(feature_file, energy_file,  csv_file):
    header_name = ['energy']
    for i in range(FEATURE_SIZE):
        header_name.append(f'phi_{i}')
    print(f'header_name: {header_name[:]}')

    df_f = pd.read_csv(feature_file, dtype=np.float128, header=None)
    df_e = pd.read_csv(energy_file, dtype=np.float128, header=None) 
    print('feature file shape: ', df_f.shape)
    print('energy file shape: ', df_e.shape)
    try:
        df = pd.concat([df_e, df_f], axis=1)
        df.to_csv(csv_file, index=False, header=header_name)
    except Exception as e:
        print(f'Error: {e}')
    return csv_file


def convert_space_CRLF2LF(input_file, output_file):
    # CRLF:\r\n为Windows格式txt, LF：\n为linux的换行格式
    with open(input_file, 'r', newline='\r\n') as infile:
        contents = infile.readlines()
        # 删除多余空格
        contents = [re.sub(' +', ' ', content).strip().split() for content in contents]
    with open(output_file, 'w', newline='\n') as outfile:
        for content in contents:
            # pandas 读取csv时，逗号分隔
            outfile.write(','.join(content) + '\n')
    return output_file


# main
for input_file in  ['Phi_20240529.txt', 'Y_20240529.txt']:
    output_file = input_file.split('.')[0] + '_converted.txt'
    convert_space_CRLF2LF(input_file, output_file)

read_txt_and_save_to_csv('phi_20240529_converted.txt', 'y_20240529_converted.txt', 'data_20240529.csv')
# test
df = pd.read_csv('data_20240529.csv', dtype=np.float128)
print(df.describe())
