import io
import os
import time
import datetime
import tempfile
from dateutil.parser import parse
from PIL import Image
from selenium import webdriver
from contextlib import contextmanager
from viztools.static import StaticViz


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


class Screenshot:
    def __init__(self,
                 filename,
                 region,
                 timestamp,
                 zoom,
                 save_overlay=False,
                 location=None,
                 opac05=20,
                 opac95=4,
                 colormap='auto',
                 include_timestamp=False,
                 textloc=None,
                 textsize=12,
                 include_colorbar=True,
                 image_overlay=None,
                 tiles='Stamen Toner'):

        self.region = region

        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp
        else:
            self.timestamp = parse(timestamp)

        if include_timestamp:
            assert textloc, "If include_timestamp then textloc must be given as (x,y) coordinates"

        self.zoom = zoom
        self.location = location
        self.opac05 = opac05
        self.colormap = colormap
        self.include_timestamp = include_timestamp
        self.textloc = textloc
        self.tiles = tiles

        delay = 1

        # Selenium web driver for taking screenshots
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

        viz = StaticViz.from_gs(
            region=self.region,
            timestamp=self.timestamp,
            zoom=self.zoom,
            location=self.location,
            opac05=self.opac05,
            colormap=self.colormap,
            include_timestamp=self.include_timestamp,
            include_colorbar=include_colorbar,
            image_overlay=image_overlay,
            textloc=self.textloc,
            textsize=textsize,
            tiles=self.tiles
        )

        if save_overlay:
            nm = filename.split('/')
            nm[-1] = f'overlay_{nm[-1]}'
            overlay_fn = '/'.join(nm)
            viz._data.img.save(overlay_fn)

        html = viz.get_root().render()
        with temp_html_filepath(html) as fname:
            # We need the tempfile to avoid JS security issues.
            driver.get(f'file:///{fname}')
            driver.maximize_window()
            time.sleep(delay)
            png = driver.get_screenshot_as_png()

        img = Image.open(io.BytesIO(png))

        img.save(filename)
        print(f'screenshot saved to {filename}')


if __name__ == '__main__':
    pass
