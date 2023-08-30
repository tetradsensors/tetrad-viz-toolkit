from viztools import StaticViz


def test_StaticViz():
    viz = StaticViz.from_gs(
        region='kc_mo',
        timestamp='2022-01-28T15:00:00Z',
        zoom=12,
        # colormap='epa',
        location=None,
        opac05=40,
        include_timestamp=True,
        textloc=(39.138269681233844, -94.44364768770033)
    )
    viz.save_map('/Users/tombo/Downloads/map.html', bbox=None)


def run_tests():
    test_StaticViz()


if __name__ == '__main__':
    run_tests()


# Salt Lake Text Loc: (40.84623281579638, -111.59796744368814)
# Cleveland: (41.54826689668482, -81.49204046011891)
# Chatt: (35.08624718853225, -85.21361137938766)
# KC: (39.138269681233844, -94.44364768770033)
