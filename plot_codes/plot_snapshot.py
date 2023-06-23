import xarray as xr
import pandas as pd
import numpy as np
import argparse
import load_helper
import tool_fig_config
import diagnostics

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--wrfout', type=str, help='Input directory.', required=True)
parser.add_argument('--output', type=str, help='Output filename in png.', default="")
parser.add_argument('--title', type=str, help='Title', default="")
parser.add_argument('--blh-method', type=str, help='Method to determine boundary layer height', default=["grad", "bulk"], nargs='+', choices=['bulk', 'grad'])
parser.add_argument('--SST-rng', type=float, nargs=2, help='Title', default=[14.5, 16.5])
parser.add_argument('--no-display', action="store_true")
parser.add_argument('--plot-check', action="store_true")
parser.add_argument('--time-idx', type=int, nargs=2, required=True)
args = parser.parse_args()

print(args)

# Loading data
print("Loading file: %s" % (args.wrfout,))
ds = load_helper.loadWRFData(args.wrfout)
print("Done")


ds = ds.isel(time=slice(args.time_idx[0], args.time_idx[1]+1)).mean(dim=['time', 'south_north', 'south_north_stag'], keep_attrs=True)

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
dP_sfcdx = (P_sfc[1:] - P_sfc[:-1]) / ds.DX


theta = ds.T + 300.0
zeta = (ds.V[:, 1:] - ds.V[:, :-1]) / ds.DX
SST = ds.TSK - 273.15


print("Compute boundary layer height")
bl = dict()


for method in args.blh_method:
    
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
            Ri_c = 0.25,
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
    4, 1,
    figsize=(8, 8),
    subplot_kw=dict(aspect="auto"),
    gridspec_kw=dict(height_ratios=[1, 0.2, 0.2, 0.2], right=0.8),
    constrained_layout=False,
    sharex=True,
)

if args.title == "":
    fig.suptitle(args.wrfout)
else:
    fig.suptitle(args.title)

w_levs = np.linspace(-5, 5, 21) / 10
theta_levs = np.arange(273, 500, 2)

mappable1 = ax[0].contourf(X_W, Z_W, ds.W * 1e2, levels=w_levs, cmap="bwr", extend="both")

cs = ax[0].contour(X_T, Z_T, theta, levels=theta_levs, colors='k')
plt.clabel(cs)


#cs = ax[0].contour(X_W, Z_W, Ri_grad, levels=[0.1, 0.25, 0.5, 0.75, 1.0], colors='green', linestyles='dashed', linewidths=1)
#plt.clabel(cs)

#ax[0].plot(X_sT, blh_grad, linestyle='solid', color="lime")
#ax[0].plot(X_sT, blh_bulk, linestyle='solid', color="magenta")

#ax[0].scatter(blh_grad[:, 0], blh_grad[:, 1], s=5, c="lime")

for method in args.blh_method:
    blh = bl[method]['blh']
    color = dict(grad="lime", bulk="cyan")[method]
    ax[0].scatter(blh[:, 0], blh[:, 1], s=2, c=color)

cax = tool_fig_config.addAxesNextToAxes(fig, ax[0], "right", thickness=0.03, spacing=0.05)
cbar1 = plt.colorbar(mappable1, cax=cax, orientation="vertical")

ax[1].plot(X_sT, SST, 'k-')
ax[2].plot(X_sT, P_sfc / 1e2, 'b-')

ax_dPdx = ax[2].twinx()
ax_dPdx.plot(X_sU[1:-1], dP_sfcdx / 1e2 * 1e3, 'r--')

ax_zeta = ax[3].twinx()
ax[3].plot(X_sT, ds.V.isel(bottom_top=2), 'b-')
ax_zeta.plot(X_sU[1:-1], zeta.isel(bottom_top=2), 'r--')

for _ax, color, side in zip([ax[2], ax_dPdx], ['blue', 'red',], ['left', 'right',]):
    _ax.tick_params(color=color, labelcolor=color, axis='y')
    _ax.spines[side].set_color(color)

for _ax, color, side in zip([ax[3], ax_zeta], ['blue', 'red',], ['left', 'right',]):
    _ax.tick_params(color=color, labelcolor=color, axis='y')
    _ax.spines[side].set_color(color)




ax[0].set_title("W [$\\mathrm{cm} / \\mathrm{s}$]")

ax[1].set_ylim(args.SST_rng)
ax[0].set_ylim([0, 5000])

ax[0].set_xlim([0, 2000])

ax[0].set_ylabel("z [ m ]")
ax[1].set_ylabel("SST [ ${}^\\circ\\mathrm{C}$ ]")
ax[2].set_ylabel("$ P_\\mathrm{sfc} $ [ $\\mathrm{hPa}$ ]", color="blue")
ax[3].set_ylabel("$ v_\\mathrm{sfc} $ [ $ \\mathrm{m} / \\mathrm{s}$ ]", color="blue")
ax_zeta.set_ylabel("$ \\zeta_\\mathrm{sfc} $ [ $\\mathrm{s}^{-1}$ ]", color="red")
ax_dPdx.set_ylabel("$\\partial P_\\mathrm{sfc} / \\partial x$ [ $ \\mathrm{hPa} / \\mathrm{km}$ ]", color="red")


cbar1.ax.set_label("[$\\times 10^{-2} \\, \\mathrm{m} / \\mathrm{s}$]")

for _ax in ax.flatten():
    _ax.grid()
    _ax.set_xlabel("[km]")


if args.output != "":
    print("Saving output: ", args.output)
    fig.savefig(args.output, dpi=300)

if not args.no_display:
    print("Showing figure...")
    plt.show()

