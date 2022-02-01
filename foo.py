import folium
import sys

def inline_map(m):
    from folium import Map
    from IPython.display import HTML, IFrame
    if isinstance(m, Map):
        m._build_map()
        srcdoc = m.HTML.replace('"', '&quot;')
        embed = HTML('<iframe srcdoc="{srcdoc}" '
                     'style="width: 100%; height: 500px; '
                     'border: none"></iframe>'.format(srcdoc=srcdoc))
    elif isinstance(m, str):
        embed = IFrame(m, width=750, height=500)
    return embed

min_lon = -112.1594
max_lon = -111.7616
min_lat = 40.35
max_lat = 41.0

width, height = 1200, 1000
mapa = folium.Map(location=[40.5, -112.0],
                  min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                  tiles='Stamen Toner', width=width, height=height, zoom_start=10)

folium.raster_layers.ImageOverlay("./tmp.png",
                    [[min_lat,min_lon],[max_lat,max_lon]],
                    opacity=0.75,
                    origin='lower',
                    pixelated=False,
                    name="PM2.5",
                   ).add_to(mapa)

folium.LayerControl().add_to(mapa)

import branca

colormap = branca.colormap.linear.viridis.scale(0, 40)
#colormap = colormap.to_step(index=[0, 10, 20, 30, 40])
# colomap.tick_labels=[0.0, 10.0, 20.0, 30.0, 40.0]
colormap.caption = 'PM 2.5 in micrograms/cu-meter'

colormap.add_to(mapa)

mapa.save("tmp.html")
inline_map(mapa)
