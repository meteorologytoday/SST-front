import xarray as xr
import pandas as pd
import numpy as np
import argparse
import tool_fig_config
import diagnostics
import wrf_load_helper 
import datetime

# Air density
Rd = 287.053 # J / K / kg
cp = 1004    # J / K / kg
T0 = 300.0 # Base theta_0  (K)
p0 = 1e5 # Reference pressure (Pa)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input-dir', type=str, help='Input directories.', required=True)
parser.add_argument('--output', type=str, help='Output filename in png.', default="")
parser.add_argument('--title', type=str, help='Suptitle of the figure', default="")
parser.add_argument('--title-template', type=str, help='Suptitle of the figure', default="")
parser.add_argument('--exp-beg-time', type=str, help='analysis beg time', required=True)
parser.add_argument('--timestep', type=int, help='analysis beg time', required=True)
parser.add_argument('--time-rng', type=int, nargs=2, help="Time range in hours after --exp-beg-time", required=True)
parser.add_argument('--no-display', action="store_true")
parser.add_argument('--overlay', action="store_true")

args = parser.parse_args()

print(args)

exp_beg_time = pd.Timestamp(args.exp_beg_time)

time_beg = exp_beg_time + pd.Timedelta(hours=args.time_rng[0])
time_end = exp_beg_time + pd.Timedelta(hours=args.time_rng[1])


# =================================================================


