Program main
use gloable
implicit none 
type(manager) :: all_result(200)
!all_result(j) indicates j_HIST.nc
INTEGER(8) num_of_terms,I,num_of_atoms,num_of_steps,Larger
character(len=512) cFile1,cFile_name
character(len=8) cFile2,cFile3,cFile4
REAL(8) Energy_temp(6)
REAL(8),allocatable :: Phi_phi(:,:),Phi_sing_phi(:,:,:),IS(:),JS(:)
INTEGER(8) NI,J,J2,K,L
INTEGER BRIV
REAL(8) Max_Energy,Max_Stress,Max_Force
REAL(8) Guiyihua_Energy,Guiyihua_Stress,Guiyihua_Force
REAL(8) Tee(13)
LOGICAL TT
print *,''
print *,'number of atoms?'
read(*,*) num_of_atoms
print *,''
print *,'number of steps?'
read(*,*) num_of_steps
print *,''
print *, 'This version output a Y only include enenrgies'
!open(unit=101,file='Guiyihua.txt')
!read(101,*) Guiyihua_Energy
!read(101,*) Guiyihua_Stress
!read(101,*) Guiyihua_Force
!close(101)

!0_HIST.nc 是2阶的结果，1_HIST.nc是DFT结果
num_of_terms=1

Larger=(3*num_of_atoms+7)*num_of_steps
TT=.TRUE.
cFile3=' fcart ='
cFile4=' strten'
ALLOCATE(Phi_phi(num_of_terms,num_of_terms))
ALLOCATE(Phi_sing_phi(num_of_steps,num_of_terms,num_of_terms))
!Phi_phi is the total martix
!Phi_sing_phi is the single structure's martix
!Size of Phi_phi should be num_of_terms, because it's the variance of parameters!
DO I=0,num_of_terms
   K=I+1
   print *,I
    ALLOCATE(all_result(K)%Forces(num_of_steps,num_of_atoms,3))
    ALLOCATE(all_result(K)%Stress(num_of_steps,6)) 
    ALLOCATE(all_result(K)%Energy(num_of_steps)) 
    !ALLOCATE(all_result(K)%Phi(num_of_steps,3*num_of_atoms+7,num_of_terms))
    write(cFile_name,*) I
! Reading the forces
    open(unit=101,file=''//Trim(adjustL(cFile_name))//'_HIST.nc')
    open(unit=102,file='output.txt')
    TT=.TRUE.
    DO while(TT)
    read(101,'(A)',IOSTAT=NI) cFile1
    !print *,cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    !print *,cFile1
    exit 
    end if 
    cFile2=cFile1(1:8)
    !write(102,'(A)') cFile2
    if (cFile2==cFile3)then
        !print *,'HERE'
    DO J=1,num_of_steps
    DO J2=1,num_of_atoms
    write(102,*) J,J2
    read(101,'(A)',IOSTAT=NI) cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    print *,'Error locate at steps:',J,'atoms:',J2
    goto 330
    end if 
    CALL StripSpaces(cFile1)
    !There are comma in the data
    read(cFile1,*) all_result(K)%Forces(J,J2,:)
    ENDDO
    ENDDO
    print *,'Finish reading forces form file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    TT=.False.
    else
    ! DO NOTHING
    end if 
    
    
    ENDDO
    close(101)
    close(102)
! Reading the energy    
! Energy can be obtained from other files
open(unit=101,file='TES_fit_diff_energy_'//Trim(adjustL(cFile_name))//'.dat')
DO J=1,num_of_steps
read(101,*) Energy_temp

if (K==1)then
 all_result(K)%Energy(J)=Energy_temp(4)
else 
 all_result(K)%Energy(J)=Energy_temp(2)
end if
ENDDO
close(101)
! Reading the Stress    
    open(unit=101,file=''//Trim(adjustL(cFile_name))//'_HIST.nc')
    open(unit=102,file='output.txt')
    TT=.TRUE.
    DO while(TT)
    read(101,'(A)',IOSTAT=NI) cFile1
    !print *,cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    !print *,cFile1
    exit 
    end if 
    cFile2=cFile1(1:8)
    !write(102,'(A)') cFile2
    if (cFile2==cFile4)then
        !print *,'HERE'
    DO J=1,num_of_steps
    
    write(102,*) J,J2
    read(101,'(A)',IOSTAT=NI) cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    print *,'Error locate at steps:',J
    goto 330
    end if 
    CALL StripSpaces(cFile1)
    !There are comma in the data
    if (K==1)then
    read(cFile1,*) all_result(K)%Stress(J,1:3)
    else
    goto 340
    end if 
    
    read(101,'(A)',IOSTAT=NI) cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    print *,'Error locate at steps:',J
    goto 330
    end if 
    CALL StripSpaces(cFile1)
    !There are comma in the data
    

    if (K==1)then
    read(cFile1,*) all_result(K)%Stress(J,4:6)
    end if 
  
    ENDDO
    print *,'Finish reading stresses from file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    TT=.False.
    else
    ! DO NOTHING
    end if 
    ENDDO
    close(101)
    close(102)
ENDDO

!额外处理DFT计算出来的Stress
340 continue
all_result(2)%Stress(:,:)=0
open(unit=109,file='TES_fit_diff_stress.dat')
DO I=1,num_of_steps
read(109,*) Tee
all_result(2)%Stress(I,1:6)=Tee(2:7)
ENDDO
close(109)
! Finish reading all the files
! Start calculation
! F=F-F(0)

DO I=1,num_of_terms
    K=I+1
    all_result(K)%Forces=all_result(K)%Forces-all_result(1)%Forces
    all_result(K)%Stress=all_result(K)%Stress-all_result(1)%Stress
    all_result(K)%Energy=all_result(K)%Energy-all_result(1)%Energy
  
ENDDO

! Only Phi in all_result(1) is calculated
!所有的信息存储在all_result(2)%XXX里面
!    ALLOCATE(all_result(K)%Forces(num_of_steps,num_of_atoms,3))
!    ALLOCATE(all_result(K)%Stress(num_of_steps,6)) 
!    ALLOCATE(all_result(K)%Energy(num_of_steps)) 

open(unit=108,file='Y.txt')
DO I=1,num_of_steps
  !  print *,'Running Here'
  !  print *,J 
  !  print *,num_of_atoms
DO J=1,num_of_atoms

write(108,*) all_result(2)%Forces(I,J,1)
write(108,*) all_result(2)%Forces(I,J,2)
write(108,*) all_result(2)%Forces(I,J,3)
ENDDO
DO J=1,6
write(108,*) all_result(2)%Stress(I,J)
ENDDO
write(108,*) all_result(2)%Energy(I)
ENDDO
close(108)

open(unit=109,file='Y_energy.txt')
DO I=1,num_of_steps
   write(109,*) all_result(2)%Energy(I) 
ENDDO
close(109)
330 continue

print *,'Finished, Press any key to continue'
read(*,*) 

contains
!StripSpaces delete all the comma in a string

    subroutine StripSpaces(string)
    character(len=512) :: string
    integer :: stringLen 
    integer :: last, actual

    stringLen = len (string)
    !print *,stringLen
    last = 1
    actual = 1
    
    DO actual=1,stringLen
       if (string(actual:actual) == ',') then
        string(actual:actual)=' '
        endif
    
    ENDDO
    do while (actual < stringLen)

    end do

    end subroutine



end program main