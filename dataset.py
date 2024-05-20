import pandas as pd
import numpy as np

FEATURE_SIZE = 18

def read_txt_and_save_to_csv(feature_file, energy_file,  csv_file):
    header_name = ['energy']
    for i in range(FEATURE_SIZE):
        header_name.append(f'phi_{i}')
    print(f'header_name: {header_name[:]}')

    df_f = pd.read_csv(feature_file, delimiter=' ', dtype=np.float64, header=None)

    df_e = pd.read_csv(energy_file, delimiter=' ', dtype=np.float64) 

    df = pd.concat([df_e, df_f], axis=1)
    print(df_f.shape)
    print(df)

    df.to_csv(csv_file, index=False, header=header_name)


import re

def convert_space_CRLF2LF(input_file, output_file):
    # CRLF:\r\n为Windows格式txt, LF：\n为linux的换行格式
    with open(input_file, 'r', newline='\r\n') as infile:
        contents = infile.readlines()
        contents = [re.sub(' +', ' ', content).strip().split() for content in contents]
        print(f'contents {contents}')
    with open(output_file, 'w', newline='\n') as outfile:
        for content in contents:
            outfile.write(' '.join(content) + '\n')

# 浮点数精度问题,精度损失
# 使用示例
input_file = 'phi_100.txt'  # 原始文件路径
output_file = 'phi_100_converted.txt'  # 输出文件路径
convert_space_CRLF2LF(input_file, output_file)
df = pd.read_csv(output_file, delimiter=' ', dtype=np.float64, header=None)
print(df)