"""Create a random cell distribution.

This script allows for creation of a random cell mosaic which can be
used for random voronoi comparison. Minimum separation between cells
can be employed.

Example
-------
Use the command line interface to create random cell coordinates
with variables specified in following arguments. Here we are 
creating a random cell distribution with 1000 seeds (cells), in a
mock image of 200 x 300 pixels, and a minimum separation of 10 pixels::

    $ python random_cell_dist.py 1000 200 300 10

Notes
-----
    Further settings with more details can be altered in the settings 
    file. Dimensions and separation are denoted in pixels for the sake
    of visualisation, but the numbers are arbitrary in this conext,
    so they can entered in and thought of as microns. However bare in
    mind that the dimensions must be also integers.


Arguments
----------
{optional} number of seeds : int
    The number of seeds (or cells). How many cells will be distributed.
    
{optional} dimension (1) : int
    The first (or only) dimension - X. If no other argumented are parsed,
    this singular dimension will be used to make a square. The default
    value is 100. (PIXELS)
    
{optional} dimension (2) : int
    The sedcond dimension - Y. The default value is 100. (PIXELS)
    
{optional} minimum separation : float
    The minimum separation between cells. Bare in mind this number cannot
    be too high, or the program will fail, as it will not be able to find
    new locations that are at the minimum separation. The default value is 
    0. (PIXELS)
"""

import sys

from lib.cells.cell_dist import CellDist
from lib.cells import seeds
from lib.utils import parse
from lib.utils.utils import *

def main():
    
    NUM_SEEDS, MPP, DENSITY, MIN_SEP = parse_args()
    DIM = auto_dim(NUM_SEEDS, DENSITY, MPP)
    
    print("Creating random seed voronoi..")
    print(f"Number of seeds: {NUM_SEEDS}. Dimensions: {DIM} (pixels)")
    
    min_sep_pix = round(MIN_SEP / MPP)
    points = seeds.generate(NUM_SEEDS, DIM, min_sep_pix)
    
    
    dist_id = "random_" + str(NUM_SEEDS) + "_" + str(MPP) + "_" + str(DENSITY) + "_" + str(MIN_SEP) 
    dist_id = dist_id.replace(".", "p")
    
    dist = CellDist(points, DIM, MPP, id=dist_id)
    dist.show_voronoi()
    dist.calc_stats()
    dist.print_report_full()
    dist.save()
    
def parse_args():

    if len(sys.argv) == 1:
        
        num_seeds = 100
        mpp = 1
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 2:
        
        num_seeds = parse.num_seeds(sys.argv[1])
        
        mpp = 1
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 3:
        
        num_seeds = parse.num_seeds(sys.argv[1])
        mpp = parse.mpp(sys.argv[2])
            
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 4:
        
        num_seeds = parse.num_seeds(sys.argv[1])
        mpp = parse.mpp(sys.argv[2])
        density = parse.density(sys.argv[3])
        
        min_sep = 0
        
    elif len(sys.argv) == 5:
        
        num_seeds = parse.num_seeds(sys.argv[1])
        mpp = parse.mpp(sys.argv[2])
        density = parse.density(sys.argv[3])
        min_sep = parse.min_sep(sys.argv[4])
        
    else:
        
        raise KeyError("Too many input arguments")
        
    return num_seeds, mpp, density, min_sep
    
main()