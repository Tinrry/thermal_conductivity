# create script from workflow.ipynb
import shutil
import os
import subprocess
import fileinput
import timeit
import threading
import glob


print_format = '==============='

print(print_format + 'step 1: phono3py generate POSCAR' + print_format)
p1 = subprocess.Popen(["phono3py", "-d", "--dim=1 1 1", "-c", "POSCAR_BZO_ROTATION"]) # phono3py -d --dim="1 1 1" -c POSCAR_BZO_ROTATION
p1.wait()
print(print_format + 'step 1: finish' + print_format)

print(print_format + 'step 2: atomsk format poscar to lmp' + print_format)
if os.path.exists('POSCAR-00'):
    shutil.rmtree('POSCAR-00')
os.mkdir("POSCAR-00")
# shutil.move("POSCAR-00*", "POSCAR-00/POSCAR-00*")
for f in glob.glob(r'POSCAR-00*'):
    shutil.move(f, "POSCAR-00")

if os.path.exists('lmp'):
    shutil.rmtree('lmp')
os.mkdir("lmp")

for p, d, files in os.walk("POSCAR-00"):
    for f in files:
        subprocess.run(["atomsk", "POSCAR-00/"+f, "lmp/", "lammps"])      # atomsk POSCAR-00/POSCAR-00001 lammps

print(print_format + 'step 2: finish' + print_format)

print(print_format + 'step 3: configure in.lammps' + print_format)
# in_f = 'in_00002.lammps'
for p, d, files in os.walk('lmp'):
    for f in files:
        if f.endswith('.lmp'):
            base_name = 'POSCAR-00'
            index = f.split('.')[0].replace(base_name, '')
            # index = '001'
            try:
                shutil.copy("in_template.lammps", f"lmp/in-00{index}.lammps")
            except:
                print("in_template.lammps not found")

# generate in.lammps for deepmd
for p, d, files in os.walk("lmp"):
    for f in files:
        if f.endswith('.lammps'):
            base_name='in-00'
            index = f.split('.')[0].replace(base_name, '')
            print(base_name, f, index)
            # configure read_data and write_dump
            old_tag = "<index>"
            new_tag = index
            with fileinput.input(os.path.join('lmp', f), inplace=True) as f_handle:
                for line in f_handle:
                    print(line.replace(old_tag, new_tag), end='')

print(print_format + 'step 3: finish' + print_format)

print(print_format + 'step 4: run lmp' + print_format)
# run deepmd lmp in lmp files , run this command is need wait for a while time. count
def mpi_run():
    start_time = timeit.default_timer()

    count = 0
    for p, d, files in os.walk("lmp"):
        for f in files:
            if f.endswith('.lammps'):
                count += 1
                index = f.split('.')[0].replace('in-', '')
                # TODO THIS COMMAND CAN SYCHRONIZE ???
                p = subprocess.Popen(["mpirun", "-n", "10", "lmp", "-in", f"lmp/{f}", f">lmp-{index}.out",
                                      f"2>lmp-{index}.err"])  # mpirun -n 10 lmp -in in-00002.lammps >lmp-00002.out 2>lmp-00002.err
                p.wait()

    end_time = timeit.default_timer()
    print('Running time: %d Seconds.' % (end_time - start_time))
    if count != 0:
        print('Executed %s times per sample.' % count)


t = threading.Thread(target=mpi_run)
t.start()
t.join()
print(print_format + 'step 4: finish' + print_format)

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
        f.write('   <calculation>\n')
        f.write('       <varray name="force">\n')
        # the force data is in the 10th line to the end
        for i in fxfyfz:
            f.write(f'           <v>{i[0]} {i[1]} {i[2]}</v>\n')
        f.write('       </varray>\n')
        f.write('   </calculation>\n')
        f.write('</modeling>\n')

print(print_format + 'step 5: convert dump to xml' + print_format)
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
        f.write('   <calculation>\n')
        f.write('       <varray name="force">\n')
        # the force data is in the 10th line to the end
        for i in fxfyfz:
            f.write(f'           <v>{i[0]} {i[1]} {i[2]}</v>\n')
        f.write('       </varray>\n')
        f.write('   </calculation>\n')
        f.write('</modeling>\n')

for p, d, files in os.walk("output"):
    for f in files:
        if f.endswith('.dump'):
            dump_file = os.path.join('output', f)
            xml_file = os.path.join('output', f.replace('.dump', '.xml'))
            fxfyfz = read_dump(dump_file)
            write_xml(fxfyfz, xml_file)
print(print_format + 'step 5: finish' + print_format)

print(print_format + 'step 6: phono3py generate thermal conductivity' + print_format)
command_1 = subprocess.Popen(["phono3py", "--cf3", "output/*.xml"])
command_1.wait()
command_2 = subprocess.Popen(["phono3py", "--sym-fc"])
command_2.wait()
command_3 = subprocess.run(["phono3py", "--fc3", "--fc2", "--dim=\"1 1 1\"", "--mesh=\"10 10 10\"", "--br", "--tmin=10", "--tmax=1000", "&> Heat.txt"])
command_3.wait()
print(print_format + 'step 6: finish' + print_format)

print(print_format + 'workflow: done.' + print_format)