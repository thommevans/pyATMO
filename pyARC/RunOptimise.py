from pyARC_dev import pyARC
import InstallNamelistParameters
import numpy as np
import pdb, sys, os

LOGG = InstallNamelistParameters.LOGG
TEQ = InstallNamelistParameters.TEQ
RPLANET = InstallNamelistParameters.RPLANET
RSTAR = InstallNamelistParameters.RSTAR
AAU = InstallNamelistParameters.AAU
MDH = InstallNamelistParameters.MDH
CORATIO = InstallNamelistParameters.CORATIO


TRANSMISSIONMODEL = 'TransmissionModelForFitting.ncdf'
TRANSMISSIONDATA = 'TransmissionDataForFitting.txt'



def ClearAtmosphere( pars_init={} ):
    
    ATMO = pyARC.ATMO()
    InstallNamelistParameters.Main( ATMO )
    ATMO.ReadTransmissionModel( ncdf_fpath=TRANSMISSIONMODEL )
    ATMO.TransmissionData = { 'G141':np.loadtxt( TRANSMISSIONDATA ) }
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
            return -ModelLogLikelihoods.ClearAtmosphere( ATMO, pars, DataArr, UncArr )
        parsarr_fit = scipy.optimize.fmin( NegLogLikeFunc, parsarr_init, args=(keys,) )
        pars_fit = {}
        for i in range( npar ):
            pars_fit[keys[i]] = parsarr_fit[i]
        pdb.set_trace()
    else:
        pdb.set_trace()

    return None


def logp_mvnormal_whitenoise( r, u, n  ):
    """
    Log likelihood of a multivariate normal distribution
    with diagonal covariance matrix.
    """
    term1 = -np.sum( np.log( u ) )
    term2 = -0.5*np.sum( ( r/u )**2. )
    return term1 + term2 - 0.5*n*np.log( 2*np.pi )

    

def MakeTransmissionModel():
    ATMO = pyARC.ATMO()
    InstallNamelistParameters.Main( ATMO )
    ATMO.Debug = 0
    ATMO.fin = None
    ATMO.nband = 5000
    ATMO.teff = TEQ
    ATMO.logg = LOGG
    ATMO.MdH = MDH
    ATMO.COratio = CORATIO
    ATMO.art_haze = 1.
    ATMO.cloud = False
    ATMO.solve_hydro = False
    ATMO.solve_energy = False
    ATMO.transmission_spectrum = True
    ATMO.surface_spectrum = False
    ATMO.ftrans_spec = TRANSMISSIONMODEL
    ATMO.RunATMO()
    return None


def MakeTransmissionData( make_plot=False ):

    # Uncertainty on RpRs data:
    RpRsSig = 4e-4
    
    # Edges for the wavelength channels:
    chedges = np.linspace( 1.12, 1.6, 28 )

    # Read in the previously-generated transmission model:
    ATMO = pyARC.ATMO()
    ATMO.ReadTransmissionModel( ncdf_fpath=TRANSMISSIONMODEL )
    wav_micron = ATMO.TransmissionModel[:,0]
    RpRsModel = ATMO.TransmissionModel[:,1]

    # Bin the model into the wavelength channels:
    nchannels = len( chedges )-1
    RpRsData = np.zeros( nchannels )
    for i in range( nchannels ):
        ixs = ( wav_micron>=chedges[i] )*( wav_micron<chedges[i+1] )
        RpRsData[i] = np.mean( RpRsModel[ixs] )

    # Add measurement uncertainties:
    RpRsData += RpRsSig*np.random.randn( nchannels )
    RpRsUncs = RpRsSig*np.ones( nchannels )

    # Save to file:
    output = np.column_stack( [ chedges[:-1], chedges[1:], RpRsData, RpRsUncs ] )
    np.savetxt( TRANSMISSIONDATA, output )

    if make_plot==True:
        x = 0.5*( chedges[:-1] + chedges[1:] )
        plt.ion()
        plt.figure()
        plt.plot( wav_micron, RpRsModel, '-c' )
        plt.plot( x, RpRsData, 'o', ms=10, mfc='r', mec='r' )
        plt.errorbar( x, RpRsData, yerr=4e-4, fmt='ok' )
        plt.xlim( [ 1, 2 ] )
        plt.xlabel( 'Wav (micron)' )
        plt.ylabel( 'Rp/Rs' )
    
    return None
