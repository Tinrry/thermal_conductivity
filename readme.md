
## 介绍
输入的文件：
graph18-compress0.pb # 该文件太大，无法上传git

POSCAR_BZO_ROTATION

in_template.lammps # 运行自动流程脚本需要
## 运行
python workflow.py

## 程序运行的过程解释和说明
https://www.notion.so/0632b5a9bf9f45d7945525d8d82211b2?pvs=4
## 备注
1. the bzo example will take 1h in mpirun with np=10, and 517 cases.

2. 
  ```
phono3py --fc3 --fc2 --dim="1 1 1" --mesh="11 11 11"  --br --tmin=10 --tmax=1000 > Heat.txt &
```

will take a while depend on --mesh="11 11 11"

