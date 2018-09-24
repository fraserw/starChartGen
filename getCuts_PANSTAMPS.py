import os
import numpy as np
import sys


targ = 'o5s52'
if len(sys.argv)>1:
    targ = sys.argv[1]

os.system('mkdir {}'.format(targ))

with open('ephs/{}.eph'.format(targ)) as han:
    data = han.readlines()

r = []
d = []
for i in range(4,len(data)-2):
    s = data[i].split()
    r.append(15.0*( float(s[4]) + float(s[5])/60.0 + float(s[6])/3600.0))
    d.append(( abs(float(s[7])) + float(s[8])/60.0 + float(s[9])/3600.0))
    if '-' in s[7]:
        d[-1] *= -1.0


r = np.array(r)
d = np.array(d)

ras = np.arange(np.min(r),np.max(r),0.1)
decs = np.arange(np.min(d),np.max(d),0.1)

rs = np.array([])
ds = np.array([])
for i in range(len(ras)):
    for j in range(len(decs)):
        R = ras[i]
        D = decs[j]
        for dr in [-0.2,-0.0,0.2]:
            for dd in [-0.2,-0.0,0.2]:
                if len(rs)>0:
                    d = ( (np.cos((D+dd)*np.pi/180.)*(rs-(R+dr)))**2 + (ds-(D+dd))**2)**0.5
                    if np.min(d)*50.0>4.0:#is the centre of the image more than 5 arcsecsonds away?
                        rs = np.insert(rs,len(rs),R+dr)
                        ds = np.insert(ds,len(ds),D+dd)
                        #print rs,ds
                else:
                    rs = np.array([R+dr])
                    ds = np.array([D+dd])
                    #print rs,ds,'&'
n = 1
for i in range(len(rs)):
    R = rs[i]
    D = ds[i]
    comm = 'panstamps --width=15 --filters=r --downloadFolder=./{}/ stack {} {}'.format(targ,R,D)
    print 'Getting image {} of {}.'.format(n,len(rs))
    print comm
    os.system(comm)

    n+=1
