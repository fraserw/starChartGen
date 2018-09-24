#! /usr/bin/env pythonw

import sys,numpy as np, pylab as pyl
import astropy.io.fits as fits
from astropy import wcs
#import orbfit_pyephem as orbfit
from stsci import numdisplay
from astropy.visualization import interval
import mp_ephem
import ephem as eph

def convDate(dateStr):
    date=eph.date(dateStr)
    return date+15019.5


def selector(event):
    global fig,shownDates,i,hours,sp1,sp2,outHan,ra_uncert,dec_uncert
    if event.key == 'q':
        outHan.close()
        exit()

    if event.key == 'g':
        print shownDates[0].split('.')[0].replace('/','-')+'  {}:00:00  {}:00'.format(hours[0],hours[-1]-hours[0])#04:00:00  14:00'
        print >>outHan,shownDates[0].split('.')[0].replace('/','-')+'  04:00:00  14:00'
        outHan.flush()

    if event.key in ['g','b']:

        sp1.cla()
        sp2.cla()

        i+=len(hours)
        if i>=len(pix):
            print '   Finishing.'
            pyl.close()
            return

        shownDates = dates[i:i+len(hours)]
        (a,b,c,d) = getLim(pix,i,dispSize)

        sp1.imshow(getSec(data,pix,i,dispSize),interpolation='nearest',origin=0)
        sp2.imshow(getSec(data,pix,i,dispSize*3),interpolation='nearest',origin=0)
        sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a,'k-o',lw=3,alpha=0.5)
        sp1.plot(pix[i:i+len(hours),0]-c-ra_uncert,pix[i:i+len(hours),1]-a,'w-',lw=3,alpha=0.5)
        sp1.plot(pix[i:i+len(hours),0]-c+ra_uncert,pix[i:i+len(hours),1]-a,'w-',lw=3,alpha=0.5)
        sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a-dec_uncert,'w-',lw=3,alpha=0.5)
        sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a+dec_uncert,'w-',lw=3,alpha=0.5)
        sp1.text(pix[i,0]-c+10,pix[i,1]-a-20,dates[i])
        sp1.set_xlim(0,d-c)
        sp1.set_ylim(0,b-a)
        sp1.set_title(shownDates[0])

        pyl.draw()

def getSec(data,pix,i,ds):
    global normer

    (a,b,c,d) = getLim(pix,i,ds)
    dat=data[a:b,c:d]
    return normer(dat)

def getLim(pix,i,ds):
    (a,b,c,d)=(np.min(pix[i:i+len(hours),1])-ds,
               np.max(pix[i:i+len(hours),1])+ds,
               np.min(pix[i:i+len(hours),0])-ds,
               np.max(pix[i:i+len(hours),0])+ds)
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    return (a,b,c,d)


locale = 'Arizona'
if len(sys.argv)>1:
    if '-h' in sys.argv:
        print 'usage observabilityCheck.py target locale'
        print 'locale can be Arizona or Hawaii, default Arizona. Sets the UT times to'
        print 'display ephemerides tracks for.'
        print 'eg. observabilityCheck.py o5c016 Hawaii'
        exit()
    if len(sys.argv)>2:
        locale = sys.argv[2]

dispSize = 250

dates=[]
mjds=[]
months=range(1,13)
daysInaMonth=[31,28,31,30,31,30,31,31,30,31,30,31]
if locale == 'Hawaii':
    hours = [4,6,8,10,12,14]
    for t in range(2,3):
        if months[t]<10:
            mon='0'+str(months[t])
        else:
            mon=str(months[t])
        for i in range(1,daysInaMonth[t]+1):

            #midnight is 10 UT. So go from +- 7 hours of midnight, or 3 to 17 UT
            for j in hours: #every 1 hour
                day=i+j/(24.)
                if day<10:
                    dates.append('2018/%s/0%s'%(mon,day))
                else:
                    dates.append('2018/%s/%s'%(mon,day))
