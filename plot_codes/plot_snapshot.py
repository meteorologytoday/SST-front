import xarray as xr
import pandas as pd
import numpy as np
import argparse
import load_helper
import tool_fig_config
import diagnostics
import datetime
import wrf_load_helper 

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input-dir', type=str, help='Input directory.', required=True)
parser.add_argument('--output', type=str, help='Output filename in png.', default="")
parser.add_argument('--extra-title', type=str, help='Title', default="")
parser.add_argument('--blh-method', type=str, help='Method to determine boundary layer height', default=[], nargs='+', choices=['bulk', 'grad'])
parser.add_argument('--SST-rng', type=float, nargs=2, help='Title', default=[14.5, 16.5])
parser.add_argument('--no-display', action="store_true")
parser.add_argument('--plot-check', action="store_true")
parser.add_argument('--exp-beg-time', type=str, help='Title', required=True)
parser.add_argument('--time-rng', type=int, nargs=2, help="Time range in hours after --exp-beg-time", required=True)
args = parser.parse_args()

print(args)

Ri_c = dict(
    bulk = 0.25,
    grad = 0.25,
)

time_beg = np.datetime64(args.exp_beg_time, 's') + np.timedelta64(args.time_rng[0], "h")
time_end = np.datetime64(args.exp_beg_time, 's') + np.timedelta64(args.time_rng[1], "h")



# Loading data
print("Loading wrf dir: %s" % (args.input_dir,))
ds = wrf_load_helper.loadWRFDataFromDir(args.input_dir, prefix="wrfout_d01_", avg=False, time_rng=[time_beg, time_end])
ds = ds.mean(dim=['time', 'south_north', 'south_north_stag'], keep_attrs=True)
print("Done")

Nx = ds.dims['west_east']
Nz = ds.dims['bottom_top']

X_sU = ds.DX * np.arange(Nx+1) / 1e3
X_sT = (X_sU[1:] + X_sU[:-1]) / 2
X_T = np.repeat(np.reshape(X_sT, (1, -1)), [Nz,], axis=0)
X_W = np.repeat(np.reshape(X_sT, (1, -1)), [Nz+1,], axis=0)

Z_W = (ds.PHB + ds.PH) / 9.81
Z_T = (Z_W[1:, :] + Z_W[:-1, :]) / 2

P_total = ds.P + ds.PB

P_sfc = P_total.isel(bottom_top=3)
dP_sfcdx = - (P_sfc[1:] - P_sfc[:-1]) / ds.DX


theta = ds.T + 300.0
zeta = (ds.V[:, 1:] - ds.V[:, :-1]) / ds.DX
SST = ds.TSK - 273.15

"""
print("Compute boundary layer height")
bl = dict()

for method in args.blh_method:
   
    _Ri_c = Ri_c[method] 
    _blh = []
    _Ri = np.zeros((Nz+1, Nx,))
    for i in range(Nx):

        U = (ds.U[:, i+1] + ds.U[:, i]) / 2

        r = diagnostics.getBoundaryLayerHeight(
            U.to_numpy(),
            ds.V[:, i].to_numpy(),
            theta[:, i].to_numpy(),
            ds.QVAPOR[:, i].to_numpy(),
            Z_W[:, i].to_numpy(),
            Ri_c = _Ri_c,
            method=method,
            skip=1,
            debug=True,
        )

        for j, __blh in enumerate(r[0]):
            _blh.append([X_sT[i], __blh])

        _Ri[:, i] = r[1]['Ri']

    _blh = np.array(_blh)

    bl[method] = dict(
        blh = _blh,
        Ri  = _Ri,
    )
"""

print("Loading matplotlib...")
import matplotlib
if args.no_display:
    matplotlib.use('Agg')
else:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
print("Done")

if args.plot_check:

    loc = 250    
    U = (ds.U[:, loc+1] + ds.U[:, loc]) / 2
    h, debug_info = diagnostics.getBoundaryLayerHeight(
        U.to_numpy(),
        ds.V[:, loc].to_numpy(),
        theta[:, loc].to_numpy(),
        ds.QVAPOR[:, loc].to_numpy(),
        Z_W[:, loc],
        Ri_c = 0.25,
        method = args.blh_method,
        skip = 0,
        debug = True,
    )


    fig, ax = plt.subplots(1, 6, figsize=(12, 6), sharey=True)


    ax[0].plot(U,  Z_T[:, loc], label="U")
    ax[0].plot(ds.V[:, loc],  Z_T[:, loc], label="V")
    ax[1].plot(theta[:, loc], Z_T[:, loc], label="$\\theta$")


    if args.blh_method == "bulk":
        ax[2].plot(debug_info['theta_v'], Z_W[:, loc], label="$\\theta_v$")
        ax[3].plot(debug_info['dtheta_v'], Z_W[:, loc], label="$\\partial \\theta_v / \\partial z$")
        ax[4].plot(debug_info['du'], Z_W[:, loc], label="$u_z$")
        ax[4].plot(debug_info['dv'], Z_W[:, loc], label="$v_z$")



    elif args.blh_method == "grad":
        ax[2].plot(debug_info['theta_v'], Z_W[:, loc], label="$\\theta_v$")
        ax[3].plot(debug_info['dtheta_vdz'], Z_W[:, loc], label="$\\partial \\theta_v / \\partial z$")
        ax[4].plot(debug_info['dudz'], Z_W[:, loc], label="$u_z$")
        ax[4].plot(debug_info['dvdz'], Z_W[:, loc], label="$v_z$")
        
    else:
        raise Exception("Unknown keyword: %s" % (args.blh_method,))

    ax[5].plot(debug_info['Ri'], Z_W[:, loc], label="$R_i$", linestyle="dotted")
    ax[5].plot(Ri[:, loc], Z_W[:, loc], label="$R_i$ - 2", linestyle="dashed")
    ax[5].set_xlim([-1, 1])

    for _ax in ax.flatten():
        _ax.legend()
        _ax.grid()

    ax[0].set_ylim([0, 2000])

    plt.show(block=False)

