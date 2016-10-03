import os
import Utils


def Main( ATMO ):
    # First make the ATMO input file:
    out_str = '&PARAM\n'
    out_str += 'Debug = {0}\n'.format( int( ATMO.Debug ) )
    out_str += 'fout = "{0}"\n'.format( str( ATMO.fout ) )
    out_str += 'fin = "{0}"\n'.format( str( ATMO.fin ) )
    out_str += '/\n'
    out_str += '&EOS\n'
    out_str += 'gamma = {0}\n'.format( float( ATMO.gamma ) )
    out_str += '/\n'
    out_str += '&GRID\n'
    out_str += 'pmin = {0}\n'.format( float( ATMO.pmin ) )
    out_str += 'pmax = {0}\n'.format( float( ATMO.pmax ) )
    out_str += 'taumin = {0}\n'.format( float( ATMO.taumin ) )
    out_str += 'taumax = {0}\n'.format( float( ATMO.taumax ) )
    out_str += 'logg = {0}\n'.format( float( ATMO.logg ) )
    out_str += 'teff = {0}\n'.format( float( ATMO.teff ) )
    out_str += 'ndepth = {0}\n'.format( int( ATMO.ndepth ) )
    out_str += 'Rp = {0}\n'.format( float( ATMO.Rp ) )
    out_str += 'pp_Rp = {0}\n'.format( float( ATMO.pp_Rp ) )
    out_str += 'nfreq = {0}\n'.format( int( ATMO.nfreq ) )
    out_str += 'nkmix = {0}\n'.format( int( ATMO.nkmix ) )
    out_str += 'nband = {0}\n'.format( int( ATMO.nband ) )
    out_str += 'nband_std = {0}\n'.format( int( ATMO.nband_std ) )
    out_str += 'corr_k = {0}\n'.format( str( ATMO.corr_k ) )
    out_str += 'numax = {0}\n'.format( float( ATMO.numax ) )
    out_str += '/\n'
    out_str += '&CHEMISTRY\n'
    out_str += 'chem = "{0}"\n'.format( str( ATMO.chem ) )
    if ATMO.chem=='eq':
        out_str += 'MdH = {0}\n'.format( float( ATMO.MdH ) )
        out_str += 'COratio = {0}\n'.format( float( ATMO.COratio ) )
    elif ATMO.chem=='man':
        keys = ATMO.abundances.keys()
        for key in keys:
            if key=='H2':
                out_str += 'Acst(001) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='He':
                out_str += 'Acst(002) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='H2O':
                out_str += 'Acst(003) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='CO2':
                out_str += 'Acst(004) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='CO':
                out_str += 'Acst(005) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='CH4':
                out_str += 'Acst(006) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='NH3':
                out_str += 'Acst(007) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='Na':
                out_str += 'Acst(008) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='K':
                out_str += 'Acst(009) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='Li':
                out_str += 'Acst(010) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='Rb':
                out_str += 'Acst(011) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='Cs':
                out_str += 'Acst(012) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='TiO':
                out_str += 'Acst(013) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='VO':
                out_str += 'Acst(014) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='FeH':
                out_str += 'Acst(015) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='PH3':
                out_str += 'Acst(016) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='H2S':
                out_str += 'Acst(017) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='HCN':
                out_str += 'Acst(018) = {0}\n'.format( ATMO.abundances[key] )
            elif key=='C2H2':
                out_str += 'Acst(019) = {0}\n'.format( ATMO.abundances[key] )
            else:
                pdb.set_trace() # key not recognised
    out_str += 'fAin = "{0}"\n'.format( str( ATMO.fAin ) )
    out_str += 'fAeqout = "{0}"\n'.format( str( ATMO.fAeqout ) )
    out_str += 'fAneqout = "{0}"\n'.format( str( ATMO.fAneqout ) )
    out_str += 'fcoeff = "{0}"\n'.format( str( ATMO.fcoeff ) )
    out_str += 'print_chem = {0}\n'.format( str( ATMO.print_chem ) )
    out_str += '/\n'
    out_str += '&CHEM_NEQ\n'
    out_str += 'mixing = {0}\n'.format( str( ATMO.mixing ) )
    out_str += 'photochem = {0}\n'.format( str( ATMO.photochem ) )
    out_str += 'kzzcst = {0}\n'.format( float( ATMO.kzzcst ) )
    out_str += 'nmol_neq = {0}\n'.format( int( ATMO.nmol_eq ) )
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
    out_str += 'fred = {0}\n'.format( float( ATMO.fred ) )
    out_str += 'ftrans_spec = "{0}"\n'.format( str( ATMO.ftrans_spec ) )
    out_str += 'fspectrum = "{0}"\n'.format( str( ATMO.fspectrum ) )
    out_str += 'fcfout = "{0}"\n'.format( str( ATMO.fcfout ) )
    out_str += '/\n'
    out_str += '&OPACITY\n'
    if ATMO.opacity=='default':
        out_str += 'nkap = {0}\n'.format( int( ATMO.nkap ) )
    else:
        nkap = len( ATMO.opacity )
        out_str += 'nkap = {0}\n'.format( int( ATMO.nkap ) )
        if ATMO.nband<=500:
            specres = 500
        else:
            specres = 5000
        for i in range( nkap ):
            if ATMO.opacity[i]=='H2':
                ncfile = '../../kabs/h2-h2_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='He':
                ncfile = '../../kabs/h2-he_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='H2O':
                ncfile = '../../kabs/h2o_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='CO2':
                ncfile = '../../kabs/co2_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='CO':
                ncfile = '../../kabs/co_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='CH4':
                ncfile = '../../kabs/ch4_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='NH3':
                ncfile = '../../kabs/nh3_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='Na':
                ncfile = '../../kabs/na_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='K':
                ncfile = '../../kabs/k_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='Li':
                ncfile = '../../kabs/li_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='Rb':
                ncfile = '../../kabs/rb_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='Cs':
                ncfile = '../../kabs/cs_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='TiO':
                ncfile = '../../kabs/tio_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='VO':
                ncfile = '../../kabs/vo_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='FeH':
                ncfile = '../../kabs/feh_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='PH3':
                ncfile = '../../kabs/ph3_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='H2S':
                ncfile = '../../kabs/h2s_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='HCN':
                ncfile = '../../kabs/hcn_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            elif ATMO.opacity[i]=='C2H2':
                ncfile = '../../kabs/c2h2_{0:.0f}_t5e-3_uw1116.nc'.format( specres )
            else:
                pdb.set_trace() # unrecognised opacity source
            out_str += 'kapname({0:02})  = "{1}"  ; fktab({0:02})  = {2}'\
                       .format( i+1, ATMO.opacity[i], ncfile )
    out_str += 'art_haze = {0}\n'.format( int( ATMO.art_haze ) )
    out_str += 'cloud = {0}\n'.format( str( ATMO.cloud ) )
    out_str += 'cloud_top = {0}\n'.format( int( ATMO.cloud_top ) )
    out_str += 'cloud_bottom = {0}\n'.format( int( ATMO.cloud_bottom ) )
    out_str += 'cloud_strength = {0}\n'.format( int( ATMO.cloud_strength ) )
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
    out_str += 'transmission_spectrum = {0}\n'.format( str( ATMO.transmission_spectrum ) )
    out_str += 'surface_spectrum = {0}\n'.format( str( ATMO.surface_spectrum ) )
    out_str += 'hydrostatic = {0}\n'.format( str( ATMO.hydrostatic ) )
    out_str += 'calc_cf = {0}\n'.format( str( ATMO.calc_cf ) )
    out_str += '/\n'
    out_str += '&CONVECTION\n'
    out_str += 'alpha = {0}\n'.format( float( ATMO.alpha ) )
    out_str += '/'
    ofile = open( ATMO.infile_path, 'w' )
    ofile.write( out_str )
    ofile.close()
    print '\nCreated ATMO input file:\n{0}'.format( ATMO.infile_path )
    if ATMO.nice!=None:
        shell_command = 'nice -n {0:.0f} ./{1} {2}'\
                        .format( ATMO.nice, ATMO.executable, ATMO.infile_path )
    else:
        shell_command = './{0} {1}'.format( ATMO.executable, ATMO.infile_path )
    os.system( shell_command )

    return None