elif locale == 'Arizona':
    #in Arizona, timezone is +2 UTC.
    #So sunset local time is 17:50, sunset UTC is 15:50
    #Sunrise local time is 6:08, sunrise UTC is 4:08
    #so go from 17 to 27 hours, which is an hour after/before sunset/sunrise
    hours = np.linspace(3,11,6)
    for t in range(9,10):
        if months[t]<10:
            mon='0'+str(months[t])
        else:
            mon=str(months[t])
        for i in range(1,daysInaMonth[t]+1):

            #delete two lines below
            print 'hacking dates for 2018B LBT run'
            if i<9 or i>13: continue

            #midnight is 10 UT. So go from +- 7 hours of midnight, or 3 to 17 UT
            for j in hours: #every 1 hour
                day=i+j/(24.)
                if day<10:
                    dates.append('2018/%s/0%s'%(mon,day))
                else:
                    dates.append('2018/%s/%s'%(mon,day))


#clean the mpc files of any bad entries
with open('mpcs/{}.mpc'.format(sys.argv[1])) as han:
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

orb = mp_ephem.BKOrbit(observations)
observations=np.array(observations)


if locale == 'Hawaii':
    with fits.open(sys.argv[1]+'.fits') as han:
        w = wcs.WCS(han[0].header)
        data=han[0].data

    outHan = open(sys.argv[1]+'.tw','w+')
    #orb=orbfit.Orbfit(filename='mpcs/{}.mpc'.format(sys.argv[1]),file_format='mpc')
    obs_code = 568

elif locale == 'Arizona':
    with fits.open(sys.argv[1]+'.fits') as han:
        w = wcs.WCS(han[0].header)
        data=han[0].data

    outHan = open(sys.argv[1]+'.tw','w+')
    #orb=orbfit.Orbfit(filename='mpcs/{}.mpc'.format(sys.argv[1]),file_format='mpc')
    obs_code = 290

#orb.predict('2016/06/01.5')
sky=[]
u_sky = []
for i in range(len(dates)):
    mjd = convDate(dates[i])
    #orb.predict(dates[i],obs_code=obs_code)
    orb.predict(mjd+2400000.5,obs_code=obs_code)
    sky.append([orb.coordinate.ra.degree,orb.coordinate.dec.degree])
    u_sky.append([orb.dra.value,orb.ddec.value])
    print dates[i],sky[-1][0],sky[-1][1],u_sky[-1][0],u_sky[-1][1]

u_sky = np.array(u_sky)
ra_uncert = int(np.max(u_sky[:,0])/0.25 + 0.5)
dec_uncert = int(np.max(u_sky[:,1])/0.25 + 0.5)

pix = np.array(w.wcs_world2pix(np.array(sky),1))
print
print


(a,b,c,d) = (np.min(pix[:,1])-dispSize,np.max(pix[:,1])+dispSize, np.min(pix[:,0])-dispSize,np.max(pix[:,0])+dispSize)
a = int(a)
b = int(b)
c = max(0,int(c))
d = int(d)
print a,b,c,d

dat = data[a:b,c:d]
w = np.where(np.isnan(dat))
dat[w] = np.nanmedian(dat)

if dat==[]:
    print 'Off chip!'
    sys.exit()

(z1,z2) = numdisplay.zscale.zscale(dat,contrast=0.1)
print z1,z2,'z'
normer = interval.ManualInterval(z1,z2)

fig1 = pyl.figure(1,figsize=(15,9)) #(30,15) for big screen
sp1=fig1.add_subplot(121)
sp2=fig1.add_subplot(122)

i=0
shownDates = dates[i:i+len(hours)]
print shownDates[0]
print '\n\n\n\n\n'

(a,b,c,d) = getLim(pix,i,dispSize)
sp1.imshow(getSec(data,pix,i,dispSize),interpolation='nearest',origin=0)
sp2.imshow(getSec(data,pix,i,dispSize*3),interpolation='nearest',origin=0)
sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a,'k-o',lw=3,alpha=0.5)
sp1.plot(pix[i:i+len(hours),0]-c-ra_uncert,pix[i:i+len(hours),1]-a,'w-',lw=3,alpha=0.5)
sp1.plot(pix[i:i+len(hours),0]-c+ra_uncert,pix[i:i+len(hours),1]-a,'w-',lw=3,alpha=0.5)
sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a-dec_uncert,'w-',lw=3,alpha=0.5)
sp1.plot(pix[i:i+len(hours),0]-c,pix[i:i+len(hours),1]-a+dec_uncert,'w-',lw=3,alpha=0.5)
sp1.text(pix[i,0]-c+10,pix[i,1]-a-20,dates[i])
sp1.set_xlim(0,d-c)
sp1.set_ylim(0,b-a)
sp1.set_title(shownDates[0])
pyl.connect('key_press_event',selector)
pyl.show()
