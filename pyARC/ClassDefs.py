import pdb, os, sys, shutil
import pyfits
import numpy as np
import MakeInDef, RunAtmoDef, OptimiseDef, SampleDef, TransmissionDef, EmissionDef

class ATMO():
    """
    """

    def __init__( self ):
        """
        """

        self.infile_path = '' # ATMO input file path

        # Namelist parameters for ATMO:
        self.Debug = 1
        self.fin = 'temp.ncdf'
        self.fout = 'pt.ncdf'
        # Equation of state parameters:
        self.gamma = 0.
        # Grid parameters:
        self.logg = 2.69
        self.teff = 100.
        self.ndepth = 50.
        self.pmin = 1e-6
        self.pmax = 1e3
        self.Rp = 0.995
        self.taumin = 1e-6
        self.taumax = 1e3
        self.nfreq = 250
        self.corr_k = True
        self.nkmix = 30
        self.nband = 32
        self.nband_std = 32
        # Chemistry parameters:
        self.chem = 'eq'
        self.fAin = 'chem_dummy.ncdf'
        self.fAeqout = 'chem_eq.ncdf'
        self.fAneqout = 'chem_neq.ncdf'
        self.fcoeff = '../../chem/coeff_NASA_sc.dat'
        self.print_chem = True
        # Non-equilibrium chemistry parameters:
        self.mixing = False
        self.photochem = False
        self.nmol_eq = 107
        self.kzzcst = 1e9
        self.tmax = 1e12
        self.dtmax = 1e10
        self.rate_limiter = True
        self.Nmin = 1e-100
        self.atol = 1e-10
        # Radiative transfer parameters:
        self.nrays = 16
        self.scatter = True
        self.firad = '' # stellar spectrum filepath
        self.rstar = 0.749
        self.rorbit = 0.0559
        self.murad = 0.5
        # Opacity parameters:
        self.nkap = 6
        self.kap_smooth = True
        self.kernel_smooth = 2
        # ATMO solver parameters:
        self.solve_hydro = True
        self.solve_energy = True
        self.minstep = 1e-4
        self.maxstep = 9e-1
        self.accuracy = 1e-1
        self.psurf = 1e-6
        self.print_err = False
        # Convection parameters:
        self.alpha = 0.
        
        # Functions for evaluating the posterior distribution:
        self.loglike_func = None # data likelihood
        self.logprior_func = None # priors

        # Functions for controlling the optimiser and sampler.
        # TODO = Have standard samplers emcee and pymultinest.
        # Also standard optimisers like scipy.optimise.fmin.
        self.sampler = 'emcee'
        self.optimiser = 'fmin'
        return None


    def RunAtmo( self ):
        """
        Runs the ATMO solver given the input file.
        """
        RunAtmoDef.Main( self )
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
