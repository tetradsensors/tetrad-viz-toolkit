import numpy as np
from PIL import Image
from colors import *
from colors import _hex_to_RGB
from generate_image import _resize_mat, _estimate_map_to_img, _estimate_map_to_img_dist_scaled
from matplotlib import pyplot as plt
import sys
import datetime
from viztools.io.storage import read_region_snapshot

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


def test_resize_img():
    mat = np.random.random(size=(10,10))
    mat2 = _resize_mat(mat, (100, 100))

    assert mat2.shape == (100, 100)


def test_estimate_map_to_img():
    obj = read_region_snapshot('slc_ut', '2022-01-30T22:00:00Z')
    print('Downloaded object')
    _estimate_map_to_img(obj, '/Users/tombo/Downloads/map.png', size=(1000, 1200))

def test_estimate_map_to_img_dist_scaled():
    start = datetime.datetime(2022, 1, 9, 0, 0, 0)
    end = datetime.datetime(2022, 1, 14, 0, 0, 0)
    intervals = (end - start).total_seconds() / (15 * 60)
    dt_range = [start + datetime.timedelta(minutes=15 * i) for i in range(int(intervals))]
    region = 'slc_ut'
    for dt in dt_range:
        print(dt)
        dts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            obj = read_region_snapshot('slc_ut', dts)
            _estimate_map_to_img_dist_scaled(obj, f'/Users/tombo/Downloads/estimate_maps/{region}_{dts}.png', largest_size=1300, opac95=7, opac05=50)
        except Exception as e:
            print('\tno map for this time period', str(e))
            continue


def video():
    import cv2
    import os

    image_folder = '/Users/tombo/Downloads/estimate_maps'
    video_name = '/Users/tombo/Downloads/video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images = sorted(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 4, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
        


def run_tests():
    # test_color_gradients()
    # test_resize_img()
    # test_estimate_map_to_img()
    # test_estimate_map_to_img_dist_scaled()
    video()


if __name__ == '__main__':
    run_tests()


