module gloable
implicit none
private
type,public ::manager
!Forces (time,atom,xyz)
REAL(8),allocatable :: Forces(:,:,:)
REAL(8),allocatable :: Energy(:)
REAL(8),allocatable :: Stress(:,:)
REAL(8),allocatable :: Phi(:,:,:)




end type manager




end module gloable