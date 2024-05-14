import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def read_file(file):
    with open(file) as f:
        lines = f.readlines()

    data = []
    # 101 datapoint
    for i, line in enumerate(lines):
        if line.startswith('#  T(K)        xx         yy         zz         yz         xz         xy  '):
            print(f'header: {line}')

            data = [x.strip().split() for x in lines[i+1:i+102]]
            break
    return np.array(data)

csv_file = 'Heat1.csv'
if not os.path.exists(csv_file):
    txt_file = 'Heat1.txt'
    data = read_file(txt_file)
    df = pd.DataFrame(data, columns=['T(K)', 'xx', 'yy', 'zz', 'yz', 'xz', 'xy'])
    df.to_csv(csv_file, index=False)
else:
    df = pd.read_csv(csv_file, header=0)
print(df.head())
print(df['T(K)'])
print(df['xx'])

# plt.plot(df['T(K)'][1:50], df['xx'][1:50], label='xx')
# plt.plot(df['T(K)'][1:50], df['yy'][1:50], label='yy')
# plt.plot(df['T(K)'][1:50], df['zz'][1:50], label='zz')
# plt.plot(df['T(K)'][1:50], df['yz'][1:50], label='yz')
# plt.plot(df['T(K)'][1:50], df['xz'][1:50], label='xz')
# plt.plot(df['T(K)'][1:50], df['xy'][1:50], label='xy')
plt.plot(df['T(K)'][1:], df['xx'][1:], label='xx')
plt.plot(df['T(K)'][1:], df['yy'][1:], label='yy')
plt.plot(df['T(K)'][1:], df['zz'][1:], label='zz')
plt.plot(df['T(K)'][1:], df['yz'][1:], label='yz')
plt.plot(df['T(K)'][1:], df['xz'][1:], label='xz')
plt.plot(df['T(K)'][1:], df['xy'][1:], label='xy')
plt.legend()
# plt.show()
plt.savefig('img.png', dpi=300, bbox_inches='tight')