def computeBudget(dt, timestep_seconds):

    # Loading data
    timestep_timedelta = pd.Timedelta(seconds=timestep_seconds)
    time_rng = [ dt - timestep_timedelta, dt + timestep_timedelta + pd.Timedelta(seconds=1)]
    print("Start loading data.")
    
    ds = wrf_load_helper.loadWRFDataFromDir(
        args.input_dir,
        prefix="wrfout_d01_",
        avg=False,
        time_rng=time_rng,
        extend_time = pd.Timedelta(hours=1),
        verbose=True,
    )
    
    ds = ds.mean(dim=['south_north', 'south_north_stag'], keep_attrs=True)
  
    print(ds.coords["time"])
 
    selected_time = [
        dt - timestep_timedelta
    ]

    Nx = ds.dims['west_east']
    Nz = ds.dims['bottom_top']
    
    dX   = ds.DX
    X_sU = dX * np.arange(Nx+1)
    X_sT = (X_sU[1:] + X_sU[:-1]) / 2
    X_T = np.repeat(np.reshape(X_sT, (1, -1)), [Nz,], axis=0)
    X_W = np.repeat(np.reshape(X_sT, (1, -1)), [Nz+1,], axis=0)
    
    ETA_W = ds.ZNW.to_numpy()[0, :]
    ETA_T = ds.ZNU.to_numpy()[0, :]

    Z_W = (ds.PHB + ds.PH).to_numpy() / 9.81
    Z_T = (Z_W[:, 1:, :] + Z_W[:, :-1, :]) / 2
    dZ_T = Z_W[:, 1:, :] - Z_W[:, :-1, :]
    dZ_W = np.zeros_like(Z_W)
    dZ_W[:, 1:-1, :] = (dZ_T[:, :-1, :] + dZ_T[:, 1:, :]) / 2.0
    dZ_W[:,  0, :] = dZ_W[:,  1, :]
    dZ_W[:, -1, :] = dZ_W[:, -2, :]
     
    # Create empty DataArray
    merge_data = []
    da_empty = xr.DataArray(
        data = np.zeros((1, Nz, Nx), dtype=np.float64),
        dims=["time", "z", "x"],
        coords=dict(
            X=(["x",], X_sT),
            ETA=(["z",], ETA_T),
            time=[dt,],
            reference_time=pd.Timestamp("2001-01-01"),
        ),
    )
 
    # Compute some common variables
    U_U = ds["U"].to_numpy()
    U_T = ( U_U[:, :, 1:] + U_U[:, :, :-1] ) / 2
 
    W_W = ds["W"].to_numpy()
    W_T = ( W_W[:, 1:, :] + W_W[:, :-1, :] ) / 2
 
    U_W = W_W.copy()
    U_W[:, 1:-1, :] = (U_T[:, :-1, :] + U_T[:, 1:, :]) / 2
    U_W[:, 0, :] = U_W[:, 1, :]
    U_W[:, -1, :] = U_W[:, -2, :]


    P_U = U_U.copy()
    P_U[:, :, 1:-1] = ( ds["P"][:, :, 1:] + ds["P"][:, :, :-1] ) / 2
    P_U[:, :, 0] = P_U[:, :, 1]
    P_U[:, :, -1] = P_U[:, :, -2]

    W_da = da_empty.copy().rename("W_T")
    W_da[:] = W_T[1, :, :]
    merge_data.append(W_da)


    P_T = (ds["P"] + ds["PB"]).to_numpy()
    THETA = (ds["T"] + T0).to_numpy()
    RHO = p0 / (Rd * THETA) * ( (P_T / p0)**(1 - Rd/cp) )

    print(RHO[1, 0, :])

    # Compute du/dt
    dUdt = (U_T[2, :, :] - U_T[0, :, :]) / (2 * timestep_seconds)
    dUdt_da = da_empty.copy().rename("dUdt_T")
    dUdt_da[:] = dUdt
    merge_data.append(dUdt_da)

    # Compute dudx
    dUdX_T = (U_U[1, :, 1:] - U_U[1, :, :-1]) / dX
    dUdX_U = (U_U[1, :, 1:] - U_U[1, :, :-1]) / dX
    dUdX_da = da_empty.copy().rename("dUdX_T")
    dUdX_da[:] = dUdX_T
    merge_data.append(dUdX_da)

    # Compute Ududx
    dUdX_U = np.zeros_like(U_U)
    dUdX_U[:, :, 1:-1] = (U_U[:, :, 2:] - U_U[:, :, :-2]) / (2*dX)
    dUdX_U[:, :, 0]  = dUdX_U[:, :, 1]
    dUdX_U[:, :, -1] = dUdX_U[:, :, -2]

    # old way
    #UdUdX_T = U_T[1, :, :] * dUdX_T

    # new way
    UdUdX_U = U_U * dUdX_U
    UdUdX_T = (UdUdX_U[:, :, 1:] + UdUdX_U[:, :, :-1]) / 2
    UdUdX_da = da_empty.copy().rename("UdUdX_T")
    UdUdX_da[:] = UdUdX_T[1, :, :]
    merge_data.append(UdUdX_da)

    # Compute dudz
    dUdZ_T = (U_W[1, 1:, :] - U_W[1, :-1, :]) / dZ_T[1, :, :]
    dUdZ_da = da_empty.copy().rename("dUdZ_T")
    dUdZ_da[:] = dUdZ_T
    merge_data.append(dUdZ_da)

    # Compute wdudz
    dUdZ_T = (U_U[1, :, 1:] - U_U[1, :, :-1]) / dZ_T[1, :, :]
    WdUdZ_T = W_T[1, :, :] * dUdZ_T
    WdUdZ_da = da_empty.copy().rename("WdUdZ_T")
    WdUdZ_da[:] = WdUdZ_T
    merge_data.append(WdUdZ_da)

    # Compute fv
    f_T = ds["F"].to_numpy()  # time, X
    V_T = ds["V"].to_numpy()  # time, Z, X
    fV_T = f_T[:, None, :] * V_T

    fV_da = da_empty.copy().rename("fV_T")
    fV_da[:] = fV_T[1, :, :]
    merge_data.append(fV_da)

    # Compute dpdx
    dPdX_U = np.zeros_like(U_U)
    dPdX_U[:, :, 1:-1] = (P_T[:, :, 1:] - P_T[:, :, :-1]) / dX
    dPdX_U[:, :, 0]  = dPdX_U[:, :, 1]
    dPdX_U[:, :, -1] = dPdX_U[:, :, -2]
    dPdX_T = (dPdX_U[:, :, 1:] + dPdX_U[:, :, :-1]) / 2


    #dPdX_T = (P_U[1, :, 1:] - P_U[1, :, :-1]) / dX
    dPdX_da = da_empty.copy().rename("dPdX_T")
    dPdX_da[:] = dPdX_T[1, :, :]
    merge_data.append(dPdX_da)

    # Compute turbulent stress
    dUdZ_W = np.zeros_like(W_W)
    dUdZ_W[:, 1:-1, :] = U_T[:, 1:, :] - U_T[:, :-1, :]
    dUdZ_W /= dZ_W
    
    FLUX_W = dUdZ_W * ds["EXCH_M"].to_numpy()
    RNLDSTRS_T = ( FLUX_W[:, 1:, :] - FLUX_W[:, :-1, :] ) / dZ_T
    RNLDSTRS_da = da_empty.copy().rename("RNLDSTRS_T")
    RNLDSTRS_da[:] = RNLDSTRS_T[1, :, :]
    merge_data.append(RNLDSTRS_da)

    # Compute dw/dt
    W_W = ds["W"].to_numpy()
    W_T = ( W_W[:, 1:, :] + W_W[:, :-1, :] ) / 2
    dWdt = (W_T[2, :, :] - W_T[0, :, :]) / (2 * timestep_seconds)
    dWdt_da = da_empty.copy().rename("dWdt_T")
    dWdt_da[:] = dWdt
    merge_data.append(dWdt_da)


    # Compute dvdx

    # Compute dudz

    # Compute Umom_res
    Umom_res = dUdt_da + UdUdX_da + WdUdZ_da - fV_da + dPdX_da / RHO[1:2, :, :] - RNLDSTRS_da
    Umom_res = Umom_res.rename("Umom_res")
    merge_data.append(Umom_res)

    ds = xr.merge(merge_data)

    
    return ds


