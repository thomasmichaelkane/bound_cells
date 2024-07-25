"""Load an arbitrary shaped cell distribution.

This script allows for visualisation and analysis of an arbitrary shape
cell mosaic. A distribution of cells is loaded and a CellDist object is
created for voronoi analysis.

Example
-------
Use the command line interface to load a csv containing cell coordinates
with scaling and dimensions specified in following arguments. Here we
are loading the cell distribution from the csv file dist.csv. In this
image there are 1.4 microns per pixel, and the dimensions of the image
are 6000 x 7000 pixels::

    $ python load_cell_dist.py examples/dist.csv 1.4 6000 7000

Notes
-----
    There are three required arguments denoted below (file, microns per
    pixel, and dimension (1)), but further settings with more details can
    be altered in the settings file.

Arguments
----------
path : str
    The relative or absolute path to the coordinates file. This
    file should be a two column csv file containing x and y 
    coordinates of all cell centres (in pixels).
    
dimension (1) : int
    The first (or only) dimension - X. If no other argumented are parsed,
    this singular dimension will be used to make a square. (PIXELS)
    
{optional} dimension (2) : int
    The second dimension - Y. (PIXELS)
    

{optional} microns per pixel : float
    The scaling factor. How many microns per pixel in the original image. The default is 1.
    
{optional} rotation : int
    How many times to rotate the coordinates 90 degrees if desired. The default is no rotation.
"""

import sys
import os

from bound_cells import CellDist, load_config
from bound_cells.utils import parse
from bound_cells.utils.util_functions import *

def run():
    
    PATH, DIM, MPP, ROTATE = parse_args()
    
    config = load_config()

    coords = csv_to_list(PATH)
    dim = DIM
    points = coords_as_np(coords)

    roi_base_name, _ = os.path.splitext(PATH)
    file_id = get_id(PATH)

    # rotate distribution if necessary
    if ROTATE != None: points, dim = rotate_coordinates_90_degrees(ROTATE, points, dim)

    # create cell distriubution object
    dist = CellDist(points, dim, config, mpp=MPP, id=file_id)

    # calulcate densities with config
    dist.find_densities(bandwidth=config['display_settings']["pdf_bandwidth"], 
                        grid_density=config['display_settings']["grid_density"],
                        cutoff=config['display_settings']["cutoff"])
    
    # show density and contour plots
    dist.show_density_plot()
    dist.show_contour_plot(contour_levels=config['display_settings']["contour_levels"])
    
    # examine density ROIS
    dist.define_density_roi("region_one")
    dist.define_density_roi("region_two")
    dist.show_density_rois()
    dist.save_rois(roi_base_name)
    
    # show undilated voronoi
    dist.show_voronoi(bound=False)
    dist.show_voronoi()
    
    # dilate
    dist.dilate_border()
    
    # console log key stats
    dist.print_report_full()
    
    # show dilated voronoi and stats
    dist.show_voronoi()
    dist.show_histograms()
    
    # save results
    dist.save()
    
    # alpha border processing steps
    dist.show_mask()
    dist.show_dil_mask()
    dist.show_points_with_border()

       
def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        raise KeyError("No dimensions specified")
        
    elif len(sys.argv) == 3:
        
        path = parse.path(sys.argv[1])
        dim_uni = sys.argv[2]
            
        dim = [parse.dim(dim_uni), parse.dim(dim_uni)]
        
        mpp = 1
        rotate = None

    elif len(sys.argv) == 4:
        
        path = parse.path(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        
        mpp = 1
        rotate = None
           
    elif len(sys.argv) == 5:
        
        path = parse.path(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        mpp = parse.mpp(sys.argv[4])
        
        rotate = None
        
    elif len(sys.argv) == 6:
        
        path = parse.path(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        mpp = parse.mpp(sys.argv[4])
        rotate = parse.rotate(sys.argv[5])
               
    else:
        
        raise KeyError("Too many input arguments")
    
    return path, dim, mpp, rotate

run()