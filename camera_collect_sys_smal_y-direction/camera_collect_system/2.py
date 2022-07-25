import numpy as np
a=[80,100,200,300]
a=np.array(a)
b=np.where(a>200)
print(b)
b=np.sum(a>100)
print(b)
c=a-100
c[c<0]=0
print(c)
print(np.sum(c))