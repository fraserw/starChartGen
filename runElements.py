import glob,os,sys,numpy as np,pylab as pyl,ephem as eph
import mp_ephem



def ephFileEntry(dateStr,mjd,r,d,dRACOSDec,dDec):
#***************************************************************************************
# Date__(UT)__HR:MN Date_________JDUT     R.A.___(ICRF/J2000.0)___DEC dRA*cosD d(DEC)/dt
#***************************************************************************************
#$$SOE
# 2013-Jan-10 16:00 2456303.166666667 Am  14 33 46.4393 -12 34 07.967 10.42232  -3.30518
#$$EOE
#***************************************************************************************

    dateEntry=dateStr.split('.')[0].replace('/','-').replace('-08-','-Aug-').replace('-09-','-Sep-').replace('-10-','-Oct-').replace('-11-','-Nov-').replace('-12-','-Dec-').replace('-01-','-Jan-').replace('-02-','-Feb-').replace('-03-','-Mar-').replace('-04-','-Apr-').replace('-05-','-May-').replace('-06-','-Jun-').replace('-07-','-Jul-')

    x=float(dateStr.split('/')[2])
    x-=int(x)
    x*=24.
    hourEntry=int(x*10000000+0.5)/10000000.
    minuteEntry=int(60*(hourEntry-int(hourEntry)))
    hourEntry=int(hourEntry)
    #hourEntry=float(dateStr.split('/')[2])
    #hourEntry-=int(hourEntry)
    #hourEntry*=24.
    #hour=int(hourEntry+0.5)
    #minute=int((hourEntry-hour)*60)

    if hourEntry<10:
        hourEntry='0'+str(hourEntry)
    else:
        hourEntry=str(hourEntry)
    if minuteEntry<10:
        hourEntry+=':0'+str(minuteEntry)
    else:
        hourEntry+=':'+str(minuteEntry)

    jdEntry=str(mjd+2400000.5)[:17].ljust(17)

    rEntry=r.replace(':',' ').ljust(13)
    if d<0:
        dEntry=('-'+d.replace(':',' ')).ljust(13)
    else:
        dEntry=(' '+d.replace(':',' ')).ljust(13)

    out=' %s %s %s Am  %s %s %1.5f %1.5f'%(dateEntry,hourEntry,jdEntry,rEntry,dEntry,dRACOSDec,dDec)
    #print out
    if hourEntry==24:
        print dateStr
    return out

def convDate(dateStr):
    date=eph.date(dateStr)
    return date+15019.5


def radStr(r,d):
    x=r/15.
    if x<10:
        rh='0'+str(int(x))
    else:
        rh=str(int(x))
    x-=int(x)
    x*=60.
    if x<10:
        rm='0'+str(int(x))
    else:
        rm=str(int(x))
    x-=int(x)
    x*=60.
    if x<=10:
        rs='0'+str(x)[:5]
    else:
        rs=str(x)[:6]

    s=np.sign(d)
    if abs(d)<10:
        dh='0'+str(int(s*int(d)))
    else:
        dh=str(int(s*int(d)))
    d=abs(d)
    d-=int(d)
    d*=60
    if d<10:
        dm='0'+str(int(d))
    else:
        dm=str(int(d))
    d-=int(d)
    d*=60.
    if d<10:
        ds='0'+str(d)[:4]
    else:
        ds=str(d)[:5]

    if s<0:
        return (":".join([rh,rm,rs]),'-'+":".join([dh,dm,ds]))
    else:
        return (":".join([rh,rm,rs]),":".join([dh,dm,ds]))



files=['mpcs/o5c016.mpc'
       ]


dates=[]
mjds=[]
months=range(1,13)
daysInaMonth=[31,28,31,30,31,30,31,31,30,31,30,31]

for t in range(8,12):
    if months[t]<10:
        mon='0'+str(months[t])
    else:
        mon=str(months[t])
    for i in range(1,daysInaMonth[t]+1):
        #midnight is 10 UT. So go from +- 7 hours of midnight, or 3 to 17 UT
        for j in range(3,17,1): #every 1 hour
            day=i+j/(24.)
            if day<10:
                dates.append('2018/%s/0%s'%(mon,day))
            else:
                dates.append('2018/%s/%s'%(mon,day))
            mjds.append(convDate(dates[len(dates)-1]))

