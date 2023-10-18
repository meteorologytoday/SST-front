import numpy as np
import xarray as xr
import json

def gaussian(xx, yy, xc, yc, sigma):
    
    return np.exp( - ( ( (xx - xc)**2 + (yy - yc)**2 ) / sigma**2 / 2 ) )

def SST_shape(XXC, YYC, begin_X, cent_Y, dT, wid, spacing, wpkt):
    
    TSK = np.zeros_like(XXC)

    for i in range(wpkt):
    
        cent_X = begin_X + i * spacing

        TSK += dT * gaussian(XXC, YYC, cent_X, cent_Y, wid);

    return TSK



input_filename = "wrfinput_d01.backup"
output_filename = "wrfinput_d01"
setting_filename = "run_setting.json"


ds = xr.open_dataset(input_filename, engine='scipy')

ds.LU_INDEX[:, :, :] = 16


_, Ny, Nx = ds.TSK.shape

with open(setting_filename, "r") as f:
    setting = json.load(f)

T0 = setting['T0']
dT = setting['dT']
wid = setting['wid']
begin_X = setting['begin_X']
cent_Y  = setting['cent_Y']
wpkt    = setting['wpkt']

YC = ds.DY * ( np.arange(Ny) + 0.5 )
XC = ds.DX * ( np.arange(Nx) + 0.5 )

YYC, XXC = np.meshgrid(YC, XC, indexing='ij')


TSK = T0 + SST_shape(XXC, YYC, begin_X, cent_Y, dT, wid, 4*wid, wpkt)
ds.TSK[0, :, :] = TSK

ds['F'][:] = setting['f0']
ds['E'][:] = 0


print("Output file : ", output_filename)
ds.to_netcdf(output_filename)
