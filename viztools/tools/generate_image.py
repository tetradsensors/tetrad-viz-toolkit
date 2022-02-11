import numpy as np
from .colors import get_gyor_color_gradient
from PIL import Image
from scipy import interpolate
from scipy.ndimage import zoom
import geopy.distance
import matplotlib as mpl
from matplotlib import cm

def _resize_mat(mat, size):
    """
    size: new size - (rows, cols)
    """

    assert mat.ndim == 2

    rows, cols = mat.shape

    rows_zm = size[0] / rows
    cols_zm = size[1] / cols

    return zoom(mat, [rows_zm, cols_zm]) 


def _var_to_alpha(var, opac95=3, opac05=12):
    """
    var: the 2D variance matrix
    opac95: threshold we want 95% opacity
    opac05: threshold we want 05% opacity

    Note: Using a reflected sigmoid to do the calculation
    """
    assert opac95 < opac05
    opac50 = opac95 + (opac05 - opac95) / 2
    s1 = 2.944444 * 2
    scale = s1 / (opac05 - opac95)
    out = 1 - (1. / (1. + np.exp(-scale * (var - opac50))))
    return (256 * out).clip(0, 255).astype(np.uint8)


def _snapshot_to_img(obj, size=None, format='png', scaling='epa', opac95=3, opac05=12, colormap='auto'):
    """
    obj: the estimate map dictionary (keys: lat, lon, alt, pm, var)
    filename: output filename
    size: if you want to resize (width, height)
    format: png, jpg, etc.
    scaling: the color gradient scaling
        "epa": anchors at 12, 35, etc.
        "aqi": anchors at 50, 100, 150, ...
        "linear": smooth scaling from green to purple
    opac95: 95% opacity value for alpha
    opac05: 05% opacity value for alpha
    """

    pm  = np.array(obj.vals)
    var = np.array(obj.vars)

    rgba = np.zeros((*pm.shape, 4), dtype=np.uint8)

    if colormap == 'auto':
        gradient = get_gyor_color_gradient('epa')
        
        # Convert the z-values to RGB
        g = np.array(gradient)
        pmi = pm.astype(int)
        for i in range(3):
            rgba[:, :, i] = g[:, i][pmi]
    else:
        # print(f'[_snapshot_to_img]: using {colormap}')
        cmap = cm.get_cmap(colormap)
        norm = mpl.colors.Normalize(vmin=0, vmax=40)
        rgba = cmap(norm(pm)) * 256

    # Alpha scaling
    rgba[:, :, -1] = _var_to_alpha(var, opac95, opac05)

    if size:
        sz = size[::-1]
        resized = np.zeros((*sz, 4))
        for i in range(4):
            resized[:, :, i] = _resize_mat(rgba[:, :, i], sz)
        rgba = resized.clip(0, 255).astype(np.uint8)
    
    # flip over x-axis for latitude getting bigger as we go up
    # rgba = rgba[::-1, :, :]

    img = Image.fromarray(rgba, "RGBA")
    return img


def _snapshot_to_img_dist_scaled(obj,
                                 largest_size=None, 
                                 format='png', 
                                 scaling='epa', 
                                 opac95=3, 
                                 opac05=12,
                                 colormap='auto'):
    """
    Takes into consideration the ratio between lat/lon distance and scales the output image accordingly.
    largest_size: the output won't be larger than this many pixels on either height or width. If None then we will scale UP instead
    """

    lat_min = obj.lats.min()
    lat_max = obj.lats.max()
    lon_min = obj.lons.min()
    lon_max = obj.lons.max()

    lat_dist_m = geopy.distance.distance((lat_min, lon_max), (lat_max, lon_max)).km
    lon_dist_m = geopy.distance.distance((lat_max, lon_min), (lat_max, lon_max)).km

    ratio = lat_dist_m / lon_dist_m

    if largest_size:
        if lat_dist_m > lon_dist_m:
            # this is image size, so we give it in (width x height)
            size = (int(largest_size / ratio), largest_size)
        else:
            size = (largest_size, int(largest_size / ratio))
    
    # Otherwise let's scale up instead of down
    else:
        lat_sz, lon_sz = len(obj.lats), len(obj.lons)

        if lat_dist_m > lon_dist_m:
            size = (lat_sz, int(lon_sz * ratio))
        else:
            size = (int(lat_sz * ratio), lon_sz)

    return _snapshot_to_img(obj,
                            size=size, 
                            format=format, 
                            scaling=scaling, 
                            opac95=opac95, 
                            opac05=opac05,
                            colormap=colormap)










