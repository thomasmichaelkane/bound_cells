"""Create many random cell distributions for averaged statistics.

This script will create many random cell mosaics which can be averaged
to acquire robust statistics to compare with real cell distributions.

Example
-------
Use the command line interface to create random cell distributions
with variables specified in following arguments. Here we are 
creating 100 random cell distribution with 1000 seeds (cells), with
a density of 300pmm2, a scaling of 1.4mpp, and a minimum separation 
of 10 pixels::

    $ python random_average.py 100 1000 1.4 300.0 10.0

Notes
-----
    Further settings with more details can be altered in the settings 
    file. Dimensions and separation are denoted in pixels for the sake
    of visualisation, but the numbers are arbitrary in this conext,
    so they can entered in and thought of as microns.

Arguments
----------
{optional} number of iterations : int
    The number of iterations to run before finding an average. The default value is 10.
    
{optional} number of cells : int
    The number of cells. How many cells will be distributed. The default value is 100.

{optional} microns per pixel : float
    The scaling factor. How many microns per pixel in the original image. The default value is 1 (1um=1pix).
   
{optional} density : float
    The density of the cells (per mm2). The default value is 1000.
    
{optional} minimum separation : float
    The minimum separation between cells. Bare in mind this number cannot
    be too high, or the program will fail, as it will not be able to find
    new locations that are at the minimum separation. The default value is 
    0. (PIXELS)
"""
    
import sys

from bound_cells import CellDist
from bound_cells.cells import seeds
from bound_cells.utils import parse
from bound_cells.utils.util_functions import *

def main():
    
    NUM_ITER, NUM_SEEDS, MPP, DENSITY, MIN_SEP = parse_args()
    DIM = auto_dim(NUM_SEEDS, DENSITY, MPP)  
    
    dists = []
    
    for i in range(NUM_ITER):
        
        min_sep_pix = round(MIN_SEP / MPP)
        points = seeds.generate(NUM_SEEDS, DIM, min_sep_pix)
        dist = CellDist(points, DIM, MPP, id=i)
        dist.calc_stats()
        stats = dist.get_bound_stats()
        dists.append(stats)
        
        print('--ITER-{:.0f}--N-{:.2f}--DEN-{:.2f}--NN-{:.2f}--VD-{:.2f}--NNRI-{:.4f}--VDRI-{:.4f}--ANNRI-{:.4f}-- '
                .format(stats["id"],
                        stats["num_bound_cells"],
                        stats["bound_density"],
                        stats["mean_nn"],
                        stats["mean_vd"],
                        stats["nnri"],
                        stats["vdri"],
                        stats["alt_nnri"]))
    
    glob_stats = {
            "num_bound_cells": sum(s["num_bound_cells"] for s in dists) / len(dists),
            "total_bound_area": sum(s["total_bound_area"] for s in dists) / len(dists),
            "bound_density": sum(s["bound_density"] for s in dists) / len(dists),
            "mean_icd": sum(s["mean_icd"] for s in dists) / len(dists),
            "std_icd": sum(s["std_icd"] for s in dists) / len(dists),
            "mean_nn": sum(s["mean_nn"] for s in dists) / len(dists),
            "std_nn": sum(s["std_nn"] for s in dists) / len(dists),
            "mean_vd": sum(s["mean_vd"] for s in dists) / len(dists),
            "std_vd": sum(s["std_vd"] for s in dists) / len(dists),
            "mean_num_neighbors": sum(s["mean_num_neighbors"] for s in dists) / len(dists),
            "std_num_neighbors": sum(s["std_num_neighbors"] for s in dists) / len(dists),
            "nnri": sum(s["nnri"] for s in dists) / len(dists),
            "vdri": sum(s["vdri"] for s in dists) / len(dists),
            "alt_nnri": sum(s["alt_nnri"] for s in dists) / len(dists)
        }
    
    # print(glob_stats)
    
def parse_args():

    if len(sys.argv) == 1:
        
        num_iter = 10
        num_seeds = 100
        mpp = 1
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 2:
        
        num_iter = parse.iter(sys.argv[1])
        
        num_seeds = 100
        mpp = 1
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 3:
        
        num_iter = parse.iter(sys.argv[1])
        num_seeds = parse.num_seeds(sys.argv[2])
        
        mpp = 1
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 4:
        
        num_iter = parse.iter(sys.argv[1])
        num_seeds = parse.num_seeds(sys.argv[2])
        mpp = parse.mpp(sys.argv[3])
            
        density = 1000
        min_sep = 0
        
    elif len(sys.argv) == 5:
        
        num_iter = parse.iter(sys.argv[1])
        num_seeds = parse.num_seeds(sys.argv[2])
        mpp = parse.mpp(sys.argv[3])
        density = parse.density(sys.argv[4])
        
        min_sep = 0
        
    elif len(sys.argv) == 6:
        
        num_iter = parse.iter(sys.argv[1])
        num_seeds = parse.num_seeds(sys.argv[2])
        mpp = parse.mpp(sys.argv[3])
        density = parse.density(sys.argv[4])
        min_sep = parse.min_sep(sys.argv[5])
        
    else:
        
        raise KeyError("Too many input arguments")
        
    return num_iter, num_seeds, mpp, density, min_sep
    
main()