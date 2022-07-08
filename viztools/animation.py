import io
import os
import cv2
import time
import datetime
import tempfile
from matplotlib.pyplot import text
import numpy as np
from dateutil.parser import parse
from pathlib import Path
from PIL import Image
from pyparsing import col
from selenium import webdriver
from contextlib import contextmanager
from viztools.static import StaticViz
from viztools.tools.clihelpers import printProgressBar


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


class Animation:
    def __init__(self,
        region,
        start,
        end,
        zoom,
        location=None,
        opac05=20,
        colormap='auto', 
        include_timestamp=False, 
        textloc=None):
        self.region = region 
        if isinstance(start, datetime.datetime):
            self.start = start 
        else:
            self.start = parse(start)
        if isinstance(end, datetime.datetime):
            self.end = end 
        else:
            self.end = parse(end)

        assert self.start < self.end, f"Bad start/end times. You entered: [{self.start} - {self.end}]"

        self.zoom = zoom
        self.location = location 
        self.opac05 = opac05
        self.colormap = colormap
        self.include_timestamp = include_timestamp
        self.textloc = textloc

    def create_animation(self, dirname, video_name='animation', fps=20):
        delay = 1

        assert os.path.exists(dirname), f"{dirname} does not exist. You must create it manually"

        # Selenium web driver for taking screenshots
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

        # OpenCV VideoWriter Init (need size before we can actually make it)
        video_name = f'{dirname}/{video_name}.avi'
        video = None

        intervals = int((self.end - self.start).total_seconds() / (15 * 60)) + 1
        dt_range = [self.start + datetime.timedelta(minutes=15 * i) for i in range(intervals)]

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
                viz = StaticViz.from_gs(region=self.region, timestamp=dt, zoom=self.zoom, location=self.location, opac05=self.opac05, colormap=self.colormap, include_timestamp=self.include_timestamp, textloc=self.textloc)
            except Exception as e:
                print(str(e))
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
            height, width, _ = img.shape
            size = (width,height)

            # Can't instantiate until we have an image size
            if video is None:
                video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
            
            video.write(img)

            t1 = time.time()
            runtime = t1 - t0
            times.append(runtime)
            totalsecs = int(np.median(times) * intervals)

        printProgressBar(iteration=intervals,
                        total=intervals,
                        prefix=' Progress',
                        suffix=f'[{str(dt)}]',
                        printEnd='\n\r',
                        totalsecs=totalsecs)

        print(f'releasing video: {video_name}')
        video.release()

def full_animation_run(region, start, end, dirname, filename, zoom=10, fps=20, location=None, opac05=20, colormap='auto', include_timestamp=False, textloc=None):
    delay = 1
    
    # Selenium web driver fro taking screenshots
    options = webdriver.firefox.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    # OpenCV VideoWriter Init (need size before we can actually make it)
    video_name = f'{dirname}/{filename}.avi'
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
            viz = StaticViz.from_gs(region=region, timestamp=dt, zoom=zoom, location=location, opac05=opac05, colormap=colormap, include_timestamp=include_timestamp, textloc=textloc)
        except Exception as e:
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
        height, width, _ = img.shape
        size = (width,height)

        # Can't instantiate until we have an image size
        if video is None:
            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        
        video.write(img)

        t1 = time.time()
        runtime = t1 - t0
        times.append(runtime)
        totalsecs = int(np.median(times) * intervals)

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

    x = {
        # 'clev_oh': {
        #     'time': (
        #         datetime.datetime(2022, 1, 30, 0, 0, 0),
        #         datetime.datetime(2022, 2, 1, 0, 0, 0)
        #     ),
        #     'zoom': 12,
        #     'location': None,
        #     'opac05': 100,
        #     'textlat': 41.51002165254554, 
        #     'textlon': -81.58609918433848
        # },
        # 'chatt_tn': {
        #     'time': (
        #         datetime.datetime(2021, 12, 5, 0, 0, 0),
        #         datetime.datetime(2021, 12, 6, 0, 0, 0)
        #     ),
        #     'zoom': 13,
        #     'location': (35.034230288186286, -85.30627399787963),
        #     'opac05': 100,
        #     'textlat': 35.06481885056493, 
        #     'textlon': -85.26052198972685
        # },
        'kc_mo': {
            'time': (
                datetime.datetime(2021, 12, 15, 12, 0, 0),
                datetime.datetime(2021, 12, 16, 12, 0, 0)
            ),
            'zoom': 12,
            'location': None,
            'opac05': 100,
            'textlat': 39.100074843734596,  
            'textlon': -94.53751580279695
        }
    }
    basedir = '/Users/tombo/Downloads/animation2'
    for region,v in x.items():

        print(region)

        img_dir = f'{basedir}/{region}'
        os.makedirs(img_dir, exist_ok=True)
        video_filename = f'{region}'

        full_animation_run(region, 
                           v['time'][0], 
                           v['time'][1], 
                           img_dir, 
                           video_filename,
                           zoom=v['zoom'],
                           location=v['location'],
                           opac05=v['opac05'],
                           include_timestamp=True,
                           textloc=(v['textlat'], v['textlon'])
        )