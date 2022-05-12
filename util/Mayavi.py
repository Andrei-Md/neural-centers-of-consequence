import matplotlib.pyplot as plt
from matplotlib import cm
from mayavi import mlab
import numpy as np


def plot_coords(df, lut, no_colors, col1='X(R)', col2='Y(A)', col3='Z(S)'):
    s = np.arange(df.shape[0])
    # plot points
    mlab.figure(1, bgcolor=(0, 0, 0))
    mlab.clf()
    pfc_pts = mlab.points3d(df[col1].to_numpy(),
                            df[col2].to_numpy(),
                            df[col3].to_numpy(),
                            s,
                            # communities,
                            colormap="Blues",
                            scale_factor=3,
                            scale_mode='none',
                            resolution=100)

    pfc_pts.module_manager.scalar_lut_manager.lut.number_of_colors = no_colors
    pfc_pts.module_manager.scalar_lut_manager.lut.table = lut
    # plot edges
    # pts.mlab_source.dataset.lines = np.array(list_of_edges)
    # tube = mlab.pipeline.tube(pts, tube_radius=0.1)
    # mlab.pipeline.surface(tube, color=(0.5, 0.5, 0.5))

    mlab.draw()
    mlab.show()


def get_lut(df, incl_list=None):
    '''
    method to obtain the look up table for colors
    :param df: dataframe to contain the specific color unique identifier
    :return: lut and # colors
    '''

    # map indexes
    ba = df.unique()
    ba_idx = {str(x): ba.tolist().index(x) for x in ba}
    no_colors = len(ba)

    # get colors
    viridis = cm.get_cmap('viridis', no_colors)
    # print('viridis.colors', viridis.colors)

    s = np.arange(df.shape[0])
    lut = np.zeros((len(s), 4))

    # lut[:, -1] = 1
    for i, val in enumerate(df.to_numpy()):
        if incl_list is not None :
            if val in incl_list:
                lut[i, 0:4] = viridis.colors[ba_idx[str(val)]] * 255
            else:
                lut[i, 0:4] = viridis.colors[ba_idx[str('nan')]] * 255
        else:
            lut[i, 0:4] = viridis.colors[ba_idx[str(val)]] * 255
        # print(i,val,ba_idx[str(val)],lut[i])

    if incl_list is not None:
        no_colors = len(incl_list)+1

    return lut, no_colors
