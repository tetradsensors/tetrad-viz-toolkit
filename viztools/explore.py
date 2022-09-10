from viztools.vizio.storage import read_region_snapshot
from google.cloud import storage
import pandas as pd
from dateutil.parser import parse
import datetime

global_stats = []
def get_stats(region, ts):
    global global_stats 
    # stats = []

    for t in ts:
        print(t)
        try:
            snapshot = read_region_snapshot(
                region, 
                ts, 
                credentials_file=None, 
                get_closest=True, 
                generate_img=False
            )
        except Exception as e:
            print(str(e))
            continue
            
        d = {
            'timestamp': t, 
            'min': snapshot.vals.min(),
            'max': snapshot.vals.max(),
            'mean': snapshot.vals.mean(),
            'std': snapshot.vals.std()
        }
        global_stats.append(d)

    # return stats

def map_stats_in_range(region, start, end, num_threads=1):
    global global_stats
    stats = []
    start = parse(start)
    end = parse(end)
    timestamp = start

    if num_threads == 1:
        while timestamp < end:

            ts = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        
            print(f'{ts}/{end}')
            try:
                snapshot = read_region_snapshot(
                    region, 
                    ts, 
                    credentials_file=None, 
                    get_closest=True, 
                    generate_img=False
                )
            except Exception as e:
                print(str(e))
                timestamp = timestamp + datetime.timedelta(minutes=15)
                continue
                
            d = {
                'timestamp': ts, 
                'min': snapshot.vals.min(),
                'max': snapshot.vals.max(),
                'mean': snapshot.vals.mean(),
                'std': snapshot.vals.std()
            }
            stats.append(d)

            timestamp = timestamp + datetime.timedelta(minutes=15)

    else:
        import threading, numpy as np
        timestamps = []
        while timestamp < end:
            timestamps.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            timestamp = timestamp + datetime.timedelta(minutes=15)
        
        chunks = list(np.array_split(np.array(timestamps), num_threads))
        threads = [threading.Thread(target=get_stats, args=(region, ts)) for ts in chunks]
        print(f'Created {len(threads)} threads')
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return pd.DataFrame(global_stats)

    return pd.DataFrame(stats)


if __name__ == '__main__':
    region = 'slc_ut'
    start = '2022-07-08'
    end = '2022-08-01'
    df = map_stats_in_range(region, start, end, num_threads=1)
    df.to_csv(f'/Users/tombo/Downloads/stats_slc_{start}_{end}.csv')
    print(df)
    print(df.describe())
