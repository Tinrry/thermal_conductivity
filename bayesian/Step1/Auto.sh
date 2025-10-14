for((i=0;i<=18;i++))
do
mkdir ${i}
cp files_Phi ${i}/.
cp input_Phi.in ${i}/input_Phi.in
#cp CsSnI_0704.ddb.out ${i}/CsSnI_0704.ddb.out
cp /home/Multibinit/Multibinit_run/BTO_machine_learning/Model/Model_zero/${i}.xml ${i}/R3m_coeffs.xml
cp L6_HIST.nc ${i}/TS.nc
cd ${i}
mpirun -np 4 multibinit <files_Phi> log.txt

agate -t TS.nc ph_test.nc << EOF
:tbegin 1053
:dhist Result.nc
:q
EOF

ncdump Result.nc > ${i}_HIST.nc
cp ${i}_HIST.nc ../.
cp TES_fit_diff_energy.dat ../TES_fit_diff_energy_${i}.dat

cd ..

done