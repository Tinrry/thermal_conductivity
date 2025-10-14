Module Zichengxu
implicit none 

contains
SUBROUTINE Mul_matrix(A,B,C)
implicit none 
REAL(8),dimension(:,:) :: A,B,C

INTEGER(8) M_i,M_j,M_k
INTEGER(8) SizA,SizB,SizC

SizA=SIZE(A,dim=1)
SizB=SIZE(A,dim=2)
SizC=SIZE(B,dim=2)
C=0

open(unit=11,file='OUTPUT')
DO M_i=1,SizA
DO M_j=1,SizB
DO M_k=1,SizC
C(M_i,M_j)=C(M_i,M_j)+A(M_i,M_k)*B(M_k,M_i)
ENDDO
ENDDO
ENDDO
close(11)


END SUBROUTINE Mul_matrix


SUBROUTINE Mul_matrix2(A,B,C)
implicit none 
REAL(8),dimension(:,:) :: A,B,C
INTEGER(8) M_i,M_j,M_k
INTEGER(8) SizA,SizB,SizC

SizA=SIZE(A,dim=1)
SizB=SIZE(A,dim=2)
SizC=SIZE(B,dim=2)
C=0
  ! print *, SizA,SizB,SIZE(B,dim=1),SizC
!open(unit=11,file='OUTPUT')
DO M_i=1,SizA
DO M_j=1,SizC
DO M_k=1,SizB
  !  print *, M_i,M_j,M_k
C(M_i,M_j)=C(M_i,M_j)+A(M_i,M_k)*B(M_k,M_i)
ENDDO
ENDDO
ENDDO
!close(11)


END SUBROUTINE Mul_matrix2


SUBROUTINE Multi_matrix(A,B,C)
implicit none 
!一个127*48的矩阵和一个48*48的矩阵乘法
REAL(8) A(127,48),C(127,48)
REAL(8) B(48,48)
INTEGER(8) M_i,M_j,M_k
C=0
DO M_i=1,127
DO M_j=1,48
DO M_k=1,48
C(M_i,M_j)=C(M_i,M_j)+A(M_i,M_k)*B(M_k,M_j)
ENDDO
ENDDO
ENDDO


END SUBROUTINE


SUBROUTINE Multi_matrix2(A,B,C)
implicit none 
!一个127*48的矩阵和一个48*127的矩阵乘法
REAL(8) A(127,48),C(127,127)
REAL(8) B(48,127)
INTEGER(8) M_i,M_j,M_k
C=0
DO M_i=1,127
DO M_j=1,127
DO M_k=1,48
C(M_i,M_j)=C(M_i,M_j)+A(M_i,M_k)*B(M_k,M_j)
ENDDO
ENDDO
ENDDO


END SUBROUTINE

END Module Zichengxu 