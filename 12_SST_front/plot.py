import xarray as xr
import pandas as pd
import numpy as np



casename = "case%02d" % (1,)
expdir = "lab"
data_file = "wrfout_d01_0001-01-01_00:00:00"
idx_z = 5
stat_xrng = np.array([200, 500])

# Loading data
data_file_full = "%s/%s/%s" % (expdir, casename, data_file)
print("Loading file: %s" % (data_file_full,))
ds = xr.open_dataset(data_file_full, engine='scipy')

#times = pd.Timestamp(["%s %s" % (t[0:10], t[11:19]) for t in ds.Times.astype(str).to_numpy()])
times = [pd.Timestamp("%s %s" % (t[0:10], t[11:19])) for t in ds.Times.astype(str).to_numpy()]

Nx = ds.dims['west_east']
Nz = ds.dims['bottom_top']

# Eta value on T grid
eta_T = ds.ZNU[0, :]
eta_W = ds.ZNW[0, :]

print("Selected idx_z=%d  ->  eta = %f" % (idx_z, eta_T[idx_z]))


X = ds.DX * np.arange(Nx) / 1e3


stat_xidx = (X >= stat_xrng[0]) & (X <= stat_xrng[1])



for t in [0, 10, 100, 200]:
    W = np.mean(ds.W[t, idx_z:idx_z+1, 0, :], axis=0) 
    Q = ds.QVAPOR[t, idx_z, 0, :]

    W_mean = np.mean(W)
    Q_mean = np.mean(Q)

    W_eddy = W - W_mean
    Q_eddy = Q - Q_mean

    WQ_mean = W_mean * Q_mean
    WQ_eddy = np.mean(W_eddy * Q_eddy)

    t_str = times[t].strftime("%H:%M")

    print("At t=%s , WQ_mean = %.2e, WQ_eddy = %.2e" % (t_str, WQ_mean, WQ_eddy,))



import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


fig, ax = plt.subplots(3, 1, figsize=(8, 6), gridspec_kw={'hspace': 0.4})

fig.suptitle(casename)

for t in [0, 10, 100, 200]:
    W = np.mean(ds.W[t, idx_z:idx_z+1, 0, :], axis=0)  * 1e2
    Q = ds.QVAPOR[t, idx_z, 0, :] * 1e3
    ax[0].plot(X, W, label=times[t].strftime("%H:%M"))
    ax[1].plot(X, Q, label=times[t].strftime("%H:%M"))


ax[0].set_title("W")
ax[1].set_title("QVAPOR")
ax[2].set_title("Skin Temperature")

ax[0].legend()

ax[2].plot(X, ds.TSK[10, 0, :] - 273.15)

ax[0].set_ylim([-5, 5])
ax[1].set_ylim([6, 7])
    
ax[0].set_ylabel("[$\\times 10^{-2} \\, \\mathrm{m} / \\mathrm{s}$]")
ax[1].set_ylabel("[$\\mathrm{g} / \\mathrm{kg}$]")
ax[2].set_ylabel("[${}^\\circ\\mathrm{C}$]")

for _ax in ax.flatten():
    _ax.grid()
    _ax.set_xlabel("[km]")
    #_ax.set_xlim([0, 1600])


fig.savefig("figures/%s.png" % (casename,), dpi=300)

plt.show()





