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
parser.add_argument('--SST-rng', type=float, nargs=2, help='Title', default=[14.5, 16.5])
parser.add_argument('--no-display', action="store_true")
parser.add_argument('--time-idx', type=int, nargs=2, required=True)
args = parser.parse_args()

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
blh_grad = np.zeros((Nx,))
blh_bulk = np.zeros((Nx,))

for i in range(len(blh_grad)):

    U = (ds.U[:, i+1] + ds.U[:, i]) / 2
 
    blh_grad[i] = diagnostics.getBoundaryLayerHeight(
        U.to_numpy(),
        ds.V[:, i].to_numpy(),
        theta[:, i].to_numpy(),
        ds.QVAPOR[:, i].to_numpy(),
        Z_W[:, i].to_numpy(),
        Ri_c = 0.25,
        method='grad',
        skip=1,
    )
  
     
    blh_bulk[i] = diagnostics.getBoundaryLayerHeight(
        U.to_numpy(),
        ds.V[:, i].to_numpy(),
        theta[:, i].to_numpy(),
        ds.QVAPOR[:, i].to_numpy(),
        Z_W[:, i].to_numpy(),
        Ri_c = 0.25,
        method='bulk',
        skip=1,
    )

    #print("[%d] : %f" % (i, blh_bulk[i]))
    


print("Loading matplotlib...")
import matplotlib
if args.no_display:
    matplotlib.use('Agg')
else:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
print("Done")

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

ax[0].plot(X_sT, blh_grad, linestyle='solid', color="lime")
ax[0].plot(X_sT, blh_bulk, linestyle='solid', color="magenta")

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

