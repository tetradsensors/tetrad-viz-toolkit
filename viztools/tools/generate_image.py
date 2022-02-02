from colors import get_gyor_color_gradient
from PIL import Image


def _estimate_map_to_img(obj, filename, format='png', scaling='epa'):
    """
    obj: the estimate map dictionary (keys: lat, lon, alt, pm, var)
    filename: output filename
    format: png, jpg, etc.
    scaling: the color gradient scaling
        "epa": anchors at 12, 35, etc.
        "aqi": anchors at 50, 100, 150, ...
        "linear": smooth scaling from green to purple
    """

    
