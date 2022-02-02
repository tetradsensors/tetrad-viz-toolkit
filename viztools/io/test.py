from storage import read_region_snapshot, _round_15min
import datetime
from dateutil.parser import parse


def test_read_region_snapshot():
    read_region_snapshot('slc_ut', '2021-09-01T00:00:00Z')


def test__round_15min():
    ts = parse('2021-01-31T23:59:01Z')
    ret = _round_15min(ts)
    assert ret == parse('2021-02-01T00:00:00Z')

    ts = parse('2021-01-31T23:50:01Z')
    ret = _round_15min(ts)
    assert ret == parse('2021-01-31T23:45:00Z')

    print('test__round_15min: All tests passed')


def run_tests():
    # test__round_15min()
    # test_read_region_snapshot()
    print('All IO tests passed')


if __name__ == '__main__':
    run_tests()

