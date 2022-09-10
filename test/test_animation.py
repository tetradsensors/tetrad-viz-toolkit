# from viztools.animation import Animation
# from viztools import animation
from viztools import Animation
from viztools.static import StaticViz
import os
import shutil


def test_animation(region, start, end, zoom, textloc, tiles):
    dr = f'/Users/tombo/Movies/pollution-animations/{region}_{start.split("T")[0]}-{end.split("T")[0]}'
    if os.path.exists(dr):
        shutil.rmtree(dr)
    os.makedirs(dr)
    video = Animation(
        region='slc_ut',
        start=start,
        end=end,
        # start='2022-08-02T00:00:00Z',
        # end='2022-08-07T18:00:00Z',
        zoom=zoom,
        include_timestamp=True,
        textloc=textloc,
        # mapbox styles: "light-v9, dark-v9, outdoors-v9, satellite-streets-v9, streets-v9"
        tiles=tiles
    )
    video.create_animation(dirname=dr,
                           fps=20,
                           save_overlays=True,
                           )


def test_static(region, timestamp, zoom, location, textloc, tiles):
    filename = f'/Users/tombo/Pictures/pollution-images/{region}_{timestamp.split("T")[0]}.png'
    viz = StaticViz.from_gs(
        region=region,
        timestamp=timestamp,
        zoom=zoom,
        location=location,
        include_timestamp=True,
        textloc=textloc,
        tiles=tiles
    )
    viz._data.img.save(filename)
    print(f'Image saved to {filename}')


if __name__ == '__main__':
    region = 'slc_ut'

    # start='2022-07-09T00:00:00Z'
    # end='2022-07-13T00:00:00Z'

    start = '2022-08-02T00:00:00Z'
    end = '2022-08-07T18:00:00Z'

    # timestamp = '2022-07-10T00:30:00Z' # hottest snapshot
    timestamp = '2022-07-10T00:30:00Z'

    zoom = 11

    textloc = [40.74678372275716, -111.64981231030511]

    # mapbox styles: "light-v9, dark-v9, outdoors-v9, satellite-streets-v9, streets-v9"
    tiles = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidGJlY25lbDE0IiwiYSI6ImNsNG0wanFoYjAzNHEzbm8ybzB3YjB5enoifQ.ETqmBqAvnMnterXcYMK6Zw'

    # test_animation(
    #     region=region,
    #     start=start,
    #     end=end,
    #     zoom=zoom,
    #     textloc=textloc,
    #     tiles=tiles
    # )

    test_static(
        region=region,
        timestamp=timestamp,
        zoom=zoom,
        location=None,
        textloc=textloc,
        tiles=tiles
    )
