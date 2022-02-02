from static import StaticViz


def test_StaticViz():
    viz = StaticViz.from_gs(
        region='slc_ut',
        timestamp='2022-01-28T15:00:00Z'
    )
    viz.save_map('/Users/tombo/Downloads/map.png')


def run_tests():
    test_StaticViz()


if __name__ == '__main__':
    run_tests()