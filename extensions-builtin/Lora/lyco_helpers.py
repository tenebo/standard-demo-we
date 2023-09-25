import torch
def make_weight_cp(t,wa,wb):A=torch.einsum('i j k l, j r -> i r k l',t,wb);return torch.einsum('i j k l, i r -> r j k l',A,wa)
def rebuild_conventional(up,down,shape,dyn_dim=None):
	C=dyn_dim;B=down;A=up;A=A.reshape(A.size(0),-1);B=B.reshape(B.size(0),-1)
	if C is not None:A=A[:,:C];B=B[:C,:]
	return(A@B).reshape(shape)
def rebuild_cp_decomposition(up,down,mid):A=down;up=up.reshape(up.size(0),-1);A=A.reshape(A.size(0),-1);return torch.einsum('n m k l, i n, m j -> i j k l',mid,up,A)