# Taken from: https://gist.github.com/RoboDonut/83ec5909621a6037f275799032e97563

PM_EPA_COLOR_SCALE_RGB = {
    0:   (105, 159, 64),    # Green
    15:  (255, 190, 63),    # Yellow
    30:  (250, 121, 29),    # Orange
    45:  (201, 52, 45),     # Red-Orange
    60: (176, 10, 87),     # Red-Purple
    75: (128, 8, 78)       # Purple
}

AQI_COLOR_SCALE_RGB = {
    0:   (105, 159, 64),    # Green
    51:  (255, 190, 63),    # Yellow
    101: (250, 121, 29),    # Orange
    151: (201, 52, 45),     # Red-Orange
    201: (176, 10, 87),     # Red-Purple
    301: (128, 8, 78)       # Purple
}

def _hex_to_RGB(hex_val):
    return [int(hex_val[i:i+2], 16) for i in range(1, 6, 2)]
    

def _RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in RGB])


def _color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
      colors in RGB and hex form for use in a graphing function
      defined later on '''
    
    return {"hex":[_RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]}


def _linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
      two hex colors. start_hex and finish_hex
      should be the full six-digit color string,
      inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = _hex_to_RGB(start_hex)
    f = _hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return _color_dict(RGB_list)


def _polylinear_gradient(colors, n, anchor_locs=None):
    ''' returns a list of colors forming linear gradients between
        all sequential pairs of colors. "n" specifies the total
        number of desired output colors '''
    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = _linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            
            if anchor_locs:
                n_out = int(n * ((anchor_locs[col+1] - anchor_locs[col])/anchor_locs[-1]))
            
            next_col = _linear_gradient(colors[col], colors[col+1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next_col[k][1:]

    return gradient_dict


def _format_color_dict(cd, format):
    """
    format:
        'RGB': list of (R,G,B) tuples
        'HEX': list of #HEX strings
    """

    if format == 'RGB':
        # convert into a list of (R,G,B) tuples
        return list(zip(*(cd[k] for k in 'rgb')))
    else:
        return cd['hex']


def get_custom_color_gradient(anchors, n=None, format='RGB'):
    """
    anchors: a dict where keys are anchor locations and values are RGB (tuple) or HEX (string)
    n: the number of points. if not specified will choose last anchor loc
    format: output format (R,G,B) or #HEX
    """

    # Convert to HEX and split into lists of keys and values
    locs, colors = zip(*[(k, v if isinstance(v,str) else _RGB_to_hex(v)) for k,v in anchors.items()])

    n = n or locs[-1]

    g = _polylinear_gradient(colors, n, anchor_locs=locs)

    return _format_color_dict(g, format)


def get_gyor_color_gradient(source, n=None, format='RGB'):
    """
    source:
        'epa': color locations based of EPA (yellow = 12, orange = 35)
        'aqi': colors matching AQI index
        'linear': just get the colors evenly spaced out
    n: the number of points. If not included it's a 1-1 mapping. Otherwise it gets stretched out to n elements
    format:
        'RGB': list of (R,G,B) tuples
        'HEX': list of #HEX strings
    """
    assert source in ['epa', 'aqi', 'linear']

    # Set the anchor points
    if source == 'epa':
        anchors = PM_EPA_COLOR_SCALE_RGB
    elif source == 'aqi':
        anchors = AQI_COLOR_SCALE_RGB
    else:
        anchors = dict(zip(range(len(PM_EPA_COLOR_SCALE_RGB)), PM_EPA_COLOR_SCALE_RGB.values()))

    return get_custom_color_gradient(anchors, n, format)