fig, ax = plt.subplots(
    6, 1,
    figsize=(8, 16),
    subplot_kw=dict(aspect="auto"),
    gridspec_kw=dict(height_ratios=[1, 1, 1, 0.2, 0.2, 0.2], right=0.8),
    constrained_layout=False,
    sharex=True,
)

time_fmt="%y/%m/%d %Hh"
fig.suptitle("%sTime: %s ~ %s" % (args.extra_title, time_beg.astype(datetime.datetime).strftime(time_fmt), time_end.astype(datetime.datetime).strftime(time_fmt)))


u_levs = np.linspace(4, 18, 15)
v_levs = np.linspace(0, 5, 21)
w_levs = np.linspace(-5, 5, 21) / 10
theta_levs = np.arange(273, 500, 2)

mappable1 = ax[0].contourf(X_W, Z_W, ds.W * 1e2, levels=w_levs, cmap="bwr", extend="both")

cs = ax[0].contour(X_T, Z_T, theta, levels=theta_levs, colors='k')
plt.clabel(cs)
cax = tool_fig_config.addAxesNextToAxes(fig, ax[0], "right", thickness=0.03, spacing=0.05)
cbar1 = plt.colorbar(mappable1, cax=cax, orientation="vertical")


U = (ds.U[:, :-1] + ds.U[:, 1:]) / 2
mappable1 = ax[1].contourf(X_T, Z_T, U, levels=u_levs, cmap="Spectral_r", extend="both")
cs = ax[1].contour(X_T, Z_T, theta, levels=theta_levs, colors='k')
plt.clabel(cs)
cax = tool_fig_config.addAxesNextToAxes(fig, ax[1], "right", thickness=0.03, spacing=0.05)
cbar1 = plt.colorbar(mappable1, cax=cax, orientation="vertical")


mappable1 = ax[2].contourf(X_T, Z_T, ds.V, levels=v_levs, cmap="Spectral_r", extend="both")
cs = ax[2].contour(X_T, Z_T, theta, levels=theta_levs, colors='k')
plt.clabel(cs)
cax = tool_fig_config.addAxesNextToAxes(fig, ax[2], "right", thickness=0.03, spacing=0.05)
cbar1 = plt.colorbar(mappable1, cax=cax, orientation="vertical")


for method in args.blh_method:
    blh = bl[method]['blh']
    color = dict(grad="lime", bulk="magenta")[method]
    for _ax in ax[0:3].flatten():
        _ax.scatter(blh[:, 0], blh[:, 1], s=2, c=color)
        
        _ax.plot(X_sT, ds.PBLH, color="pink", linestyle="--")


for _ax in ax[0:3].flatten():
    _ax.plot(X_sT, ds.PBLH, color="pink", linestyle="--")


# SST
ax[3].plot(X_sT, SST, 'k-')

# Other information
ax[4].plot(X_sT, P_sfc / 1e2, 'b-')

ax_dPdx = ax[4].twinx()
ax_dPdx.plot(X_sU[1:-1], dP_sfcdx / 1e2 * 1e3, 'r--')

ax_zeta = ax[5].twinx()
ax[5].plot(X_sT, ds.V.isel(bottom_top=2), 'b-')
ax_zeta.plot(X_sU[1:-1], zeta.isel(bottom_top=2), 'r--')

for _ax, color, side in zip([ax[4], ax_dPdx], ['blue', 'red',], ['left', 'right',]):
    _ax.tick_params(color=color, labelcolor=color, axis='y')
    _ax.spines[side].set_color(color)

for _ax, color, side in zip([ax[5], ax_zeta], ['blue', 'red',], ['left', 'right',]):
    _ax.tick_params(color=color, labelcolor=color, axis='y')
    _ax.spines[side].set_color(color)


ax[0].set_title("W [$\\mathrm{cm} / \\mathrm{s}$]")
ax[1].set_title("U [$\\mathrm{m} / \\mathrm{s}$]")
ax[2].set_title("V [$\\mathrm{m} / \\mathrm{s}$]")

for _ax in ax[0:3].flatten():
    _ax.set_ylim([0, 5000])
    _ax.set_ylabel("z [ m ]")


ax[3].set_ylim(args.SST_rng)

ax[0].set_xlim([0, 2000])


ax[3].set_ylabel("SST [ ${}^\\circ\\mathrm{C}$ ]")
ax[4].set_ylabel("$ P_\\mathrm{sfc} $ [ $\\mathrm{hPa}$ ]", color="blue")
ax[5].set_ylabel("$ v_\\mathrm{sfc} $ [ $ \\mathrm{m} / \\mathrm{s}$ ]", color="blue")
ax_zeta.set_ylabel("$ \\zeta_\\mathrm{sfc} $ [ $\\mathrm{s}^{-1}$ ]", color="red")
ax_dPdx.set_ylabel("$ - \\partial P_\\mathrm{sfc} / \\partial x$ [ $ \\mathrm{hPa} / \\mathrm{km}$ ]", color="red")

#cbar1.ax.set_label("[$\\times 10^{-2} \\, \\mathrm{m} / \\mathrm{s}$]")

for _ax in ax.flatten():
    _ax.grid()
    _ax.set_xlabel("[km]")


if args.output != "":
    print("Saving output: ", args.output)
    fig.savefig(args.output, dpi=300)

if not args.no_display:
    print("Showing figure...")
    plt.show()

