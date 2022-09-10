from viztools import Animation, Screenshot
import os
import shutil


def test_animation(region, start, end, zoom, textloc, tiles, colorbar, fps, textsize, opac05):
    dr = f'/Users/tombo/Movies/pollution-animations/{region}_{start.split("T")[0]}-{end.split("T")[0]}'
    if os.path.exists(dr):
        shutil.rmtree(dr)
    os.makedirs(dr)
    video = Animation(
        region='slc_ut',
        start=start,
        end=end,
        zoom=zoom,
        include_timestamp=True,
        textloc=textloc,
        textsize=textsize,
        tiles=tiles,
        opac05=opac05,
        include_colorbar=False,
        image_overlay=colorbar
    )
    video.create_animation(dirname=dr,
                           fps=fps,
                           save_overlays=True,
                           )


def test_static(region, timestamp, zoom, location, textloc, tiles, colorbar, textsize, opac05):
    filename = f'/Users/tombo/Pictures/pollution-images/{region}_{timestamp.split("T")[0]}.png'

    Screenshot(
        filename=filename,
        region=region,
        timestamp=timestamp,
        zoom=zoom,
        location=location,
        include_timestamp=True,
        textloc=textloc,
        include_colorbar=False,
        image_overlay=colorbar,
        opac05=opac05,
        tiles=tiles,
        textsize=textsize
    )


if __name__ == '__main__':

    # --------------------------------------------------------------------------
    # Salt Lake City, UT Parameters
    # --------------------------------------------------------------------------
    # region = 'slc_ut'

    # w = -112.0465865384756
    # e = -111.85698805364868
    # s = 40.48007044216738
    # n = 40.52026192104301

    # # width, height = Image.open(filename).size
    # # ratio = height / width
    # # meters = geopy.distance.distance((s, w), (s, e)).kilometers * 1000
    # # meters2 = meters * ratio
    # # lat_degrees = meters2 / 200000
    # # n = s + lat_degrees

    # colorbar = {
    #     'filename': '/Users/tombo/Tetrad/tetrad-viz-toolkit/EPA-colorbar-horizontal.png',
    #     'north': n,
    #     'south': s,
    #     'east': e,
    #     'west': w,
    #     'name': 'colorbar'
    # }

    # # start = '2022-07-09T00:00:00Z'
    # # end = '2022-07-13T00:00:00Z'

    # # start = '2022-08-02T00:00:00Z'
    # # end = '2022-08-07T18:00:00Z'

    # start = '2022-09-09T00:00:00Z'
    # end = '2022-09-12T00:00:00Z'

    # fps = 20

    # # timestamp = '2022-07-10T00:30:00Z' # hottest snapshot
    # timestamp = '2022-07-10T00:30:00Z'

    # zoom = 11

    # # textloc = [40.74678372275716, -111.64981231030511] # upper right
    # textloc = [40.788307310953066, -112.06522825027406]  # upper left
    # textsize = 24

    # --------------------------------------------------------------------------
    # END Salt Lake City, UT Parameters
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Lake Tahoe, CA/NV Parameters
    # --------------------------------------------------------------------------
    region = 'tahoe_ca'

    width = 0.18959848482691655
    height = 0.04019147887562724
    n, w = 38.89802594471676, -119.98648769112309
    s = n - height
    e = w + width

    colorbar = {
        'filename': '/Users/tombo/Tetrad/tetrad-viz-toolkit/EPA-colorbar-horizontal.png',
        'north': n,
        'south': s,
        'east': e,
        'west': w,
        'name': 'colorbar'
    }

    start = '2022-09-08T00:00:00Z'
    end = '2022-09-12T00:00:00Z'
    fps = 20
    opac05 = 100

    # timestamp = '2022-07-10T00:30:00Z' # hottest snapshot
    timestamp = '2022-09-09T08:15:00Z'

    zoom = 10
    textsize = 10

    textloc = [(n+s)/2, -120.15088422565398]  # bottom left
    # --------------------------------------------------------------------------
    # END Lake Tahoe
    # --------------------------------------------------------------------------

    # mapbox styles: "light-v9, dark-v9, outdoors-v9, satellite-streets-v9, streets-v9"
    tiles = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidGJlY25lbDE0IiwiYSI6ImNsNG0wanFoYjAzNHEzbm8ybzB3YjB5enoifQ.ETqmBqAvnMnterXcYMK6Zw'

    test_static(
        region=region,
        timestamp=timestamp,
        zoom=zoom,
        location=None,
        textsize=textsize,
        textloc=textloc,
        tiles=tiles,
        colorbar=colorbar,
        opac05=opac05
    )

    # test_animation(
    #     region=region,
    #     start=start,
    #     end=end,
    #     zoom=zoom,
    #     textloc=textloc,
    #     tiles=tiles,
    #     colorbar=colorbar,
    #     fps=fps,
    #     textsize=24,
    #     opac05=opac05
    # )
