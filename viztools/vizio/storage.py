from datetime import timedelta
from dateutil.parser import parse
from google.cloud import storage
import json
from viztools.tools.snapshot import Snapshot

BUCKET = 'tetrad_estimate_maps'


def _round_time(dt, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   https://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object
   """
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)


def _round_15min(dt):
    return _round_time(dt, roundTo=60*15)


def _round_1min(dt):
    return _round_time(dt, roundTo=60*1)


def read_region_snapshot(region, timestamp, credentials_file=None, get_closest=False):
    if credentials_file:
        import os
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)

    if isinstance(timestamp, str):
        timestamp = parse(timestamp)

    if get_closest:
        timestamp = _round_15min(timestamp)
    else:
        timestamp = _round_1min(timestamp)

    source_blob_name = f'{timestamp.strftime("%Y/%m %B")}/{region}/{region}_{timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")}.json'

    blob = bucket.blob(source_blob_name)
    contents = blob.download_as_string()
    obj = json.loads(contents)
    
    estimates = obj['estimates'][0]['PM2_5']
    variance = obj['estimates'][0]['Variance']

    return Snapshot(lats=obj['Latitudes'],
                    lons=obj['Longitudes'],
                    alts=obj['Elevations'],
                    vals=estimates,
                    vars=variance,
                    generate_img=True,
                    opac95=5,
                    opac05=20)
    