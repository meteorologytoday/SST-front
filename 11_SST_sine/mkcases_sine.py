import numpy as np
import os
import json
import f90nml

def pleaseRun(cmd):

    print(">> ", cmd)
    os.system(cmd)

lab_name = "lab_sine"

ref_WRF_root = "/home/t2hsu/projects/WRF_frontcases/01_various_SST_front_wavelength/WRF-4.3.3_em_quarter_ss"
ref_namelist = "namelist.input"
ref_caserundir = "%s/test/em_quarter_ss" % ( ref_WRF_root,)
ref_softlink_run_dir = "%s/run" % (ref_WRF_root,)
ref_softlink_main_dir = "%s/main" % (ref_WRF_root,)

# Needed files for running idealized model
ref_softlinks = [
    "bulkdens.asc_s_0_03_0_9",
    "bulkradii.asc_s_0_03_0_9",
    "capacity.asc",
    "coeff_p.asc",
    "coeff_q.asc",
    "constants.asc",
    "kernels.asc_s_0_03_0_9",
    "kernels_z.asc",
    "masses.asc",
    "termvels.asc",
]


ref_softlinks_exes = ["ideal.exe", "wrf.exe"]


bl_scheme_mapping = dict(
    YSU    = 1,
    MYNN25 = 5,
    MYNN3  = 6,
)

# option: no_mp_heating
mp_heating_mapping = dict(
    on  = 0,
    off = 1,
)

#Us    = np.array([0.0, 5.0, 10.0, 15.0])
Us    = np.array([15.0])
f0    = 1e-4
T0    = 273.15 + 15.0
dTs    = np.linspace(0, 1.0, 11)
bl_scheme = ["MYNN25",]
mp_heating = ["off"]
#Lxs = np.array([50, 100, 200, 500,], dtype=float) * 1e3
Lxs = np.array([100,], dtype=float) * 1e3

dx = 2000.0 # 2km
dy = 2000.0 # 2km


# parallelization
parallel_N = 4


sim_cases = []


nml = f90nml.read(ref_namelist)

#dx = nml['domains']['dx']
#dy = nml['domains']['dy']

#Nx = nml['domains']['e_we'][0] - 1
#Ny = nml['domains']['e_sn'][0] - 1

# Setup cases configuration
for i, dT in enumerate(dTs):
    for j, Lx in enumerate(Lxs):
        for k, U in enumerate(Us):
            for m, _bl_scheme in enumerate(bl_scheme):
                for n, _mp_heating in enumerate(mp_heating):


                    if Lx % dx != 0:
                        raise Exception("Lx mod dx != 0. We get: Lx=%f, dx=%f" % (Lx, dx))

                    sim_cases.append({
                        'casename' : "case_mph-%s_Lx%03d_U%02d_dT%03d_%s" % (_mp_heating, int(Lx/1e3), U, dT*1e2, _bl_scheme),
                        'T0'         : T0,
                        'dT'         : dT,
                        'Lx'         : Lx,
                        'dx'         : dx,
                        'Nx'         : int(Lx / dx),
                        'U'          : U,
                        'f0'         : f0,
                        'bl_scheme'  : _bl_scheme,
                        'mp_heating' : _mp_heating,
                    })


# Generate vertical profiles

def getSoundingFilename(U):
    return "sounding_files/sounding_U%d.ref" % (U,)
            
for U in Us:
    print("Generate vertical profile of U=%d" % (U,))
    filename = getSoundingFilename(U)
    if os.path.exists(filename):
        print("File %s already exist." % filename)
    else:
        print("File %s does not exist. Generate it now..." % (filename,) )
        pleaseRun("gen_sounding.sh %d" % (U,))

# Generate cases
for i, sim_case in enumerate(sim_cases):

    print("Generating case %d : %s" % (i, sim_case['casename'], ))

    case_folder = '%s/%s' % (lab_name, sim_case['casename'],)

    if os.path.isdir(case_folder):
        print("Folder %s already exists. Skip it!" % (case_folder,))
    else:
        
        print("Folder %s not exists. Make it!" % (case_folder,))

        pleaseRun("mkdir -p %s" % (case_folder,) )

        for fname in ref_softlinks:
            pleaseRun("ln -s %s/%s %s/" % (ref_softlink_run_dir, fname, case_folder))

        for fname in ref_softlinks_exes:
            pleaseRun("ln -s %s/%s %s/" % (ref_softlink_main_dir, fname, case_folder))


        sounding_filename = getSoundingFilename(sim_case["U"])
        pleaseRun("cp %s %s/input_sounding" % (sounding_filename, case_folder,))

        pleaseRun("cp tools/* %s/" % (case_folder,))
        pleaseRun("cp %s %s/namelist_unmodified.input" % (ref_namelist, case_folder,))

        pleaseRun("f90nml -p -g physics -v bl_pbl_physics=%d -v no_mp_heating=%d %s/namelist_unmodified.input > %s/namelist.tmp" % (bl_scheme_mapping[sim_case['bl_scheme']], mp_heating_mapping[sim_case['mp_heating']], case_folder, case_folder))
        
        pleaseRun("f90nml -p -g domains -v e_we=%d -v dx=%f %s/namelist.tmp > %s/namelist.input" % (
            sim_case["Nx"] + 1,
            sim_case["dx"],
            case_folder,
            case_folder,
        ))

        # Write settings
        with open('%s/run_setting.json' % (case_folder,), 'w', encoding='utf-8') as f:
            json.dump(sim_case, f, ensure_ascii=False, indent=4)

