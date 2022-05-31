#plot mcmc sampling histories for Gaia WDS sample
%reset-f #ask Sarah what the help plot_sampling_batch;

import time
import os
import re
import pandas
import numpy

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
    
    N_full_len    = len(logAge)
    iter          = numpy.arange(1, N_full_len + 1)
    
    skip_burn = 1
    if stage(end) < 3:          #entire file remained in burnin, so 
        print(' Entire file remained in burnin, so nothing to calculate or plot ... skipping.\n')
        continue                   #nothing to calculate or plot, skipping
    if stage(1) == 3:               #already cleaned by hand with burnin removed
        start_iter = 1
    else:
        for skip_burn in iter:       #skip over the burnin iterations
            if stage(skip_burn) == 3:
                start_iter = skip_burn
                break
    #Check for chain not yet converged as shown by logPost climbing 
    #dramatically. If that happens, move start_iter forward.
    
    add_iter    = [0,0]
    logP_half_len = len(logPost)/2
    logP_half = numpy.empty(logP_half_len)
    x = 0
    for x in logP_half:
        logP_half = logPost[logP_half_len + x]
    logP_comp   = numpy.average(logP_half)
    
    threshold   = 10				# logPost threshold diff for recognizing convergence
    chunk_len   = 1000				# chain lengths over which means are checked
    half_chnlen = chunk_len/2		# convenience
    
    i_logPost = start_iter
    for i_logPost in chunk_len:N_full_len	# calc chain means in chunks    HOW???
        lo = max(start_iter, i_logPost-half_chnlen)
        hi = min(i_logPost+half_chnlen, N_full_len)
        if hi < lo:
            print(' Not enough iterations in ', stars(st).name, ' to check burnin via logPost, continuing ...\n')
            break
        logPostVal = mean(logPost(lo:hi))
        if logPostVal < logP_comp - threshold:
            add_iter(1) = i_logPost         # ?????
      
    #numpy.std(...) standard deviation
