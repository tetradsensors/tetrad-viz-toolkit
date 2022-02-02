import io
import os
import numpy as np
import folium
from folium import Map as FoliumMap
from PIL import Image
import tools.snapshot
import vizio.storage


class StaticViz(FoliumMap):
    """
    """
    def __init__(self, 
                 overlay_data:tools.snapshot.Snapshot,
                 tiles='Stamen Terrain',
                 zoom='auto',
                 *args, 
                 **kwargs):
        
        self._data = overlay_data    # Snapshot object

        # TODO: Make better
        if zoom == 'auto':
            zoom = 11

        super().__init__(location=[self._data.lats.mean(), self._data.lons.mean()],
                         min_lat=self._data.lats.min(),
                         max_lat=self._data.lats.max(),
                         min_lon=self._data.lons.min(),
                         max_lon=self._data.lons.max(),
                         tiles=tiles,
                         zoom_start=zoom,
                         *args,
                         **kwargs
        )

        # Add the image to a map
        folium.raster_layers.ImageOverlay(np.asarray(self._data.img),
                                         [
                                             (self._data.lats.min(),self._data.lons.min()),
                                             (self._data.lats.max(),self._data.lons.max())
                                         ],
                                         opacity=0.75,
                                         origin='lower',
                                         pixelated=False,
                                         name=self._data.param).add_to(self)
        folium.LayerControl().add_to(self)


    def save_img(self, filename):
        print(f'Saving image to: {filename}')
        self._data.img.save(filename)


    def save_map(self, filename):
        """filename: HTML or PNG"""
        
        print(f'Saving map to: {filename}')

        if os.path.splitext(filename)[-1] == '.html':
            self.save(filename)
        elif os.path.splitext(filename)[-1] == '.png':
            img_data = self._to_png(0.1)
            img = Image.open(io.BytesIO(img_data))
            img.save(filename)
        else:
            assert False, "Not a supported format"


    @classmethod
    def from_gs(cls,
                region,
                timestamp,
                credentials_file=None,
                get_closest=False):
        """Get the data from Google Storage (no permissions needed)"""
        obj = vizio.storage.read_region_snapshot(region, timestamp, credentials_file, get_closest)
        return StaticViz(obj)

    






