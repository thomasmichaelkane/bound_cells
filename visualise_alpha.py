"""See the border creation for different alpha values.

This script allows visualisation of the outcome of the border creation
function using different alpha values. Alpha values determine how to
define where the border should be, and different values will gain
vastly different results. This script will simulate cell distriubution
analysis and will allow different alpha values to be viewed and selected.
The first middle value shown is the calculated inter-cell-distance average,
referred to as the ICD.

Example
-------
Use the command line interface to load a cell distribution from a file,
and visualise border creation. This will load the cells from dist.csv 
with dimensions of 500 x 700 (pixels), and display borders created with
5 alpha values from 5% below to 5% above the ICD::

    $ python visualise_alpha.py dist.csv 500 700 5 0.05
    
Once graphs have been presnted using matplotlib, the values can be
rejected or accepted from the command line interface. Once the plot has
been closed, the user will be prompted with the following text:

    "Please confirm alpha value by typing 0, 1, or 2, or type D or U to 
    see new alpha values [U, D, 0, 1, 2]: "
    
Enter the desired value as instructed to see new values, or accept and
continue with the simulation.

Notes
-----
    Further settings with more details can be altered in the settings 
    file. Dimensions and separation are denoted in pixels for the sake
    of visualisation, but the numbers are arbitrary in this conext,
    so they can entered in and thought of as microns. However bare in
    mind that the dimensions must be also integers.

Arguments
----------
file name : str
    The relative or absolute path to the coordinates file. This
    file should be a two column csv file containing x and y 
    coordinates of all cell centres (in pixels).
    
dimension (1) : int
    The first (or only) dimension - X. If no other argumented are parsed,
    this singular dimension will be used to make a square. (PIXELS)
    
{optional} dimension (2) : int
    The sedcond dimension - Y. (PIXELS)
    
{optional} alpha count : int
    How many values of alpha will be trailed each time, and how many graphs
    will be displayed. The default is 3.
    
{optional} alpha allowance : float
    The limits of the linspace of trialled alphas. The lowest and highest
    alpha values that will be shown each time compared with the middle value.
    The default is 0.1, which will show 10% above and below the central value.
"""

import sys

from lib import CellDist, geometry, parse
from lib.utils.utils import *

def main():
    
    FILE_NAME, DIM, ALPHA_COUNT, ALPHA_ALLOWANCE = parse_args()
    
    coords = csv_to_list(FILE_NAME)
    points = coords_as_np(coords)
    
    dist = CellDist(points, DIM, id=FILE_NAME)

    dist.calc_stats()
    icd = dist.get_icd()
    points = dist.get_points_array()
    
    alpha = None
    trial_alpha = icd
        
    while alpha is None:

        alphas = geometry.test_alpha(points, trial_alpha, ALPHA_COUNT, ALPHA_ALLOWANCE)
        alpha, trial_alpha = parse.alpha_input(alphas)
    
    dist.update_alpha(alpha)
    dist.find_border()
    dist.dilate_border()
    dist.show_mask()
    dist.show_dil_mask()
    dist.show_points_with_border()

def parse_args():
    
    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        raise KeyError("No dimensions specified")
        
    elif len(sys.argv) == 3:
        
        file_name = parse.file_name(sys.argv[1])
        dim_uni = sys.argv[2]
        dim = [parse.dim(dim_uni), parse.dim(dim_uni)]
        
        alpha_count = 3
        alpha_allowance = 0.1
    
    elif len(sys.argv) == 4:
        
        file_name = parse.file_name(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        alpha_count = 3
        alpha_allowance = 0.1
        
    elif len(sys.argv) == 5:
        
        file_name = parse.file_name(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        alpha_count = parse.alpha_count(sys.argv[4])
        
        alpha_allowance = 0.1
        
    elif len(sys.argv) == 6:
        
        file_name = parse.file_name(sys.argv[1])
        dim = [parse.dim(sys.argv[2]), parse.dim(sys.argv[3])]
        alpha_count = parse.alpha_count(sys.argv[4])    
        alpha_allowance = parse.alpha_allowance(sys.argv[5])  
               
    else:
        
        raise KeyError("Too many input arguments")
    
    return file_name, dim, alpha_count, alpha_allowance

main()
