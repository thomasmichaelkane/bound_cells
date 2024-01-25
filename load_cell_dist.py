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
file name : str
    The relative or absolute path to the coordinates file. This
    file should be a two column csv file containing x and y 
    coordinates of all cell centres (in pixels).

microns per pixel : float
    The scaling factor. How many microns per pixel in the original image.
    
dimension (1) : int
    The first (or only) dimension - X. If no other argumented are parsed,
    this singular dimension will be used to make a square. (PIXELS)
    
{optional} dimension (2) : int
    The second dimension - Y. (PIXELS)
"""

import sys
import os

from lib.cells.cell_dist import CellDist
from lib.utils import parse
from lib.utils.utils import *
from lib.utils.settings import display_settings

def main():
    
    FILENAME, MPP, ROTATE, DIM = parse_args()

    coords = csv_to_list(FILENAME)
    dim = DIM
    points = coords_as_np(coords)
    roi_base_name, _ = os.path.splitext(FILENAME)
    
    if ROTATE != 0: points, dim = rotate_coordinates_90_degrees(ROTATE, points, dim)
    
    file_id = get_id(FILENAME)
    
    dist = CellDist(points, dim, MPP, id=file_id)
    
    # dist.show_voronoi()
    # dist.find_densities(bandwidth=display_settings["pdf_bandwidth"], 
    #                     grid_density=display_settings["grid_density"],
    #                     cutoff=display_settings["cutoff"])
    # dist.show_density_plot()
    # dist.show_contour_plot(contour_levels=display_settings["contour_levels"])
    # dist.define_density_roi("ventral")
    # dist.define_density_roi("dorsal")
    # dist.show_density_rois()
    # dist.save_rois(roi_base_name)
    
    dist.show_voronoi(bound=False)
    dist.show_voronoi()
    dist.dilate_border()
    dist.print_report_full()
    dist.show_voronoi()
    
    dist.show_histograms()
    # dist.save()
    dist.show_mask()
    dist.show_dil_mask()
    dist.show_points_with_border()

       
def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        raise KeyError("No scaling specified")
        
    elif len(sys.argv) == 3:
        
        raise KeyError("No dimensions specified")

    elif len(sys.argv) == 4:
        
        raise KeyError("No dimensions specified")
           
    elif len(sys.argv) == 5:
        
        file_name = parse.file_name(sys.argv[1])
        mpp = parse.mpp(sys.argv[2])
        rotate = parse.rotate(sys.argv[3])
        dim_uni = sys.argv[4]
            
        dim = [parse.dim(dim_uni), parse.dim(dim_uni)]
        
    elif len(sys.argv) == 6:
        
        file_name = parse.file_name(sys.argv[1])
        mpp = parse.mpp(sys.argv[2])
        rotate = parse.rotate(sys.argv[3])
        dim = [parse.dim(sys.argv[4]), parse.dim(sys.argv[5])]
               
    else:
        
        raise KeyError("Too many input arguments")
    
    return file_name, mpp, rotate, dim

main()