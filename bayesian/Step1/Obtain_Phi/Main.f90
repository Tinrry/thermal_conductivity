Program main
use gloable
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
LOGICAL TT
print *,'number of terms?'
read(*,*) num_of_terms
print *,''
print *,'number of atoms?'
read(*,*) num_of_atoms
print *,''
print *,'number of steps?'
read(*,*) num_of_steps
print *,''

!open(unit=101,file='Guiyihua.txt')
!read(101,*) Guiyihua_Energy
!read(101,*) Guiyihua_Stress
!read(101,*) Guiyihua_Force
!close(101)

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
 all_result(K)%Energy(J)=Energy_temp(4)
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
    read(cFile1,*) all_result(K)%Stress(J,1:3)
    
    read(101,'(A)',IOSTAT=NI) cFile1
    if (NI/=0)then
    print *,'Error in reading file:',''//Trim(adjustL(cFile_name))//'_HIST.nc'
    print *,'Error locate at steps:',J
    goto 330
    end if 
    CALL StripSpaces(cFile1)
    !There are comma in the data
    read(cFile1,*) all_result(K)%Stress(J,4:6)
    
  
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
ALLOCATE(all_result(1)%Phi(num_of_steps,3*num_of_atoms+7,num_of_terms))
! order in Force, Stress, Energy
all_result(1)%Phi=0.0
open(unit=108,file='Forces.txt')
Max_Force=0.0
DO I=1,num_of_steps
DO J=1,num_of_atoms
DO K=1,num_of_terms
    L=K+1
    !write(108,*) all_result(L)%Forces(I,J,:)

if (abs(all_result(L)%Forces(I,J,1))>=Max_Force)then
Max_Force=abs(all_result(L)%Forces(I,J,1))
end if 

if (abs(all_result(L)%Forces(I,J,2))>=Max_Force)then
Max_Force=abs(all_result(L)%Forces(I,J,2))
end if 

if (abs(all_result(L)%Forces(I,J,3))>=Max_Force)then
Max_Force=abs(all_result(L)%Forces(I,J,3))
end if 

ENDDO
ENDDO
ENDDO
write(108,*) 'Max_Force',Max_Force
close(108)


Max_Stress=0.0
open(unit=108,file='Stress.txt')
DO I=1,num_of_steps
DO J=1+3*num_of_atoms,6+3*num_of_atoms
DO K=1,num_of_terms
    L=K+1
!write(108,*) all_result(L)%Stress(I,J-3*num_of_atoms)
 if (abs(all_result(L)%Stress(I,J-3*num_of_atoms))>=Max_Stress) then
 Max_Stress=abs(all_result(L)%Stress(I,J-3*num_of_atoms))
 end if 

ENDDO
ENDDO
ENDDO
write(108,*) 'Max_Stress',Max_Stress
close(108)
open(unit=108,file='Energy.txt')
Max_Energy=0
DO I=1,num_of_steps
J=7+3*num_of_atoms
DO K=1,num_of_terms
    L=K+1
 if (abs(all_result(L)%Energy(I))>=Max_Energy) then
 Max_Energy=abs(all_result(L)%Energy(I))
 end if 
ENDDO
ENDDO
write(108,*) 'Max_energy',Max_Energy

close(108)
!获得归一化的系数
Guiyihua_Energy=Max_Energy
Guiyihua_Stress=Max_Stress
Guiyihua_Force=Max_Force
!将归一化的系数待会到Phi中

DO I=1,num_of_steps
DO J=1,num_of_atoms
DO K=1,num_of_terms
    L=K+1
all_result(1)%Phi(I,3*(J-1)+1,K)=all_result(1)%Phi(I,3*(J-1)+1,K)+(all_result(L)%Forces(I,J,1))/Guiyihua_Force
all_result(1)%Phi(I,3*(J-1)+2,K)=all_result(1)%Phi(I,3*(J-1)+2,K)+(all_result(L)%Forces(I,J,2))/Guiyihua_Force
all_result(1)%Phi(I,3*(J-1)+3,K)=all_result(1)%Phi(I,3*(J-1)+3,K)+(all_result(L)%Forces(I,J,3))/Guiyihua_Force

ENDDO
ENDDO
ENDDO

DO I=1,num_of_steps
DO J=1+3*num_of_atoms,6+3*num_of_atoms
DO K=1,num_of_terms
    L=K+1
all_result(1)%Phi(I,J,K)=all_result(1)%Phi(I,J,K)+(all_result(L)%Stress(I,J-3*num_of_atoms))/Guiyihua_Stress
ENDDO
ENDDO
ENDDO

DO I=1,num_of_steps
J=7+3*num_of_atoms
DO K=1,num_of_terms
    L=K+1
all_result(1)%Phi(I,J,K)=all_result(1)%Phi(I,J,K)+(all_result(L)%Energy(I))/Guiyihua_Energy
!all_results(1) is the reference state, it's not the results!
ENDDO
ENDDO

!Now you have Phi all_result(1)%Phi(number_of_steps,7+3*number_of_atoms,number_of_terms)
open(unit=104,file='Phi.txt')
DO I=1,num_of_steps
DO J=1,7+3*num_of_atoms
write(104,*) all_result(1)%Phi(I,J,:)
ENDDO
ENDDO
close(104)


Phi_sing_phi=0.0
Phi_phi=0.0
!Calculate Phi_phi
DO I=1,num_of_terms
DO J=1,num_of_terms
DO K=1,7+3*num_of_atoms
DO L=1,num_of_steps
Phi_phi(I,J)=Phi_phi(I,J)+all_result(1)%Phi(L,K,I)*all_result(1)%Phi(L,K,J)
ENDDO
ENDDO
ENDDO
ENDDO
!Output Phi_phi
open(unit=108,file='Phi_phi.txt')
DO I=1,num_of_terms
write(108,*) Phi_phi(I,:)
ENDDO
close(108)



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