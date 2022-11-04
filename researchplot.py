#plot mcmc sampling histories for Gaia WDS sample
%reset-f #ask Sarah what the help plot_sampling_batch;

import sys
import time
import os
import re
import pandas
import numpy
import matplotlib.pyplot as plt

filename = sys.argv[1]
def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)

tic
os.chdir('mcmc.0001/') #not defined, find the python equivalent
counter = 0
stars = dir('*.wd.all') #ask Sarah about if this methods are written the same in matlab as python
#ll: logAge FeH parallax absorption logPost stage mass logTeff logg coolingAge precLogAge
for st in range len(stars)
    print('Working on ', st, 'of ', len(stars), ': ', stars(st).name)
    #grab EDR3 parallax values out of file name (possible could be done w np.loadtxt() based off stats_sampleWDMass.py
    pattern       = '.wd.all'
    replacement   = ''
    S             = re.sub(pattern, replacement, stars(st).name)

    outfile       = 'sampling.' + S + '.jp'

    pattern       = '.Av'
    tempA         = re.sub(pattern, replacement, S)

    pattern       = '.eplx.'
    replacement   =' '
    tempB         = re.sub(pattern, replacement, tempA)
    pattern       = '.plx.'
    tempC         = re.sub(pattern, replacement, tempB)
    pattern       = '.wd.'
    tempD         = re.sub(pattern, replacement, tempC)
    pattern       = '.asDA'
    tempE         = re.sub(pattern, replacement, tempD)
    pattern       = '.asDB'
    tempF         = re.sub(pattern, replacement, tempE)

    starParams    = float(tempF)
    starName      = starParams(1)
    starSpT       = starParams(2)
    starPrlx      = 10**(-3) * starParams(3)
    starPrlx_e    = 10**(-3) * starParams(4)

    starPrlx3p    = starPrlx + 3 * starPrlx_e
    starPrlx3n    = starPrlx - 3 * starPrlx_e

    print(' EDR3 Star params: name=', starName, ' SpT=', format(starSpT,".1f"), 'prlx=', format(10**(3)*starPrlx,".2f"), 'mas eprlx=', format(10**(3)*starPrlx_e, ".2f"), 'mas/n')
    #read in BASE-9 singlePopMcmc + sampleWDMass file

    #unsure about open() vs. importdata()
    sample  = numpy.loadtxt(stars(st).name, ' ')

logAge_all      = sample[:,0]
fe_h_all        = sample[;,1]
parallax_all    = sample[:,2]
absorb_all      = sample[:,3]
logPost_all     = sample[:,4]
stage_all       = sample[:,5]
mass_all        = sample[:,6]
logT_all        = sample[:,7]
logg_all        = sample[:,8]
coolingAge_all  = sample[:,9]
precLogAge_all  = sample[:,10]

N_full_len      = len(logAge)
iteration       = 1:N_full_len

#dont plot burn in
ind        = numpy.where(stage == 3)
logAge     = logAge_all[ind]
fe_h       = fe_h_all[ind]   
parallax   = parallax_all[ind]
absorb     = absorb_all[ind]
logPost    = logPost_all[ind]
stage      = stage_all[ind]
mass       = mass_all[ind]
logT       = logT_all[ind]
logg       = logg_all[ind]
coolingAge = coolingAge_all[ind]
precLogAge = precLogAge_all[ind]

iter_run   = iteration[ind]
#for plotting, determine which iterations outside +-3 EDR3 parallax sigma
k = 1
hold_array = []
for k in range(len(ind)) :
    if parallax(k) <= starPrlx3p and parallax(k) >= starPrlx3n:
        hold_array.append(k) 
        
    if k > 1:
        logAge_hold     = numpy.take(logAge, hold_array)
        fe_h_hold       = numpy.take(fe_h, hold_array)
        parallax_hold   = numpy.take(parallax, hold_array)
        absorb_hold     = numpy.take(absorb, hold_array)
        logPost_hold    = numpy.take(logPost, hold_array)
        mass_hold       = numpy.take(mass,hold_array)
        logT_hold       = numpy.take(logT, hold_array)
        logg_hold       = numpy.take(logg, hold_array)
        coolingAge_hold = numpy.take(coolingAge,hold_array)
        precLogAge_hold = numpy.take(precLogAge, hold_array)
        iter_hold       = numpy.take(iter_run, hold_array)
    else :
        logAge_hold[0]      = 0
        fe_h_hold[0]        = 0
        parallax_hold[0]    = 0
        absorb_hold[0]      = 0
        logPost_hold[0]     = 0
        mass_hold[0]        = 0
        logT_hold[0]        = 0
        logg_hold[0]        = 0
        coolingAge_hold[0]  = 0
        precLogAge_hold[0]  = 0
        iter_hold[0]        = 0
   # creat plots #
fig, axs = plt.subplots(5,2)
axs[0, 0].scatter(iter_run, logAge)
axs[0, 0].set_title('Log Age')

axs[1, 0].scatter(iter_run, fe_h)
axs[1, 0].set_title('Metallicity')

axs[2, 0].scatter(iter_run, parallax)
axs[2, 0].set_title('Parallax')

axs[3, 0].scatter(iter_run, absorb)
axs[3, 0].set_title('Absorbtion')

axs[4, 0].scatter(iter_run, logPost)
axs[4, 0].set_title('logPost')

axs[0, 1].scatter(iter_run, mass)
axs[0, 1].set_title('Mass')

axs[1,1].scatter(iter_run, logT)
axs[1,1].set_title('log(T)')

axs[2,2].scatter(iter_run, coolingAge)
axs[2,2].set_title('log(coolAge)')

axs[3,3].scatter(iter_run, logg)
axs[3,3].set_title('log(g)')

axs[4,4].scatter(iter_run, precLogAge)
axs[4,4].set_title('log(precAge')


#plt.plot([X-AXIS], [Y-AXIS], [COLOR], [PLOT LABEL])
#plt.axhline(y=T_h, color='yellow', linestyle='--', label='T_h')     HORIZONTAL LINE
#plt.axvline(x=eps_crit, color='blue', linestyle='--', label='epsilon critical')    VERTICAL LINE


#plt.xlim([-0.2, 0])
#plt.xlabel('[LABEL]', fontsize=18)
#plt.ylabel('[LABEL]', fontsize=18)
#plt.legend()

plot.show()
plt.savefig('Sampling Plot')
counter = counter + 1
toc
end

