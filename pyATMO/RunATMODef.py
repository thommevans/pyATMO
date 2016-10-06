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
        chemmap = get_chemmap()        
        for key in keys:
            matched = False
            for chemname in chemmap.keys():
                if key==chemname:
                    matched = True
                    ix = chemmap[chemname]
                    out_str += 'Acst({0:03}) = {1} ! {2}\n'\
                               .format( ix, ATMO.abundances[key], key )                    
                else:
                    continue
            if matched==False:
                pdb.set_trace() # could not match to any ATMO species
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
        out_str += 'nkap = {0:02}\n'.format( int( nkap ) )
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
            out_str += 'kapname({0:02})  = "{1}"  ; fktab({0:02})  = "{2}"\n'\
                       .format( i+1, ATMO.opacity[i], ncfile )
    if ATMO.art_haze!=None:
        out_str += 'art_haze = {0}\n'.format( int( ATMO.art_haze ) )
    out_str += 'cloud = {0}\n'.format( str( ATMO.cloud ) )
    if ATMO.cloud!=False:
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


def get_chemmap():
    return { 'H2':1, 'O-3P':2, 'O-1D':3, 'CO':4, 'C':5, \
             'CH':6, '3CH2':7, '1CH2':8, 'H2O':9, 'O2':10, \
             'H2O2':11, 'CH4':12,     'H2CO':13, 'CH3OH':14, 'CO2':15, \
             'CH3OOH':16, 'C2H2':17, 'C2H4':18, 'C2H6':19, 'CH2CO':20, \
             'CH3CHO':21, 'C2H5OH':22, 'C2H5OOH':23, 'CH3COOOH':24, 'C3H8':25, \
             'C4H8Y':26, 'C4H10':27, 'C2H5CHO':28, 'C3H7OH':29, 'C2H6CO':30, \
             'C3H8CO':31, 'C2H3CHOZ':32, 'cC2H4O':33, 'C3H7OH':34, 'C2H6CO':35, \
             'OH':36, 'OOH':37, 'CH3':38, 'HCO':39, 'CH2OH':40, \
             'CH3O':41, 'CH3OO':42, 'C2H':43, 'C2H3':44, 'C2H5':45, \
             'CHCO':46, 'CH2CHO':47, 'CH3CO':48, 'C2H5O':49, 'C2H4OOH':50, \
             'C2H5OO':51, 'CH3COOO':52, '1C3H7':53, '1C4H9':54, 'CH3OCO':55, \
             'CO2H':56, '2C2H4OH':57, '1C2H4OH':58, '2C3H7':59, '2C4H9':60, \
             'N2':61, 'He':62, 'Ar':63, 'N-4S':64, 'N-2D':65, \
             'NH':66, 'NH2':67, 'NH3':68, 'NNH':69, 'NO':70, \
             'NO2':71, 'N2O':72, 'NCN':73, 'HNO':74, 'CN':75, \
             'HCN':76, 'H2CN':77, 'HCNN':78, 'HCNO':79, 'HOCN':80, \
             'HNCO':81, 'HON':82, 'NCO':83, 'HNO2':84, 'HONO':85, \
             'NO3':86, 'HONO2':87, 'CH3ONO':88, 'CH3NO2':89, 'CH3NO':90, \
             'C3H7O':91, 'C4H9O':92, 'cC6H6':93, 'N2O3':94, 'NH2OH':95, \
             'N2O4':96, 'N2H2':97, 'N2H3':98, 'N2H4':99, 'HNNO':100, \
             'HNOH':101, 'HNO3':102, 'H2NO':103, 'CNN':104, 'H2CNO':105, \
             'C2N2':106, 'HCNH':107, 'Na':108, 'NaH':109, 'NaO':110, \
             'NaOH':111, 'NaCl':112, 'K':113, 'KH':114, 'KO':115, \
             'KOH':116, 'KCl':117, 'HO2':118, 'SO':119, 'SO2':120, \
             'Cl':121, 'HCl':122, 'ClO':123, 'Cl2':124, 'Ti':125, \
             'TiO':126, 'V':127, 'VO':128, 'Si':129, 'SiH':130, \
             'S':131, 'SH':132, 'H2S':133, 'Mg':134, 'MgH':135, \
             'MgS':136, 'Al':137, 'AlH':138, 'Fe':139, 'FeH':140, \
             'Cr':141, 'CrN':142, 'CrO':143, 'Ca':144, 'F':145, \
             'HF':146, 'Li':147, 'LiCl':148, 'LiH':149, 'LiF':150, \
             'Cs':151, 'CsCl':152, 'CsH':153, 'CsF':154, 'Rb':155, \
             'RbCl':156, 'RbH':157, 'RbF':158, 'P':159, 'PH':160, \
             'PH3':161, 'PO':162, 'P2':163, 'PS':164, 'PH2':165, \
             'P4O6':166 }
