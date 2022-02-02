import numpy as np
from PIL import Image
from colors import *
from colors import _hex_to_RGB
from matplotlib import pyplot as plt

def test_color_gradients():
    def show_gradient(cd, format):

        if format == 'HEX':
            cd = [_hex_to_RGB(i) for i in cd]
        ch = np.array(list(zip(*cd))).T.astype(np.uint8)

        img = np.zeros((100,len(cd),3)).astype(np.uint8)
        img[:,:,0] = np.tile(np.array(ch[:, 0]).astype(np.uint8), (100, 1))
        img[:,:,1] = np.tile(np.array(ch[:, 1]).astype(np.uint8), (100, 1))
        img[:,:,2] = np.tile(np.array(ch[:, 2]).astype(np.uint8), (100, 1))

        Image.fromarray(img, "RGB").show()
        print('sent to sytem image viewer')


    gradient = get_gyor_color_gradient('epa')
    show_gradient(gradient, format='RGB')

    gradient = get_gyor_color_gradient('epa', n=700)
    show_gradient(gradient, format='RGB')

    gradient = get_gyor_color_gradient('linear', n=500, format='HEX')
    show_gradient(gradient, format='HEX')


def run_tests():
    test_color_gradients()


if __name__ == '__main__':
    run_tests()


