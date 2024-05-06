program main
implicit none
!???dump??????vasprun.xml
character(len=24) pair_info,pair_read
character(len=19) temp_read1
character(len=21) temp_read2
INTEGER(8) main_i,main_n,Found_pair
character(len=15) pair_read2
character(len=20) disp1,get_disp1
character(len=512) cFile1,cFile2,cFile3
character(len=1) single
character(len=4) write_number
character(len=7) disp2,get_disp2
character(len=8) fcart1,get_fcart
character(len=18) single_id,get_single_id,pair_id
INTEGER(8) NI,current_id(10),pair_ids(10),cck
INTEGER(8) current_atom,pair_atom,atom1,atom2
REAL(8) current_loc(3),pair_loc(3)
INTEGER pair_cycle
INTEGER(8) num_of_ids,temp_i,Force_i,side_i
INTEGER(8) Number_of_data_end
REAL(8) Temp_force(8)
REAL(8) Current_disp(8)
INTEGER(8) Number_of_singles,Number_of_pairs,Number_of_data,glo_i,glo_j
REAL(8),DIMENSION(:,:),ALLOCATABLE :: Disp
REAL(8),DIMENSION(:,:,:),ALLOCATABLE :: Forces
INTEGER(8) Number_of_atoms,total_number

print *,'Number of atoms:'
read(*,*) Number_of_atoms
print *,' '
print *,'Number of data start:'
read(*,*) Number_of_data
print *,' '

ALLOCATE(Disp(Number_of_data,8))
ALLOCATE(Forces(Number_of_data,Number_of_atoms,3))
!print *,'ALLOC'
!????????????????

DO main_n=1,Number_of_data
write(cFile1,*) main_n

open(unit=101,file='BZO-'//Trim(adjustL(cFile1))//'.dump')
DO side_i=1,9
read(101,*)
ENDDO
print *,main_n
DO Force_i=1,Number_of_atoms
read(101,*) Temp_force
Forces(main_n,Force_i,:)=Temp_force(6:8)
ENDDO
close(101)
END DO
!????????????????????vasprun.xml??



DO main_n=1,Number_of_data
write(cFile1,*) main_n
print *,main_n
open(unit=102,file='vasprun-'//Trim(adjustL(cFile1))//'.xml')
write(102,207) '<?xml version="1.0" encoding="ISO-8859-1"?>'
write(102,208) '<modeling>'
write(102,214) ' <generator>'
write(102,216) '  <i name="program" type="string">vasp </i>'
write(102,215) '  <i name="version" type="string">5.4.4.18Apr17-6-g9f103f2a35  </i>'
write(102,211) ' </generator>'
write(102,211) ' <calculation>'
write(102,209) '  <varray name="forces" >'
DO NI=1,Number_of_atoms
    write(102,213) '   <v> ',forces(main_n,NI,:),' </v>'
ENDDO
write(102,210) '  </varray>'
write(102,212) ' </calculation>'
write(102,210) '</modeling>'
close(102)
ENDDO


print *,'Finished, press any key to continue'
read(*,*)

206 format(A8)
207 format(A43)
208 format(A10)
209 format(A25)
210 format(A11)
211 format(A14)
212 format(A15)
213 format(A13,3f16.8,A5)
214 format(A13)
215 format(A68)
216 format(A44)
end program main
SUBROUTINE Suojian(cFile1,ck)
implicit none
character(len=512) cFile1
character(len=12) cFile2,disp1
INTEGER(8) I,ck
disp1='ForceOnAtoms'
ck=0
!ck=0代表这一行不是ForceOnAtoms
I=len(cFile1)
!首先要长度大于22才有可能是ForceOnAtoms
if (I>=22)then
cFile2=cFile1(10:22)
if (cFile2==disp1)then
ck=1
end if 
else
ck=0
end if 

END SUBROUTINE Suojian
SUBROUTINE Delet(cFile1)
implicit none
character(len=512) cFile1
character(len=1) CC

INTEGER(8) I,J

!用来删除逗号
I=len(cFile1)

DO J=1,I
CC=cFile1(J:J)
if (CC==',')then
cFile1(J:J)=' '
end if 
ENDDO

END SUBROUTINE Delet