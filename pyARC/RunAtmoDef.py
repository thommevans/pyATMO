import os

def Main( ATMO ):

    # First make the ATMO input file:
    out_str = '&PARAM\n'
    out_str += 'Debug = {0}\n'.format( ATMO.Debug )
    out_str += 'fin = "{0}"\n'.format( ATMO.fin )
    out_str += 'fout = "{0}"\n'.format( ATMO.fout )
    out_str += '/\n'
    out_str += '&EOS\n'
    out_str += 'gamma = {0}\n'.format( ATMO.gamma )
    out_str += '/\n'
    out_str += '&GRID\n'
    out_str += 'logg = {0}\n'.format( ATMO.logg )
    out_str += 'teff = {0}\n'.format( ATMO.teff )
    out_str += 'ndepth = {0}\n'.format( ATMO.ndepth )
    out_str += 'pmin = {0}\n'.format( ATMO.pmin )
    out_str += 'pmax = {0}\n'.format( ATMO.pmax )
    out_str += 'Rp = {0}\n'.format( ATMO.Rp )
    out_str += 'taumin = {0}\n'.format( ATMO.taumin )
    out_str += 'taumax = {0}\n'.format( ATMO.taumax )
    out_str += 'nfreq = {0}\n'.format( ATMO.nfreq )
    out_str += 'corr_k = {0}\n'.format( ATMO.corr_k )
    out_str += 'nkmix = {0}\n'.format( ATMO.nkmix )
    out_str += 'nband = {0}\n'.format( ATMO.nband )
    out_str += 'nband_std = {0}\n'.format( ATMO.nband_std )
    out_str += '/\n'
    out_str += '&CHEMISTRY\n'
    out_str += 'chem = "{0}"\n'.format( ATMO.chem )
    out_str += 'fAin = "{0}"\n'.format( ATMO.fAin )
    out_str += 'fAeqout = "{0}"\n'.format( ATMO.fAeqout )
    out_str += 'fAneqout = "{0}"\n'.format( ATMO.fAneqout )
    out_str += 'fcoeff = "{0}"\n'.format( ATMO.fcoeff )
    out_str += 'print_chem = {0}\n'.format( ATMO.print_chem )
    out_str += '/\n'
    out_str += '&CHEM_NEQ\n'
    out_str += 'mixing = {0}\n'.format( ATMO.mixing )
    out_str += 'photochem = {0}\n'.format( ATMO.photochem )
    out_str += 'nmol_neq = {0}\n'.format( ATMO.nmol_eq )
    out_str += 'kzzcst = {0}\n'.format( ATMO.kzzcst )
    out_str += 'tmax = {0}\n'.format( ATMO.tmax )
    out_str += 'dtmax = {0}\n'.format( ATMO.dtmax )
    out_str += 'rate_limiter = {0}\n'.format( ATMO.rate_limiter )
    out_str += 'Nmin = {0}\n'.format( ATMO.Nmin )
    out_str += 'atol = {0}\n'.format( ATMO.atol )
    out_str += '/\n'
    out_str += '&RADTRANS\n'
    out_str += 'nrays = {0}\n'.format( ATMO.nrays )
    out_str += 'scatter = {0}\n'.format( ATMO.scatter )
    out_str += 'irrad = {0}\n'.format( ATMO.irrad )
    out_str += 'firad = "{0}"\n'.format( ATMO.firad )
    out_str += 'rstar = {0}\n'.format( ATMO.rstar )
    out_str += 'rorbit = {0}\n'.format( ATMO.rorbit )
    out_str += 'murad = {0}\n'.format( ATMO.murad )
    out_str += '/\n'
    out_str += '&OPACITY\n'
    out_str += 'nkap = {0}\n'.format( ATMO.nkap )
    out_str += 'kap_smooth = {0}\n'.format( ATMO.kap_smooth )
    out_str += 'kernel_smooth = {0}\n'.format( ATMO.kernel_smooth )
    out_str += '/\n'
    out_str += '&SOLVER\n'
    out_str += 'solve_hydro = {0}\n'.format( ATMO.solve_hydro )
    out_str += 'solve_energy = {0}\n'.format( ATMO.solve_energy )
    out_str += 'minstep = {0}\n'.format( ATMO.minstep )
    out_str += 'maxstep = {0}\n'.format( ATMO.maxstep )
    out_str += 'accuracy = {0}\n'.format( ATMO.accuracy )
    out_str += 'psurf = {0}\n'.format( ATMO.psurf )
    out_str += 'print_err = {0}\n'.format( ATMO.print_err )
    out_str += '/\n'
    out_str += '&CONVECTION\n'
    out_str += 'alpha = {0}\n'.format( ATMO.alpha )
    out_str += '/'
    ofile = open( ATMO.infile_path, 'w' )
    ofile.write( out_str )
    ofile.close()
    print '\nCreated ATMO input file:\n{0}'.format( ATMO.infile_path )

    shell_command = './{0} {1}'.format( ATMO.executable, ATMO.infile_path )
    os.system( shell_command )

    return None
