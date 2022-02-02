from static import StaticViz


def test_StaticViz():
    viz = StaticViz.from_gs(
        region='slc_ut',
        timestamp='2022-01-28T15:00:00Z'
    )
    print(vars(viz).keys())


def run_tests():
    test_StaticViz()


def main():
    run_tests()


if __name__ == '__main__':
    main()