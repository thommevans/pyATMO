

def Main( ATMO ):

    # First make the ATMO input file:
    out_str = '&PARAM'
    out_str += 'Debug = {0}'.format( ATMO.Debug )
    out_str += 'fin = {0}'.format( ATMO.fin )
    out_str += 'fout = {0}'.format( ATMO.fout )
    out_str += '/\n'
    out_str += '&EOS'
    out_str += 'gamma = {0}'.format( ATMO.gamma )
    out_str += '/\n'
    out_str += '&GRID'
    out_str += 'logg = {0}'.format( ATMO.logg )
    out_str += 'teff = {0}'.format( ATMO.teff )
    out_str += 'ndepth = {0}'.format( ATMO.ndepth )
    out_str += 'pmin = {0}'.format( ATMO.pmin )
    out_str += 'pmax = {0}'.format( ATMO.pmax )
    out_str += 'Rp = {0}'.format( ATMO.Rp )
    out_str += 'taumin = {0}'.format( ATMO.taumin )
    out_str += 'taumax = {0}'.format( ATMO.taumax )
    out_str += 'nfreq = {0}'.format( ATMO.nfreq )
    out_str += 'corr_k = {0}'.format( ATMO.corr_k )
    out_str += 'nkmix = {0}'.format( ATMO.nkmix )
    out_str += 'nband = {0}'.format( ATMO.nband )
    out_str += 'nband_std = {0}'.format( ATMO.nband_std )
    out_str += '/\n'
    out_str += '&CHEMISTRY'
    out_str += 'chem = {0}'.format( ATMO.chem )
    out_str += 'fAin = {0}'.format( ATMO.fAin )
    out_str += 'fAeqout = {0}'.format( ATMO.fAeqout )
    out_str += 'fAneqout = {0}'.format( ATMO.fAneqout )
    out_str += 'fcoeff = {0}'.format( ATMO.fcoeff )
    out_str += 'print_chem = {0}'.format( ATMO.print_chem )
    out_str += '/\n'
    out_str += '&CHEM_NEQ'
    out_str += 'mixing = {0}'.format( ATMO.mixing )
    out_str += 'photochem = {0}'.format( ATMO.photochem )
    out_str += 'nmol_neq = {0}'.format( ATMO.nmol_eq )
    out_str += 'kzzcst = {0}'.format( ATMO.kzzcst )
    out_str += 'tmax = {0}'.format( ATMO.tmax )
    out_str += 'dtmax = {0}'.format( ATMO.dtmax )
    out_str += 'rate_limiter = {0}'.format( ATMO.rate_limiter )
    out_str += 'Nmin = {0}'.format( ATMO.Nmin )
    out_str += 'atol = {0}'.format( ATMO.atol )
    out_str += '/\n'
    out_str += '&RADTRANS'
    out_str += 'nrays = {0}'.format( ATMO.nrays )
    out_str += 'scatter = {0}'.format( ATMO.scatter )
    out_str += 'irrad = {0}'.format( ATMO.irrad )
    out_str += 'firad = {0}'.format( ATMO.firad )
    out_str += 'rstar = {0}'.format( ATMO.rstar )
    out_str += 'rorbit = {0}'.format( ATMO.rorbit )
    out_str += 'murad = {0}'.format( ATMO.murad )
    out_str += '/\n'
    out_str += '&OPACITY'
    out_str += 'nkap = {0}'.format( ATMO.nkap )
    out_str += 'kap_smooth = {0}'.format( ATMO.kap_smooth )
    out_str += 'kernel_smooth = {0}'.format( ATMO.kernel_smooth )
    out_str += '/\n'
    out_str += '&SOLVER'
    out_str += 'solve_hydro = {0}'.format( ATMO.solve_hydro )
    out_str += 'solve_energy = {0}'.format( ATMO.solve_energy )
    out_str += 'minstep = {0}'.format( ATMO.minstep )
    out_str += 'maxstep = {0}'.format( ATMO.maxstep )
    out_str += 'accuracy = {0}'.format( ATMO.accuracy )
    out_str += 'psurf = {0}'.format( ATMO.psurf )
    out_str += 'print_err = {0}'.format( ATMO.print_err )
    out_str += '/\n'
    out_str += '&CONVECTION'
    out_str += 'alpha = {0}'.format( ATMO.alpha )
    out_str += '/'
    ofile = open( ATMO.infile_path, 'w' )
    ofile.write( out_str )
    ofile.close()
    print '\nCreated ATMO input file:\n{0}'.format( ATMO.infile_path )

    return None
