# create script from workflow.ipynb
import shutil
import os
import subprocess
import fileinput
import timeit
import threading
import glob
import argparse
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
--dim=2 2 1
--mesh=11 11 11
"""

print_format = '==============='

def step_0(config, dim, mesh):
    # we need to copy the required files to the working directory
    print(print_format + 'step 0: copy files' + print_format)
    save_base = config['save']['path']
    # if os.path.exists(save_base):
    #     shutil.rmtree(save_base)
    os.makedirs(save_base, exist_ok=True)       # if exist, do nothing
    shutil.copy(config['geometry'], save_base)
    shutil.copy(config['properties']['thermal-conductivity']['model'], save_base)
    shutil.copy(config['properties']['thermal-conductivity']['arguments']['in_lammps'], save_base)
    os.chdir(save_base)

def step_1(config, dim, mesh):
    print(print_format + 'step 1: phono3py generate POSCAR' + print_format)
    POSCAR = config['geometry']
    # save_base = config['save']['path']
    # poscar_00 = os.path.join(save_base, 'POSCAR-')
    poscar_00 = 'POSCAR-'

    command_1 = ["phono3py", "-d", f"--dim='{dim}'", "-c", POSCAR]
    print(' '.join(command_1))
    p1 = subprocess.Popen(' '.join(command_1), shell=True) # phono3py -d --dim="1 1 1" -c POSCAR_BZO_ROTATION
    p1.wait()
    if os.path.exists(poscar_00):
        shutil.rmtree(poscar_00)
    os.mkdir(poscar_00)
    # shutil.move("POSCAR-*", "POSCAR-/POSCAR-*")
    for f in glob.glob(r'POSCAR-*'):
        shutil.move(f, poscar_00)
    print(print_format + 'step 1: finish' + print_format)


def step_2(config, dim, mesh):
    print(print_format + 'step 2: atomsk format poscar to lmp' + print_format)
    # save_base = config['save']['path']
    save_base = os.getcwd()
    lmp_dir = os.path.join(save_base, 'lmp')
    poscar_00 = os.path.join(save_base, 'POSCAR-')

    if os.path.exists(lmp_dir):
        shutil.rmtree(lmp_dir)
    os.mkdir(lmp_dir)

    if not os.path.exists(poscar_00):
        print('POSCAR- is not found.')
        return

    for p, d, files in os.walk(poscar_00):
        for f in files:
            full_f = os.path.join(poscar_00, f)
            command_1 = ["atomsk", full_f, "lammps"]
            p1 = subprocess.Popen([' '.join(command_1)], shell=True)      # atomsk POSCAR-/POSCAR-00001 lammps
            p1.wait()
    
    for f in glob.glob(f'{poscar_00}/*lmp'):
        shutil.move(f, lmp_dir)
    print(print_format + 'step 2: finish' + print_format)

def step_3(config, dim, mesh):
    print(print_format + 'step 3: configure in_lammps' + print_format)
    # save_base = config['save']['path']
    save_base = os.getcwd()
    lmp_dir = os.path.join(save_base, 'lmp')
    in_f = config['properties']['thermal-conductivity']['arguments']['in_lammps']


    # in_f = 'in_00002.lammps'
    for p, d, files in os.walk(lmp_dir):
        for f in files:
            if f.endswith('.lmp'):
                base_name = 'POSCAR-'
                index = f.split('.')[0].replace(base_name, '')
                # index = '001'
                try:
                    shutil.copy(in_f, f"{lmp_dir}/in-{index}.lammps")
                except:
                    print("in_template.lammps not found")

    # generate in_lammps for deepmd
    for p, d, files in os.walk(lmp_dir):
        for f in files:
            if f.endswith('.lammps'):
                base_name='in-'
                index = f.split('.')[0].replace(base_name, '')
                # print(base_name, f, index)
                # configure read_data and write_dump
                old_tag = "<index>"
                new_tag = index
                with fileinput.input(os.path.join(lmp_dir, f), inplace=True) as f_handle:
                    for line in f_handle:
                        print(line.replace(old_tag, new_tag), end='')

    print(print_format + 'step 3: finish' + print_format)

# run deepmd lmp in lmp files , run this command is need wait for a while time. count
def mpi_run(cores=1):
    start_time = timeit.default_timer()
    lmp_dir = os.path.join(os.getcwd(), 'lmp')
    print(lmp_dir)
    print("run lammps in ", os.getcwd())
    count = 0
    for p, d, files in os.walk(lmp_dir):
        for f in files:
            if f.endswith('.lammps'):
                count += 1
                index = f.split('.')[0].replace('in-', '')
                if cores > 1:
                    command_1 = ["mpirun", "-n", str(cores), "lmp", "-in", f"{lmp_dir}/{f}", f">lmp-{index}.out", f"2>lmp-{index}.err"]  # mpirun -n 10 lmp -in in-00002.lammps >lmp-00002.out 2>lmp-00002.err
                else:
                    command_1 = ["lmp", "-in", f"{lmp_dir}/{f}", f">lmp-{index}.out", f"2>lmp-{index}.err"]  # lmp -in in-00002.lammps >lmp-00002.out 2>lmp-00002.err
                print(' '.join(command_1))
                p = subprocess.Popen([' '.join(command_1)], shell=True)  # mpirun -n 10 lmp -in in-00002.lammps >lmp-00002.out 2>lmp-00002.err
                p.wait()

    end_time = timeit.default_timer()
    print('Running time: %d Seconds.' % (end_time - start_time))
    if count != 0:
        print(f'Executed {(end_time - start_time) / count} times per sample.')

def step_4(config, dim, mesh):
    # save_base = config['save']['path']
    save_base = os.getcwd()
    lmp_dir = os.path.join(save_base, 'lmp')

    print(print_format + 'step 4: run lmp' + print_format)
    cores = config["properties"]["thermal-conductivity"]["arguments"]["cores"]
    t = threading.Thread(target=mpi_run, args=(cores,))
    t.start()
    t.join()
    print(print_format + 'step 4: finish' + print_format)

# # format deepmd output BZO-00002.dump to xml file for phono3py

# format deepmd output BZO-00002.dump to xml file for phono3py
def read_dump(dump_file):
    with open(dump_file, 'r') as f:
        lines = f.readlines()
    lines = lines[9:]
    data = [i.split() for i in lines]
    fxfyfz = []
    for i in data:
        fxfyfz.append([float(i[-3]), float(i[-2]), float(i[-1])])
    return fxfyfz

def write_xml(fxfyfz, xml_file):
    with open(xml_file, 'w') as f:
        f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        f.write('<modeling>\n')
        f.write('   <generator>\n')
        f.write('       <i name="program" type="string">vasp </i>\n')
        f.write('       <i name="version" type="string">5.4.4.18Apr17-6-g9f103f2a35  </i>\n')
        f.write('   </generator>\n')
        f.write('   <calculation>\n')
        f.write('       <varray name="forces">\n')
        # the force data is in the 10th line to the end
        for i in fxfyfz:
            f.write(f'           <v>       {i[0]}      {i[1]}      {i[2]} </v>\n')
        f.write('       </varray>\n')
        f.write('   </calculation>\n')
        f.write('</modeling>\n')


def step_5(config, dim, mesh):
    print(print_format + 'step 5: convert dump to xml' + print_format)
    save_base = os.getcwd()
    # the command in step_4 will generate dump file in output working directory, and we need to convert it to xml file
    xml_dir = os.path.join(save_base, 'output')
    dump_dir = 'output'
    for p, d, files in os.walk(dump_dir):
        for f in files:
            if f.endswith('.dump'):
                dump_file = os.path.join(dump_dir, f)
                xml_file = os.path.join(xml_dir, f.replace('.dump', '.xml'))
                fxfyfz = read_dump(dump_file)
                write_xml(fxfyfz, xml_file)
    print(print_format + 'step 5: finish' + print_format)

def step_6(config, dim, mesh ):
    save_base = os.getcwd()     # because we change the working directory in step_0
    print(print_format + 'step 6: phono3py generate thermal conductivity' + print_format)
    os.chdir(save_base)

    # 必须使用com_1拼接，否则phono3py的run mode会出现问题
    com_1 = ["phono3py", "--cf3", "output/*.xml"]
    print("run ", ' '.join(com_1))
    command_1 = subprocess.Popen(' '.join(com_1), shell=True)
    command_1.wait()
    
    # com_2_251 = ["phono3py", "--sym-fc"]
    com_2_303 = ["phono3py", "--sym-fc", "phono3py_disp.yaml"]
    print("run ", ' '.join(com_2))
    command_2 = subprocess.Popen(' '.join(com_2_303), shell=True)
    command_2.wait()

    # this step will take a long time when set mesh='11 11 11'
    heat = open('Heat1.txt', 'w')
    heat.flush()
    # 必须有双引号
    run_mode_RTA = ["phono3py", "--fc3", "--fc2", f"--dim=\"{dim}\"", f"--mesh=\"{mesh}\"", "--br", "--tmin=10", "--tmax=1000"]
    print(' '.join(run_mode_RTA))
    command_3 = subprocess.Popen([' '.join(run_mode_RTA)], stdout=heat, stderr=heat, shell=True)
    command_3.wait()
    print(print_format + 'step 6: finish' + print_format)


def read_heat_txt(file):
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

def step_7(config, dim, mesh):
    csv_file = 'Heat1.csv'
    if not os.path.exists(csv_file):
        data = read_heat_txt('Heat1.txt')
        df = pd.DataFrame(data, columns=['T(K)', 'xx', 'yy', 'zz', 'yz', 'xz', 'xy'])
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file, header=0)
    
        plt.plot(df['T(K)'][1:], df['xx'][1:], label='xx')
        plt.plot(df['T(K)'][1:], df['yy'][1:], label='yy')
        plt.plot(df['T(K)'][1:], df['zz'][1:], label='zz')
        plt.plot(df['T(K)'][1:], df['yz'][1:], label='yz')
        plt.plot(df['T(K)'][1:], df['xz'][1:], label='xz')
        plt.plot(df['T(K)'][1:], df['xy'][1:], label='xy')
        plt.legend()
        plt.savefig('img.png', dpi=300, bbox_inches='tight')

    
def DAG(config, dim, mesh):
    step_0(config, dim, mesh)
    step_1(config, dim, mesh)
    step_2(config, dim, mesh)
    step_3(config, dim, mesh)
    step_4(config, dim, mesh)
    step_5(config, dim, mesh)
    step_6(config, dim, mesh)
    step_7(config, dim, mesh)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='workflow for thermal conductivity.')

    parser.add_argument('-c', '--configure', required=True, help='POSACR file name')
    # parser.add_argument('--dim', type=str, default='2 2 1', help='dim')
    # parser.add_argument('--mesh', type=str, default='11 11 11', help='mesh')
    args = parser.parse_args()

    f_config = open(args.configure, 'r')
    config = json.load(f_config)

    dim = config["properties"]["thermal-conductivity"]["arguments"]["dim"]
    mesh = config["properties"]["thermal-conductivity"]["arguments"]["mesh"]
    # this config give you work directory, *.pb, POSCAR_BZO_ROTATION
    # worker(config, dpcal, logger)
    DAG(config, dim, mesh)
    print(print_format + 'workflow: done.' + print_format)

# python workflow.py -c default_pbc.json