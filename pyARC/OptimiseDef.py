import pdb, sys, os
import numpy as np
import scipy.optimize


def Main( ATMO, pars_init={} ):
    datasets = ATMO.TransmissionData.keys()
    ndatasets = len( datasets )
    DataArr = []
    UncArr = []    
    for i in range( ndatasets ):
        dataseti = ATMO.TransmissionData[datasets[i]]
        DataArr += [ dataseti[:,2] ]
        UncArr += [ dataseti[:,3] ]        
    DataArr = np.concatenate( DataArr )
    UncArr = np.concatenate( UncArr )
    if ATMO.Optimiser=='fmin':
        keys = pars_init.keys()
        npar = len( keys )
        parsarr_init = np.zeros( npar )
        for i in range( npar ):
            parsarr_init[i] = pars_init[keys[i]]
        def NegLogLikeFunc( parsarr, keys ):
            pars = {}
            for i in range( npar ):
                pars[keys[i]] = parsarr[i]
            return -ATMO.LogLikeFunc( pars, DataArr, UncArr )
        parsarr_fit = scipy.optimize.fmin( NegLogLikeFunc, parsarr_init, args=(keys,) )
        pars_fit = {}
        for i in range( npar ):
            pars_fit[keys[i]] = parsarr_fit[i]
        pdb.set_trace()
    else:
        pdb.set_trace()
    return None
