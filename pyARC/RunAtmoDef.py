import os
import Utils


def Main( ATMO ):

    # First make the ATMO input file:
    out_str = '&PARAM\n'
    out_str += 'Debug = {0}\n'.format( int( ATMO.Debug ) )
    out_str += 'fin = "{0}"\n'.format( str( ATMO.fin ) )
    out_str += 'fout = "{0}"\n'.format( str( ATMO.fout ) )
    out_str += '/\n'
    out_str += '&EOS\n'
    out_str += 'gamma = {0}\n'.format( float( ATMO.gamma ) )
    out_str += '/\n'
    out_str += '&GRID\n'
    out_str += 'logg = {0}\n'.format( float( ATMO.logg ) )
    out_str += 'teff = {0}\n'.format( float( ATMO.teff ) )
    out_str += 'ndepth = {0}\n'.format( int( ATMO.ndepth ) )
    out_str += 'pmin = {0}\n'.format( float( ATMO.pmin ) )
    out_str += 'pmax = {0}\n'.format( float( ATMO.pmax ) )
    out_str += 'Rp = {0}\n'.format( float( ATMO.Rp ) )
    out_str += 'taumin = {0}\n'.format( float( ATMO.taumin ) )
    out_str += 'taumax = {0}\n'.format( float( ATMO.taumax ) )
    out_str += 'nfreq = {0}\n'.format( int( ATMO.nfreq ) )
    out_str += 'corr_k = {0}\n'.format( str( ATMO.corr_k ) )
    out_str += 'nkmix = {0}\n'.format( int( ATMO.nkmix ) )
    out_str += 'nband = {0}\n'.format( int( ATMO.nband ) )
    out_str += 'nband_std = {0}\n'.format( int( ATMO.nband_std ) )
    out_str += '/\n'
    out_str += '&CHEMISTRY\n'
    out_str += 'chem = "{0}"\n'.format( str( ATMO.chem ) )
    out_str += 'fAin = "{0}"\n'.format( str( ATMO.fAin ) )
    out_str += 'fAeqout = "{0}"\n'.format( str( ATMO.fAeqout ) )
    out_str += 'fAneqout = "{0}"\n'.format( str( ATMO.fAneqout ) )
    out_str += 'fcoeff = "{0}"\n'.format( str( ATMO.fcoeff ) )
    out_str += 'print_chem = {0}\n'.format( str( ATMO.print_chem ) )
    out_str += '/\n'
    out_str += '&CHEM_NEQ\n'
    out_str += 'mixing = {0}\n'.format( str( ATMO.mixing ) )
    out_str += 'photochem = {0}\n'.format( str( ATMO.photochem ) )
    out_str += 'nmol_neq = {0}\n'.format( int( ATMO.nmol_eq ) )
    out_str += 'kzzcst = {0}\n'.format( float( ATMO.kzzcst ) )
    out_str += 'tmax = {0}\n'.format( float( ATMO.tmax ) )
    out_str += 'dtmax = {0}\n'.format( float( ATMO.dtmax ) )
    out_str += 'rate_limiter = {0}\n'.format( str( ATMO.rate_limiter ) )
    out_str += 'Nmin = {0}\n'.format( float( ATMO.Nmin ) )
    out_str += 'atol = {0}\n'.format( float( ATMO.atol ) )
    out_str += '/\n'
    out_str += '&RADTRANS\n'
    out_str += 'nrays = {0}\n'.format( int( ATMO.nrays ) )
    out_str += 'scatter = {0}\n'.format( str( ATMO.scatter ) )
    out_str += 'irrad = {0}\n'.format( str( ATMO.irrad ) )
    out_str += 'firad = "{0}"\n'.format( str( ATMO.firad ) )
    out_str += 'rstar = {0}\n'.format( float( ATMO.rstar ) )
    out_str += 'rorbit = {0}\n'.format( float( ATMO.rorbit ) )
    out_str += 'murad = {0}\n'.format( float( ATMO.murad ) )
    out_str += '/\n'
    out_str += '&OPACITY\n'
    out_str += 'nkap = {0}\n'.format( int( ATMO.nkap ) )
    out_str += 'kap_smooth = {0}\n'.format( str( ATMO.kap_smooth ) )
    out_str += 'kerkap_smooth = {0}\n'.format( int( ATMO.kerkap_smooth ) )
    out_str += '/\n'
    out_str += '&SOLVER\n'
    out_str += 'solve_hydro = {0}\n'.format( str( ATMO.solve_hydro ) )
    out_str += 'solve_energy = {0}\n'.format( str( ATMO.solve_energy ) )
    out_str += 'minstep = {0}\n'.format( float( ATMO.minstep ) )
    out_str += 'maxstep = {0}\n'.format( float( ATMO.maxstep ) )
    out_str += 'accuracy = {0}\n'.format( float( ATMO.accuracy ) )
    out_str += 'psurf = {0}\n'.format( float( ATMO.psurf ) )
    out_str += 'print_err = {0}\n'.format( str( ATMO.print_err ) )
    out_str += '/\n'
    out_str += '&CONVECTION\n'
    out_str += 'alpha = {0}\n'.format( float( ATMO.alpha ) )
    out_str += '/'
    ofile = open( ATMO.infile_path, 'w' )
    ofile.write( out_str )
    ofile.close()
    print '\nCreated ATMO input file:\n{0}'.format( ATMO.infile_path )

    shell_command = './{0} {1}'.format( ATMO.executable, ATMO.infile_path )
    os.system( shell_command )

    Utils.ReadPT( ATMO, ncdf_fpath=ATMO.fout )

    return None


