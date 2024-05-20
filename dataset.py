import pandas as pd
import numpy as np
import re


FEATURE_SIZE = 18

def read_txt_and_save_to_csv(feature_file, energy_file,  csv_file):
    header_name = ['energy']
    for i in range(FEATURE_SIZE):
        header_name.append(f'phi_{i}')
    print(f'header_name: {header_name[:]}')

    df_f = pd.read_csv(feature_file, delimiter=' ', dtype=np.float128, header=None)
    df_e = pd.read_csv(energy_file, delimiter=' ', dtype=np.float128, header=None) 
    df = pd.concat([df_e, df_f], axis=1)
    df.to_csv(csv_file, index=False, header=header_name, sep=' ')
    return

def convert_space_CRLF2LF(input_file, output_file):
    # CRLF:\r\n为Windows格式txt, LF：\n为linux的换行格式
    with open(input_file, 'r', newline='\r\n') as infile:
        contents = infile.readlines()
        # 删除多余空格
        contents = [re.sub(' +', ' ', content).strip().split() for content in contents]
    with open(output_file, 'w', newline='\n') as outfile:
        for content in contents:
            outfile.write(' '.join(content) + '\n')


# main
for input_file in  ['phi_100.txt', 'y_100.txt']:
    output_file = input_file.split('.')[0] + '_converted.txt'
    convert_space_CRLF2LF(input_file, output_file)

read_txt_and_save_to_csv('phi_100_converted.txt', 'y_100_converted.txt', 'data.csv')
df = pd.read_csv('data.csv', delimiter=' ', dtype=np.float128)
print(df.describe())