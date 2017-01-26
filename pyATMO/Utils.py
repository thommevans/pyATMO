import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import pdb, os, sys



def ReadChem( ATMO, ncdf_fpath='' ):
    ncdfFile = scipy.io.netcdf.netcdf_file( ncdf_fpath, mode='r', mmap=False )
    z = ncdfFile.variables
    molname = []
    for i in z['molname'][:]:
        molnamei = ''
        for j in i:
            molnamei += j
        molname += [ molnamei.replace( ' ', '' ) ]
    ATMO.Chem = { 'molname':molname, 'pressure_bar':z['pressure'][:]/1e6, \
                  'abundance':z['abundances'][:] }
    return None


def ReadPT( ATMO, ncdf_fpath='' ):
    """
    Reads an ATMO pressure-temperature profile and stores it in an Nx2
    array, where the first column is pressure in bar and the second
    column is temperature in Kelvin.    
    """
    
    ncdfFile = scipy.io.netcdf.netcdf_file( ncdf_fpath, mode='r', mmap=False )
    z = ncdfFile.variables
    ATMO.PT = np.column_stack( [ z['pressure'][:]/1e6, z['temperature'][:] ] )
    return None


def PlotPT( ATMO, ofigpath='' ):
    if hasattr( ATMO, 'PT' ):
        fig = plt.figure( figsize=[12,12] )
        xlow = 0.1
        ylow = 0.1
        axw = 0.85
        axh = 0.85
        ax = fig.add_axes( [ xlow, ylow, axw, axh ] )
        lw = 2
        c = 'r'
        ax.plot( ATMO.PT[:,1], ATMO.PT[:,0], '-', lw=lw, c=c )
        ax.set_xscale( 'linear' )
        ax.set_yscale( 'log' )
        ax.set_ylim( [ ATMO.PT[:,0].max(), ATMO.PT[:,0].min() ] )
        fig.savefig( ofigpath )
        print '\nSaved PT figure: {0}\n'.format( ofigpath )
    else:
        print '\nPT attribute does not exist. Run ReadPT() first.\n'
    return None


def ReadTransmissionModel( ATMO, ncdf_fpath='' ):
    ncdfFile = scipy.io.netcdf.netcdf_file( ncdf_fpath, mode='r', mmap=False )
    z = ncdfFile.variables
    nu = z['nu'][:]
    RpRs = z['transit_radius'][:]
    wav_micron = (1e4)*( 1./nu )
    ixs = np.argsort( wav_micron )
    ATMO.TransmissionModel = np.column_stack( [ wav_micron[ixs], RpRs[ixs] ] )
    return None


def ReadEmissionModel( ATMO, ncdf_fpath='' ):
    ncdfFile = scipy.io.netcdf.netcdf_file( ncdf_fpath, mode='r', mmap=False )
    z = ncdfFile.variables
    nu = z['nu'][:]
    nubandmin = z['nubandmin'][:]
    nubandmax = z['nubandmax'][:]
    fnu_p = z['fnu'][:]
    fnu_s = z['fnu_star'][:]
    Rp = z['R_planet_TOA'].data
    Rs = z['R_star'].data
    FpFs = ( ( Rp/Rs )**2. )*( fnu_p/fnu_s )
    wav_micron = (1e4)*( 1./nu )
    ixs = np.argsort( wav_micron )
    ATMO.EmissionModelNuCGS = nu[ixs]
    ATMO.EmissionModelNuBandMinCGS = nubandmin
    ATMO.EmissionModelNuBandMaxCGS = nubandmax
    ATMO.EmissionModelWavMicron = wav_micron[ixs]
    ATMO.EmissionModelFpFs = FpFs[ixs]
    ATMO.EmissionModelFpnu = fnu_p[ixs]
    ATMO.EmissionModelRp = Rp
    ATMO.EmissionModelFsnu = fnu_s[ixs]
    ATMO.EmissionModelRs = Rs
    return None


def ComputeOpacities( ATMO, species=[ 'H2O', 'CO', 'CH4' ], odir='.' ):
    freeze = ATMO.__dict__
    species = np.array( species )
    n = len( species )
    ATMO.nkap = 1
    ATMO.scatter = False
    print '\nSaving opacities:'
    for i in range( n ):
        ATMO.opacity = [ species[i] ]
        ofilename = 'opacity.{0}.ncdf'.format( species[i] )
        ATMO.ftrans_spec = os.path.join( odir, ofilename )
        ATMO.RunATMO()
        print ATMO.infile_path
        print '{0}'.format( ATMO.ftrans_spec )
        # Testing below here:
        ATMO.ReadTransmissionModel( ncdf_fpath=ATMO.ftrans_spec )
        x = ATMO.TransmissionModel[:,0]
        y = ATMO.TransmissionModel[:,1]
        plt.figure()
        plt.plot(x,y,'-')
        plt.title( species[i] )
        plt.show()
    for key in freeze.keys():
        ATMO.__dict__[key] = freeze[key]
    return None


def PlotTransmissionModel( ATMO, ofigpath='', xscale='log', yscale='linear' ):
    # TODO adapt this from pt profile plotting
    plt.ion()
    if hasattr( ATMO, 'TransmissionModel' ):
        fig = plt.figure( figsize=[14,12] )
        vbuff = 0.05
        axw = 0.85
        axh = ( 1-3*vbuff )/2.
        xlow = 0.1
        ylow1 = 1 - vbuff - axh
        ylow2 = ylow1 - vbuff - axh
        ax1 = fig.add_axes( [ xlow, ylow1, axw, axh ] )
        ax2 = fig.add_axes( [ xlow, ylow2, axw, axh ] )
        lw = 2
        c = 'r'
        wav_micron = ATMO.TransmissionModel[:,0]
        RpRs = ATMO.TransmissionModel[:,1]
        axs = [ ax1, ax2 ]
        for i in range( 2 ):
            axs[i].plot( wav_micron, RpRs, '-', lw=lw, c=c )
            axs[i].set_xscale( xscale )
            axs[i].set_yscale( yscale )
        dRpRs = RpRs.max() - RpRs.min()
        x1a = 0.26
        x1b = 10.0
        x2a = 10.0
        x2b = 30.0
        ax1.set_xlim( [ x1a, x1b ] )
        ax2.set_xlim( [ x2a, x2b ] )        
        ax1.set_ylim( [ RpRs.min()-0.15*dRpRs, RpRs.max()+0.15*dRpRs ] )
        ax2.set_ylim( [ RpRs.min()-0.15*dRpRs, RpRs.max()+0.15*dRpRs ] )        
        fig.savefig( ofigpath )
        print '\nSaved TransmissionModel figure: {0}\n'.format( ofigpath )
    else:
        print '\nTransmissionModel attribute does not exist. Run ReadTransmissionModel() first.\n'
    return None

