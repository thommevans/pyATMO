import pdb, os, sys, shutil
import numpy as np
import RunAtmoDef, OptimiseDef, SampleDef, TransmissionDef, EmissionDef, Utils

class ATMO():
    """
    """

    def __init__( self ):
        """
        ATMO object.
        """

        self.executable = '' # ATMO executable path
        self.infile_path = '' # ATMO input file path

        # PARAM: Parameters for ATMO
        self.Debug = 1 # Debug=1 prints additional information to screen to help with debugging
        self.fout = 'pt.ncdf' # name of the output pressure-temperature file
        self.fin = 'temp.ncdf' # name of the input pressure-temperature file; leave this 
                               # undefined to start from an isothermal profile

        # Equation of state parameters:
        self.gamma = 0. # 

        # GRID: Grid parameters
        self.pmin = 1e-6 # the minimum initial pressure
        self.pmax = 1e3 # the maximum initial pressure
        self.taumin = 1e-6 # the minimum optical depth
        self.taumax = 1e3 # the maximum optical depth
        self.logg = 2.69 # the log of the gravity
        self.teff = 100. # if irradiation is included, this represents the internal
                         # temperature of the planet; if irradiation is not included, 
                         # it represents the effective temperature of the atmosphere
        self.ndepth = 50. # the number of levels
        self.Rp = 0.995 # the planetary radius (in Jupiter radii)
        self.pp_Rp = 0. # pressure at the radius Rp (in bar)
        self.nfreq = 250 # the number of frequency points used in the radiation scheme
        self.nkmix = 30 # number of k-coefficients for gas mixture
        self.nband = 32 # the number of bands to use
        self.nband_std = 32 # the band used to define the optical depth grid
        self.corr_k = True # flag to use the correlated-k method (if false, line-by-line is used)
        self.numax = 5e6 # upper limit on the wave number

        # CHEMISTRY: Chemistry parameters
        self.chem = 'eq' # flag to choose which type of chemistry to use; 'ana' - analytical, 
                         # 'eq' - equilibrium, 'neq' - non-equilibrium and 'cst' holds the 
                         # abundances constant
        self.MdH = 0. # metallicity of the atmosphere, log base 10. [M/H] = 0 for the Sun.  
                      # [M/H] = 2 is 100x solar
        self.COratio = 0. # The carbon-oxygen ratio. A default solar value ([C/O] ~ 0.56) is 
                          # assumed if COratio = 0. E.g. a ~2x solar value would be COratio = 1.2.
        self.fAin = 'chem_dummy.ncdf' # the name of the input chemistry file; if running 'ana' or 
                                      # 'eq' this should be the chem_dummy file, otherwise it 
                                      # should be a pre-calculated equilibrium chemistry file
        self.fAeqout = 'chem_eq.ncdf' # the name of the output equilibrium chemistry file
        self.fAneqout = 'chem_neq.ncdf' # the name of the output non-equilibrium chemistry file
        self.fcoeff = '../../chem/coeff_NASA_sc.dat' # 
        self.print_chem = True # 

        # CHEM_NEQ: Non-equilibrium chemistry parameters
        self.mixing = False # flag to turn vertical mixing on/off
        self.photochem = False # flag to turn photochemistry on/off
        self.kzzcst = 1e9 # value of the Kzz term, if kzzcst = 0. then the value is read from 'fin'
        self.nmol_eq = 107 # 
        self.tmax = 1e12 # the maximum integration time
        self.dtmax = 1e10 # the maximum time step
        self.rate_limiter = True # flag to turn on the rate limiter 
        self.Nmin = 1e-100 # the minimum number density
        self.atol = 1e-10 # the absolute tolerance of the solver

        # RADTRANS: Radiative transfer parameters
        self.nrays = 16 # the number of rays
        self.scatter = True # flag to turn on scattering
        self.irrad = True # flag to turn on irradiation
        self.firad = '' # name of the irradiation input file
        self.rstar = 0.749 # the radius of the star in solar radii
        self.rorbit = 0.0559 # the semi-major axis of the planet in astronomical units
        self.murad = 0.5 # the inclination angle of the irradiation
        self.fred = 0.5 # the amount the irradiation is reduced at the top of the atmosphere; 
                        # e.g. fred = 0.5 for efficient horizontal redistribution
        self.ftrans_spec = '' # name of the output transmission spectrum
        self.fspectrum = '' # name of the output emission spectrum
        self.fcfout = '' # name of the output normalised contribution function file which is
                         # a function of wavenumber and pressure
        

        # OPACITY: Opacity parameters
        self.nkap = 6 # the number of molecules used for opacities (note: ordering is hard-coded)
                      # Addition of each opacity source along with the previous ones, with increase
                      # in value of nkap are as follows:
                      # 1) H2  2) He  3) H2O  4) CO2  5) CO  6) CH4  7) NH3  8) Na  9) K  10) Li  
                      # 11) Rb  12) Cs  13) TiO  14) VO  15) FeH 16) PH3 17) H2S 18) HCN 
                      # 19) C2H2 20) SO2
        self.art_haze = 1 # the variable to input artificial haze/scattering.  
                          # (e.g. art_haze = 1 means one times standard rayleigh scattering, 
                          # 2 means two times and so on. Default = 1)
        self.cloud = False # flag to turn on cloud deck (True or False), default is False
        self.cloud_top = 1 # integer representing cloud top (minimum is 1 - top of the atmophsere, 
                           # maximum is ndepth lowest level in the atmosphere). Default is 1.
        self.cloud_bottom = 20 # integer representing cloud bottom (cloud_bottom should be greater 
                               # than cloud_top). Default is 20. To check which pressure levels 
                               # these layers correspond to, see your input p-t profile file.
        self.cloud_strength = 1 # multiplication factor to increase cloud deck scattering opacity 
                                # realtive to molecualr hydrogen scattering opacity. 
                                # (e.g. 1x, 2x, 10x, 50x etc.). Default is 1
        self.kap_smooth = True # smooths the opacities, important for convergence at the top of the
                               # atmosphere
        self.kerkap_smooth = 2 # smoothing kernel for opacities

        # SOLVER: ATMO solver parameters
        self.solve_hydro = True # flag to solve hydrostatic equation
        self.solve_energy = True # flag to solve energy equation
        self.minstep = 1e-4 # minimum step of the solver
        self.maxstep = 9e-1 # maximum step of the solver
        self.accuracy = 1e-1 # tolerance of the solver
        self.psurf = 1e-6 # the pressure at the upper boundary of the model (i.e. minimum pressure)
        self.print_err = False # 
        self.transmission_spectrum = False # calculate transmission spectrum
        self.surface_spectrum = False # calculate emission spectrum
        self.hydrostatic = True # assume the PT profile is already in hydrostatic balance
        self.calc_cf = True # set to True to obtain contribution function otherwise False
        
        # CONVECTION: Convection parameters
        self.alpha = 0. # the mixing length for convection

        # Array for holding the bandpass used to take the data:
        # TODO - This might require some thought, e.g. what if there are multiple bandpasses
        # for a heterogenous dataset?
        
        # Arrays for holding Transmission and Emission data:
        self.TransmissionData = None
        
        # Provide emission data:
        #self.EmissionData = None
        
        # Functions for evaluating the posterior distribution:
        self.loglike_func = None # data likelihood
        self.logprior_func = None # priors

        # Functions for controlling the optimiser and sampler.
        # TODO = Have standard samplers emcee and pymultinest.
        # Also standard optimisers like scipy.optimise.fmin.
        self.sampler = 'emcee'
        self.optimiser = 'fmin'

        return None


    def RunATMO( self ):
        """
        Runs the ATMO solver given the input file.
        """
        RunATMODef.Main( self )
        return None

    
    def ReadPT( self, ncdf_fpath='' ):
        """
        """
        Utils.ReadPT( self, ncdf_fpath=ncdf_fpath )
        return None


    def PlotPT( self, ofigpath='' ):
        """
        """
        Utils.PlotPT( self, ofigpath=ofigpath )
        return None

    
    def ReadTransmissionModel( self, ncdf_fpath='' ):
        """
        """
        Utils.ReadTransmissionModel( self, ncdf_fpath=ncdf_fpath )
        return None
    

    def PlotTransmissionModel( self, ofigpath='', xscale='log' ):
        """
        """
        Utils.PlotTransmissionModel( self, ofigpath=ofigpath, xscale=xscale )
        return None
    

    def Optimise( self ):
        """
        Optimises the posterior distribution with respect to the model parameters
        using the optimiser specified by the self.optimiser attribute.
        """
        OptimiseDef.Main( self )
        return None


    def Sample( self ):
        """
        Samples from the posterior distribution using the sampler specified by the
        self.sampler attribute.
        """
        SampleDef.Main( self )
        return None


    def Transmission( self ):
        TransmissionDef.Main( self )
        return None


    def Emission( self ):
        EmissionDef.Main( self )
        return None
