import f90nml
import numpy as np
import os
import json

def pleaseRun(cmd):

    print(">> ", cmd)
    os.system(cmd)

lab_name = "lab_front"
overwrite = False
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

sounding_profiles = dict(
    wML   = "input_sounding_wML.ref",
    woML  = "input_sounding_woML.ref",
)

bl_scheme_mapping = dict(
    YSU   = 1,
    MYNN3 = 6,
)


f0    = 1e-4
T0    = 273.15 + 15.0
dTs    = np.linspace(3.0, -3.0, 7)
wids   = np.array([50,]) * 1e3
bl_scheme = ["YSU", "MYNN3"]
ML = ["wML", "woML"]


begin_X = 500e3

# parallelization
parallel_N = 20


sim_cases = []


nml = f90nml.read(ref_namelist)

dx = nml['domains']['dx']
dy = nml['domains']['dy']

Nx = nml['domains']['e_we'][0] - 1
Ny = nml['domains']['e_sn'][0] - 1

# Setup cases configuration
for i, dT in enumerate(dTs):
    for j, wid in enumerate(wids):
        for l, _ML in enumerate(ML):
            for m, _bl_scheme in enumerate(bl_scheme):
                sim_cases.append({
                    'casename' : "case_dT%03d_wid%03d_%s_%s" % (dT*1e2, wid/1e3, _ML, _bl_scheme,),
                    'begin_X'    : begin_X,
                    'T0'         : T0,
                    'dT'         : dT,
                    'wid'        : wid,
                    'f0'         : f0,
                    'ML'         : _ML,
                    'bl_scheme'  : _bl_scheme,
                })

with open("run_all_front.sh", "w") as f_runall:

    f_runall.write("#!/bin/bash\n")

    # Generate cases
    for i, sim_case in enumerate(sim_cases):

        print("Generating case %d : %s" % (i, sim_case['casename'], ))

        case_folder = '%s/%s' % (lab_name, sim_case['casename'],)

        if os.path.exists(case_folder):

            if not overwrite:
                print("Case folder %s exists and overwrite is False. Skip it")
                continue 
            else:
                print("Case folder %s exists and overwrite is True. Remove the case and recreate it.")

        pleaseRun("rm -rf %s" % (case_folder,) )
        pleaseRun("mkdir -p %s" % (case_folder,) )

        f_runall.write("( echo \"Running case %s \" ; cd %s ; bash ./run_front.sh ) & \n" % (sim_case["casename"], case_folder, ))
        f_runall.write("pid[%d]=$!\n" % (i,))
        
        if i > 0 and i % parallel_N == 0:
            f_runall.write("wait\n")
            

        for fname in ref_softlinks:
            pleaseRun("ln -s %s/%s %s/" % (ref_softlink_run_dir, fname, case_folder))

        for fname in ref_softlinks_exes:
            pleaseRun("ln -s %s/%s %s/" % (ref_softlink_main_dir, fname, case_folder))

        pleaseRun("cp %s %s/input_sounding" % (sounding_profiles[sim_case['ML']], case_folder))

        pleaseRun("cp tools/* %s/" % (case_folder,))
        pleaseRun("cp %s %s/namelist_unmodified.input" % (ref_namelist, case_folder,))

        pleaseRun("f90nml -p -g physics -v bl_pbl_physics=%d %s/namelist_unmodified.input > %s/namelist.input" % (bl_scheme_mapping[sim_case['bl_scheme']], case_folder, case_folder))

        # Write settings
        with open('%s/run_setting.json' % (case_folder,), 'w', encoding='utf-8') as f:
            json.dump(sim_case, f, ensure_ascii=False, indent=4)


    f_runall.write("wait\n")
    f_runall.write("pid_str=$(IFS=\" \"; echo \"${pid[*]}\")\n") 
    f_runall.write("echo \"Going to trap kill: \" $pid_str\n")
    #f_runall.write("trap \"kill %s; exit 1\" INT\n" % (" ".join(["${pid[%i]}" % (i,) for i in range(len(sim_cases))]), )) 
    f_runall.write("trap \"kill $pid_str; exit 1\" INT\n")
    f_runall.write("wait\n")


      




 
