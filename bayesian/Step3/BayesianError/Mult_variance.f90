program main
use Zichengxu
implicit none 
INTEGER(8) I,num_of_steps,J,num_of_term,CHECK
REAL(8) PA2(127,127),PA22(127,127)
REAL(8) Zhuyuan(127)
REAL(8),allocatable :: MAX_result(:),Sigma(:,:),Phi_now(:,:),PA1(:,:),Phi_now_T(:,:)
REAL(8),allocatable :: PA12(:,:)
!REAL(8),allocatable :: Sum_result(:)
INTEGER(8) L1,L2,L3
print *,'number of steps?'
read(*,*) num_of_steps
print *,''

print *,'number of term?'
read(*,*) num_of_term
print *,''

ALLOCATE(MAX_result(num_of_steps))
!ALLOCATE(Sum_result(num_of_steps))
ALLOCATE(Sigma(num_of_term,num_of_term))
ALLOCATE(Phi_now(127,num_of_term))
ALLOCATE(PA1(127,num_of_term))
ALLOCATE(PA12(127,num_of_term))
ALLOCATE(Phi_now_T(num_of_term,127))
MAX_result=-1
!Sum_result=-1
!-1是初始值，由于所有的主元都会求绝对值，因此正常的MAX_result一定是正的
Sigma=0
open(unit=101,file='variance.csv')
DO I=1,num_of_term
read(101,*) Sigma(I,:)
ENDDO
close(101)

!根据Phi来进行计算
!读入的Phi可能会有非常多步，但没关系，读就是了
!Phi是N*127*48的矩阵 
open(unit=102,file='Phi.txt')
DO I=1,num_of_steps
    Phi_now=0
    !初始化当前的Phi
DO J=1,127
read(102,*) Phi_now(J,:)
ENDDO
!Reverse Phi_now
DO L1=1,127
DO L2=1,num_of_term
Phi_now_T(L2,L1)=Phi_now(L1,L2)
ENDDO
ENDDO

CALL Mul_matrix2(Phi_now,Sigma,PA1)
PA12=matmul(Phi_now,Sigma)
!print *,SIZE(PA1,dim=1),SIZE(PA1,dim=2)
!print *,SIZE(Phi_now_T,dim=1),SIZE(Phi_now_T,dim=2)
!print *,SIZE(PA2,dim=1),SIZE(PA2,dim=2)
CHECK=1999
CALL Mul_matrix2(PA1,Phi_now_T,PA2)
open(unit=106,file='PA22.dat')
PA22=matmul(PA12,Phi_now_T)
DO L3=1,127
Zhuyuan(L3)=PA22(L3,L3)
ENDDO
!先写到这里吧，Zhuyuan求完了，下一步就是下一步的事了
!要求每一个step的max主元的值
Zhuyuan=abs(Zhuyuan)
MAX_result(I)=maxval(Zhuyuan(:))
!Sum_result(I)=sum(Zhuyuan)
if (I==1)then
open(unit=105,file='zhuyuan.dat')
DO L3=1,127
write(105,*) Zhuyuan(L3)
write(105,*) MAX_result(I)

ENDDO
close(105)
end if 
ENDDO
close(102)



open(unit=103,file='result.dat')
open(unit=104,file='sum_result.dat')
DO I=1,num_of_steps
write(103,*) I,MAX_result(I)
!write(104,*) I,Sum_result(I)
    
ENDDO
close(103)
close(104)

end program main

