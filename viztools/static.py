import io
import os
import numpy as np
import folium
import branca
from folium import Map as FoliumMap
from PIL import Image
from viztools.tools import snapshot, colors
from viztools.vizio import storage


class StaticViz(FoliumMap):
    """
    Tile options:
        “OpenStreetMap”
        “Mapbox Bright” (Limited levels of zoom for free tiles)
        “Mapbox Control Room” (Limited levels of zoom for free tiles)
        “Stamen” (Terrain, Toner, and Watercolor)
        “Cloudmade” (Must pass API key)
        “Mapbox” (Must pass API key)
        “CartoDB” (positron and dark_matter)
    """

    def __init__(self,
                 overlay_data: snapshot.Snapshot,
                 tiles='Stamen Toner',
                 zoom='auto',
                 colormap='auto',
                 location=None,
                 timestamp=False,
                 textloc=None,
                 textsize=12,
                 include_colorbar=True,
                 image_overlay=None,  # {filename:, north:,...,name:}
                 *args,
                 **kwargs):

        if timestamp:
            assert textloc, "if timestamp then must textloc"

        self._data = overlay_data    # Snapshot object
        self.textloc = textloc
        self.textsize = textsize

        # TODO: Make better
        if zoom == 'auto':
            zoom = 11

        if location is None:
            self.clat, self.clon = self._data.lats.mean(), self._data.lons.mean()
            location = [self._data.lats.mean(), self._data.lons.mean()]
        else:
            self.clat, self.clon = location[0], location[1]

        if tiles.startswith('http'):
            attr = 'XXX Mapbox Attribution'
        else:
            attr = ''
        super().__init__(location=location,
                         min_lat=self._data.lats.min(),
                         max_lat=self._data.lats.max(),
                         min_lon=self._data.lons.min(),
                         max_lon=self._data.lons.max(),
                         tiles=tiles,
                         attr=attr,
                         zoom_start=zoom,
                         colormap='auto',
                         *args,
                         **kwargs
                         )

        # Add the image to a map
        folium.raster_layers.ImageOverlay(np.asarray(self._data.img),
                                          [
            (self._data.lats.min(), self._data.lons.min()),
            (self._data.lats.max(), self._data.lons.max())
        ],
            opacity=0.75,
            origin='lower',
            pixelated=False,
            name=self._data.param).add_to(self)

        if image_overlay:
            print('adding image overlay')
            img = np.array(Image.open(image_overlay['filename']))

            folium.raster_layers.ImageOverlay(
                img,
                [
                    (image_overlay['north'], image_overlay['east']),
                    (image_overlay['south'], image_overlay['west'])
                ],
                opacity=1,
                origin='upper',
                pixelated=False,
                name=image_overlay['name']
            ).add_to(self)
            print(
                f'Added image with bounds: {image_overlay["north"]}, {image_overlay["south"]}, {image_overlay["east"]}, {image_overlay["west"]}')

        folium.LayerControl().add_to(self)

        if timestamp and self._data.timestamp:
            text = self._data.timestamp.strftime("%B %d, %Y")
            icon_width = len(list(text)) * self.textsize
            icon_height = self.textsize
            folium.map.Marker(
                [self.textloc[0], self.textloc[1]],
                icon=folium.features.DivIcon(
                    icon_size=(icon_width, icon_height),
                    icon_anchor=(int(icon_width/2), int(icon_height/2)),
                    html=f'<div style="border-radius:10px;font-size:{self.textsize}pt;background:rgba(255,255,255,0.6);text-align:center;justify-content:center;padding: 5px 5px">{text}</div>',
                )
            ).add_to(self)

        if include_colorbar:
            i, c = zip(*colors.PM_EPA_COLOR_SCALE_RGB.items())
            if colormap == 'auto':
                cmap = branca.colormap.LinearColormap(colors=c,
                                                      index=i,
                                                      vmin=0,
                                                      vmax=40)
            else:
                cmap = eval(f"branca.colormap.linear.{colormap}.scale(0, 40)")

            cmap.caption = 'PM2.5 in micrograms/cu-meter'
            cmap.add_to(self)

    def save_img(self, filename):
        self._data.img.save(filename)

    def save_map(self, filename, bbox=None):
        """filename: HTML or PNG
        bbox: 'auto' data bounds. None: no bbox
        """

        if bbox == 'auto':
            bbox = folium.Rectangle(bounds=[
                (self._data.lats.min(), self._data.lons.min()),
                (self._data.lats.max(), self._data.lons.min()),
                (self._data.lats.max(), self._data.lons.max()),
                (self._data.lats.min(), self._data.lons.max())
            ])
            bbox.add_to(self)

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
                get_closest=False,
                colormap='auto',
                zoom='auto',
                location=None,
                include_timestamp=False,
                include_colorbar=True,
                image_overlay=None,
                textloc=None,
                textsize=12,
                opac95=5,
                opac05=20,
                tiles='Stamen Toner'):
        """Get the data from Google Storage (no permissions needed)"""

        # returns a Snapshot
        obj = storage.read_region_snapshot(region,
                                           timestamp,
                                           credentials_file,
                                           get_closest,
                                           colormap=colormap,
                                           opac95=opac95,
                                           opac05=opac05)
        return StaticViz(obj,
                         zoom=zoom,
                         colormap=colormap,
                         location=location,
                         timestamp=include_timestamp,
                         textloc=textloc,
                         textsize=textsize,
                         tiles=tiles,
                         include_colorbar=include_colorbar,
                         image_overlay=image_overlay,
                         )
