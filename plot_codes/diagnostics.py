import numpy as np

M_d = 28.8
M_v = 18.0
epsilon = M_v / M_d
g0 = 9.8

def getVirtualTemperature(T, q):
    return T * ( 1 + q / epsilon ) / (1 + q)
    

def getBoundaryLayerHeight(u, v, theta, q, z_W, Ri_c=0.25, method='grad', skip=1):
   
    if method == 'grad':
        dz_T = z_W[1:] - z_W[:-1]
        dz_W = ( dz_T[1:] + dz_T[:-1] ) / 2
        Ri = getRichardsonNumber(u, v, theta, q, dz_W)

    elif method == 'bulk':
        z_T = ( z_W[1:] + z_W[:-1] ) / 2
        Ri = getBulkRichardsonNumber(u, v, theta, q, z_T, ref=skip)

        
    h = findBoundaryLayerWithRi(z_W, Ri, Ri_c = Ri_c, skip=skip)

    return h

def getBulkRichardsonNumber(u, v, theta, q, z_T, ref=0):

    if len(z_T) != len(u):
        raise Exception("Length of z_T should be the same as u")
    if len(z_T) != len(v):
        raise Exception("Length of z_T should be the same as v")
    if len(z_T) != len(theta):
        raise Exception("Length of z_T should be the same as theta")
    if len(z_T) != len(q):
        raise Exception("Length of z_T should be the same as q")
    
    theta_v = getVirtualTemperature(theta, q)
    dtheta_v = theta_v - theta_v[ref]

    du = u - u[ref]
    dv = v - v[ref]
    
    dU2 = (du**2 + dv**2)
    mask = dU2 == 0
    dU2[mask] = 1.0

    _Ri = (g0 / theta_v) * dtheta_v * z_T / dU2
    _Ri[mask] = 1.0
    
    Ri = np.zeros((len(u)+1,)) # on W-grid
    Ri[1:-1] = (_Ri[1:] + _Ri[:-1] ) / 2
    Ri[0] = Ri[1]
    Ri[-1] = Ri[-2]
    
    #print(_Ri)

    return Ri


def getRichardsonNumber(u, v, theta, q, dz_W):

    if len(dz_W) != len(u) - 1:
        raise Exception("Length of dz_W should be len(u) - 1")

    if len(dz_W) != len(v) - 1:
        raise Exception("Length of dz_W should be len(v) - 1")

    if len(dz_W) != len(theta) - 1:
        raise Exception("Length of dz_W should be len(theta) - 1")

    if len(dz_W) != len(q) - 1:
        raise Exception("Length of dz_W should be len(q) - 1")


    theta_v = getVirtualTemperature(theta, q)
    
    theta_v_mid = ( theta_v[1:] + theta_v[:-1] ) / 2


    dtheta_vdz = (theta_v[1:] - theta_v[:-1]) / dz_W
    dudz = (u[1:] - u[:-1]) / dz_W
    dvdz = (v[1:] - v[:-1]) / dz_W
    dvdz = (v[1:] - v[:-1]) / dz_W

    Ri = np.zeros((len(u)+1,)) # on W-grid
    Ri[1:-1] = (g0 / theta_v_mid) * dtheta_vdz / (dudz**2 + dvdz**2)
    Ri[0] = Ri[1]
    Ri[-1] = Ri[-2]

    return Ri

def findBoundaryLayerWithRi(z_W, Ri, Ri_c = 0.25, skip=1):
    
    if len(z_W) != len(Ri):
        raise Exception("Length of z_w should be the same as Ri.")


    h = np.nan

    for k in range(skip, len(z_W)-1):
        if Ri[k] > Ri_c and Ri[k+1] <= Ri_c:
            h = z_W[k] + (z_W[k+1] - z_W[k]) / (Ri[k+1] - Ri[k])  * ( Ri_c - Ri[k] )

    return h



