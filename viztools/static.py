import numpy as np
from folium import Map as FoliumMap
import viztools.io

class StaticViz(FoliumMap):
    """
    """
    def __init__(self, 
                 overlay_data,
                 *args, 
                 **kwargs):
        
        self.overlay_data = overlay_data

        super().__init__(
            location=[np.mean(self.overlay_data['lat']), np.mean(self.overlay_data['lon'])],
            min_lat=np.min(self.overlay_data['lat']),
            max_lat=np.max(self.overlay_data['lat']),
            min_lon=np.min(self.overlay_data['lon']),
            max_lon=np.min(self.overlay_data['lon']),
            *args, 
            **kwargs
        )




    @classmethod
    def from_gs(cls,
                region,
                timestamp,
                *args,
                credentials_file=None,
                get_closest=False):
        obj = viztools.io.storage.read_region_snapshot(region, timestamp, credentials_file, get_closest)
        return StaticViz(obj)





