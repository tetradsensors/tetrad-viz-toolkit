import numpy as np
import tools.generate_image

class Snapshot:
    """
    Formalized view of the data saved in our database. This just cleans it up
    and makes sure everything is correct before it can be used elsewhere. 
    """
    def __init__(self,
                 lats,
                 lons,
                 alts,
                 vals,
                 vars,
                 generate_img=False,
                 opac95=3,
                 opac05=12,
                 param="PM2.5"):  # Placeholder, will change once estimate maps are for more metrics

        self.lats = np.array(lats).reshape(-1,)
        self.lons = np.array(lons).reshape(-1,)
        self.alts = np.array(alts)
        self.vals = np.array(vals)
        self.vars = np.array(vars)
        self.param = param

        assert self.lats.shape[0] == self.vals.shape[1]
        assert self.lons.shape[0] == self.vals.shape[0]
        assert self.alts.shape == self.vals.shape == self.vars.shape

        if generate_img:
            # PIL.Image
            self.img = tools.generate_image._snapshot_to_img_dist_scaled(self,
                                                                       largest_size=1300,  
                                                                       scaling='epa', 
                                                                       opac95=opac95, 
                                                                       opac05=opac05)
        else:
            self.img = None



