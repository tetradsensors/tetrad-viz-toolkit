import io
import os
import cv2
import time
import datetime
import tempfile
import numpy as np
from pathlib import Path
from PIL import Image
from selenium import webdriver
from contextlib import contextmanager
from static import StaticViz
from tools.clihelpers import printProgressBar


# taken from Folium utilities.py
@contextmanager
def temp_html_filepath(data):
    """Yields the path of a temporary HTML file containing data."""
    filepath = ''
    try:
        fid, filepath = tempfile.mkstemp(suffix='.html', prefix='folium_')
        os.write(fid, data.encode('utf8') if isinstance(data, str) else data)
        os.close(fid)
        yield filepath
    finally:
        if os.path.isfile(filepath):
            os.remove(filepath)
            

def full_animation_run(region, start, end, dirname):
    delay = 1
    fps = 4
    
    # Selenium web driver fro taking screenshots
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    # OpenCV VideoWriter Init (need size before we can actually make it)
    video_name = f'{dirname}/video.avi'
    video = None

    intervals = int((end - start).total_seconds() / (15 * 60)) + 1
    dt_range = [start + datetime.timedelta(minutes=15 * i) for i in range(intervals)]

    times = []
    totalsecs = 5 * intervals
    for i, dt in enumerate(dt_range):

        printProgressBar(iteration=i,
                         total=intervals,
                         prefix=' Progress',
                         suffix=f'[{str(dt)}]',
                         totalsecs=totalsecs)

        t0 = time.time()

        dts = dt.strftime("%Y-%m-%d %H.%M.%SZ")

        try:
            viz = StaticViz.from_gs(region=region, timestamp=dt)
        except:
            continue

        html = viz.get_root().render()
        with temp_html_filepath(html) as fname:
            # We need the tempfile to avoid JS security issues.
            driver.get('file:///{path}'.format(path=fname))
            driver.maximize_window()
            time.sleep(delay)
            png = driver.get_screenshot_as_png()
        
        img = Image.open(io.BytesIO(png))

        fn = f'{dirname}/{dts}.png'
        img.save(fn)

        img = cv2.imread(fn)
        height, width, layers = img.shape
        size = (width,height)

        if i == 0:
            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        
        video.write(img)

        t1 = time.time()
        runtime = t1 - t0
        times.append(runtime)
        totalsecs = int(np.mean(times) * intervals)

    printProgressBar(iteration=intervals,
                     total=intervals,
                     prefix=' Progress',
                     suffix=f'[{str(dt)}]',
                     printEnd='\n\r',
                     totalsecs=totalsecs)

    print(f'releasing video: {video_name}')
    video.release()


def animation_from_images(dir, filename, fps=20):
    """
    dir: directory containing images
    filename: video output name
    """
    
    # Selenium web driver fro taking screenshots
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    # OpenCV VideoWriter Init (need size before we can actually make it)
    video_name = f'{os.path.splitext(filename)[0]}.avi'
    video = None

    images = sorted([str(p) for p in Path(dir).rglob('*.png')])
    for i in images:
        print(i)
    input('Is this order corret? [ENTER or ^c]')

    intervals = len(images)

    times = []
    totalsecs = 5 * intervals
    for i, img in enumerate(images):

        printProgressBar(iteration=i,
                         total=intervals,
                         prefix=' Progress',
                         totalsecs=totalsecs)

        t0 = time.time()

        img = cv2.imread(img)
        height, width, _ = img.shape
        size = (width, height)

        if i == 0:
            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        
        video.write(img)

        t1 = time.time()
        runtime = t1 - t0
        times.append(runtime)
        totalsecs = int(np.mean(times) * intervals)

    printProgressBar(iteration=intervals,
                     total=intervals,
                     prefix=' Progress',
                     printEnd='\n\r',
                     totalsecs=totalsecs)

    print(f'releasing video: {video_name}')
    video.release()


if __name__ == '__main__':
    # region = 'slc_ut'
    # start = datetime.datetime(2022, 1, 9, 0, 0, 0)
    # end = datetime.datetime(2022, 1, 14, 0, 0, 0)
    # dirname = '/Users/tombo/Downloads/animation'

    # full_animation_run(region, start, end, dirname)

    dirname = '/Users/tombo/Downloads/animation'
    filename = f'{dirname}/video2'
    animation_from_images(dirname, filename, fps=20)