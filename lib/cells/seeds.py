"""
This module provides functions for generating random points with optional minimum separation.

Module Functions:
- generate(num_points, dim, min_separation=None): Generates random points within a specified dimension.
- generate_with_min_sep(num_points, dim, min_separation): Generates random points with a minimum separation constraint.
- seed_with_min_sep(population, dim, min_separation): Generates a single random seed with minimum separation.
"""

import numpy as np

from ..utils.utils import *

def generate(num_points, dim, min_separation=None):
    """
    Generate random points within a specified dimension.

    Parameters:
    - num_points (int): The number of points to generate.
    - dim (list): The dimensions [width, height] of the area in which to generate points.
    - min_separation (float or None): Minimum Euclidean separation between points. If None, generate random points without constraints.

    Returns:
    - numpy.ndarray: An array containing the generated points.
    """
    if min_separation is not None:
        seeds = generate_with_min_sep(num_points, dim, min_separation)
    else:
        seeds = np.random.rand(num_points, 2)
        seeds = scale(seeds, dim)

    return seeds

def generate_with_min_sep(num_points, dim, min_separation):
    """
    Generate random points with a minimum separation constraint.

    Parameters:
    - num_points (int): The number of points to generate.
    - dim (list): The dimensions [width, height] of the area in which to generate points.
    - min_separation (float): Minimum Euclidean separation between points.

    Returns:
    - numpy.ndarray: An array containing the generated points with minimum separation.
    """
    first_seed = [np.random.random() * dim[0], np.random.random() * dim[1]]
    seeds = [first_seed]

    for _ in range(1, num_points):
        new_seed = seed_with_min_sep(seeds, dim, min_separation)
        seeds.append(new_seed)

    return seeds

def seed_with_min_sep(population, dim, min_separation):
    """
    Generate a single random seed with a minimum separation from an existing population.

    Parameters:
    - population (list): List of existing points.
    - dim (list): The dimensions [width, height] of the area in which to generate points.
    - min_separation (float): Minimum Euclidean separation between points.

    Returns:
    - list: A randomly generated seed with minimum separation from the existing population.
    """
    euc_min = False

    while euc_min is False:
        rand_seed = [np.random.random() * dim[0], np.random.random() * dim[1]]

        for other_seed in population:
            euc_min = check_euc_min(rand_seed, other_seed, min_separation)
            if euc_min is False:
                break

    return rand_seed
