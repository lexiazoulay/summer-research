#plot mcmc sampling histories for Gaia WDS sample
%reset-f #ask Sarah what the help plot_sampling_batch;

import time
import os
import re
import pandas

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
    #grab EDR3 parallax values out of file name
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
    sample        = pandas.read_csv(stars(st).name, ' ') #may not be correct...
    
    logAge        = sample[0]
    fe-h          = sample[1]
    parralax      = sample[2]
    absorb        = sample[3]
    logPost       = sample[4]
    stage         = sample[5]
    mass          = sample[6]
    logT          = sample[7]
    logg          = sample[8]
    coolingAge    = sample[9]
    precLogAge    = sample[10]
    
    