ds = computeBudget(time_beg, args.timestep)


print("Loading matplotlib...")
import matplotlib
if args.no_display:
    matplotlib.use('Agg')
else:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
print("Done")


z_idx = 5
ds = ds.isel(time=0, z=z_idx)

#def plot_variables(varnames, scau)
varnames = [
    ("dUdt_T",      "+"),
    ("UdUdX_T",     "-"),
    ("WdUdZ_T",     "-"),
    ("fV_T",        "+"), 
    ("dPdX_T",      "-"),
    ("RNLDSTRS_T",  "+"),
    ("Umom_res",    "+"),
]


fig, ax = plt.subplots( ( 1 if args.overlay else len(varnames) ), 1, figsize=(10, 6), sharex=True, squeeze=False)
x = ds.coords['X'] / 1e3

title = args.title

if args.title_template == "time":
    title = pd.Timestamp(ds.time.to_numpy().item()).strftime("Date: %d %H:%M:%S")
    print(title)

fig.suptitle(title)

for i, (varname, sign) in enumerate(varnames):
    
    if args.overlay:
        _ax = ax[0, 0]
    else:
        _ax = ax[i, 0]
        _ax.set_title(varname)

    _sign = None
    if sign == "+":
        _sign = 1.0
        _sign_str = ""
    elif sign == "-":
        _sign = -1.0
        _sign_str = "- "

    _ax.plot(x, _sign * ds[varname], label="%s%s" % (_sign_str, varname))

    _ax.grid()
    _ax.set_ylim(np.array([-1, 1]) * 1e-3)
    _ax.set_ylabel("[ $\\mathrm{m} / \\mathrm{s}^2 $ ]")


if args.overlay:
    ax[0, 0].legend(loc="lower left")
    
ax[-1, 0].set_xlabel("[ $\\mathrm{km}$ ]")

ax[0, 0].set_xlim([0, 1000])

plt.show()

if args.output != "":
    print("Saving output: ", args.output)
    fig.savefig(args.output, dpi=300)