for t in range(0,1):
    if months[t]<10:
        mon='0'+str(months[t])
    else:
        mon=str(months[t])
    for i in range(1,daysInaMonth[t]+1):
        #midnight is 10 UT. So go from +- 7 hours of midnight, or 3 to 17 UT
        for j in range(3,17,1): #every 1 hour
            day=i+j/(24.)
            if day<10:
                dates.append('2019/%s/0%s'%(mon,day))
            else:
                dates.append('2019/%s/%s'%(mon,day))
            mjds.append(convDate(dates[len(dates)-1]))

outhan=open('ephemerides_2019A.txt','w+')

showDiscoveryLines=False

objs={}
for i in files:
    xxx=i.split('.')

    if len(xxx)==2 and 'Col' not in xxx[0]:
        n=xxx[0]
        end='mpc'
    elif len(xxx)==2 and 'Col' in xxx[0]:
        n=xxx[0]
        end='mpc'
    elif len(xxx)==2 and 'p' in xxx[0]:
        n=xxx[0]
        end='mpc'
    elif 'O15B' in xxx[0]:
        end='mpc'
    else:
        n=xxx[0]+'.'+xxx[1]
        end='ast'



    #clean the mpc files of any bad entries
    with open(n+'.'+end) as han:
        data=han.readlines()
    observations=[]
    for k in range(len(data)):
        if not data[k][0]=='!' and ' 304' not in data[k] and ' 662' not in data[k]:
            date = data[k][15:31]
            s = data[k][31:44].split()
            ra = 15.0*(float(s[0]) + float(s[1])/60.0 + float(s[2])/3600.0)
            s = data[k][44:57].split()
            dec = abs(float(s[0])) + float(s[1])/60.0 + float(s[2])/3600.0
            if '-' in s[0]: dec *= -1.0
            obscode = data[k].split()[-1]

            observation = mp_ephem.ephem.Observation(ra=ra, dec=dec, date=date, observatory_code=obscode)
            observations.append(observation)

    orb=mp_ephem.BKOrbit(observations)
    observations=np.array(observations)


    if 1:#m<=23.6 and n.split('/')[-1] and n>0:


        s=n.split('.')[0].split('/')
        shortn=s[len(s)-1]
        geminiOutHan=open('ephs/'+shortn+'.eph','w+')
        print >> geminiOutHan,'***************************************************************************************'
        print >> geminiOutHan,' Date__(UT)__HR:MN Date_________JDUT     R.A.___(ICRF/J2000.0)___DEC dRA*cosD d(DEC)/dt'
        print >> geminiOutHan,'***************************************************************************************'
        print >> geminiOutHan,'$$SOE'


        print "{}".format(shortn),

        R=[]
        D=[]
        xxx=n.split('/')
        print >> outhan, xxx[len(xxx)-1]
        for j in range(len(dates)-1):
            orb.predict(mjds[j]+2400000.5)
            r,d=orb.coordinate.ra.degree,orb.coordinate.dec.degree
            orb.predict(mjds[j]+2400000.5+1.0/24.0)
            rr,dd=orb.coordinate.ra.degree,orb.coordinate.dec.degree
            ea=orb.dra.value
            eb=orb.ddec.value
            ang=orb.pa.value

            R.append(r)
            D.append(d)
            (rs,ds)=radStr(r,d)
            dra=(rr-r)*np.cos(d*np.pi/180.)*3600.
            ddec=(dd-d)*3600.
            if (mjds[j+1]-mjds[j])*24.>1:
                dra/=24*(mjds[j+1]-mjds[j])
                ddec/=24*(mjds[j+1]-mjds[j])
            print >>outhan,'%s %12.6f %s %s %4.6f %4.6f %1.3f %1.3f %1.3f %1.5f %1.5f'%(dates[j][:14].ljust(15),mjds[j],rs,ds,r,d,ea,eb,ang,dra,ddec)
            print >> geminiOutHan,ephFileEntry(dates[j],mjds[j],rs,ds,dra,ddec)

            #if j==0: print "{:.5f} {:.5f}".format(r,d)

        R = np.array(R)
        D = np.array(D)
        print np.min(R),np.max(R),np.min(D),np.max(D)
        pyl.plot(R,D)
        print >> outhan

        print >> geminiOutHan,'$$EOE'
        print >> geminiOutHan,'***************************************************************************************'
        geminiOutHan.close()
outhan.close()

pyl.show()
