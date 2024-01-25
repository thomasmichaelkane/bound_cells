"""
This module provides functions for analyzing data related to Voronoi diagrams.

Module Functions:
- convert_dict(data_dict, factor): Multiply all values in a dictionary by a specified factor.
- get_icds(vor, cells): Calculate intercellular distances between specified cells in a Voronoi diagram.
- get_nn_distances(vor, cells): Calculate nearest neighbor distances for specified cells in a Voronoi diagram.
- get_areas(vor, cells): Calculate areas of regions around specified cells in a Voronoi diagram.
- get_alt_index(mean, area, num_points): Calculate an alternative index based on mean, area, and number of points.
- get_regularity_index(mean, std): Calculate a regularity index based on mean and standard deviation.
- get_neighbors(vor, cells): Count the number of neighbors for specified cells in a Voronoi diagram.
- mean_std_dict(data_dict): Calculate the mean and standard deviation of values in a dictionary.
"""

import numpy as np
from scipy.spatial import distance, KDTree
from scipy.stats.kde import gaussian_kde
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

from ..utils.utils import *
from ..utils.settings import display_settings

# Define the negative log likelihood function
def neg_log_likelihood(bandwidth, data):
    kde = gaussian_kde(data, bw_method=bandwidth)
    return -kde.logpdf(data).sum()

def get_optimal_bandwidth(data):
    # Create a parameter grid for bandwidth
    bandwidths = np.linspace(0, 10, 100)

    # Create the GridSearchCV object
    grid_search = GridSearchCV(KernelDensity(kernel='gaussian'),
                    {'bandwidth': bandwidths},
                    cv=2)
    
    # Fit the GridSearchCV object
    grid_search.fit(data)

    # Access the best bandwidth and the corresponding model
    best_bandwidth = grid_search.best_params_['bandwidth']
    return best_bandwidth
    
def kde_density(points, bandwidth, grid_density, cutoff):
    x, y = map(np.array, zip(*points))
    xy = np.vstack([x, y])
    
    k = gaussian_kde(xy, bw_method=bandwidth)

    xi, yi = np.mgrid[x.min():x.max():grid_density * 1j, y.min():y.max():grid_density * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    zi = np.array([d if d > zi.max()*cutoff else 0 for d in zi])
    
    average_density = len(points) / (np.ptp(x) * np.ptp(y))
    average_zi = zi.mean()
    pdf_scale = average_density / average_zi
    
    zi = zi * pdf_scale
    
    densities = (xi, yi, zi)
    
    return densities
    
    # # Get the maximum density value
    # max_density_per_mm = zi.max()
    # print(f"Maximum Density: {max_density_per_mm}")

def convert_dict(data_dict, factor):
    """
    Multiply all values in a dictionary by a specified factor.

    Parameters:
    - data_dict (dict): The input dictionary.
    - factor (float): The factor by which to multiply the values.

    Returns:
    - dict: A new dictionary with values multiplied by the factor.
    """
    new_dict = {key: value * factor for key, value in data_dict.items()}
    
    return new_dict

def get_icds(vor, cells):
    """
    Calculate intercellular distances between specified cells in a Voronoi diagram.

    Parameters:
    - vor (scipy.spatial.qhull.Voronoi): The Voronoi diagram.
    - cells (list): List of cell indices.

    Returns:
    - dict: A dictionary containing intercellular distances between specified cells.
    """
    icd = {}

    # Iterate over the ridges
    for ridge in vor.ridge_points:
        
        if ridge[0] in cells or ridge[1] in cells:
            
            # Get the indices of the cells that define the ridge
            cell_one, cell_two = ridge
            
            # Get the coordinates of the cells
            point_one = vor.points[cell_one]
            point_two = vor.points[cell_two]
            
            # Calculate the distance between the cells
            dist = distance.euclidean(point_one, point_two)
            cells_key = f"{cell_one}-{cell_two}"
            icd.update({cells_key: dist})

    return icd

def get_nn_distances(vor, cells):
    """
    Calculate nearest neighbor distances for specified cells in a Voronoi diagram.

    Parameters:
    - vor (scipy.spatial.qhull.Voronoi): The Voronoi diagram.
    - cells (list): List of cell indices.

    Returns:
    - dict: A dictionary containing nearest neighbor distances for specified cells.
    """
    tree = KDTree(vor.points)
    nn = {}

    for j in cells:
        point = vor.points[j]
        dist, index = tree.query(x=point, k=[2])
        nn_key = str(index.squeeze())
        nn.update({j: dist.squeeze()})

    return nn

def get_areas(vor, cells):
    """
    Calculate areas of regions around specified cells in a Voronoi diagram.

    Parameters:
    - vor (scipy.spatial.qhull.Voronoi): The Voronoi diagram.
    - cells (list): List of cell indices.

    Returns:
    - dict: A dictionary containing areas of regions around specified cells.
    """
    areas = {}

    for j in cells:
        region = vor.regions[vor.point_region[j]]
        polygon = [vor.vertices[i] for i in region]
        area = polygon_area(polygon)
        areas.update({j: area})

    return areas

def get_alt_index(mean, area, num_points):
    """
    Calculate an alternative index based on mean, area, and number of points.

    Parameters:
    - mean (float): The mean value.
    - area (float): The area.
    - num_points (int): The number of points.

    Returns:
    - float: The alternative index.
    """
    alt_index = mean / (0.5 * np.sqrt(area / num_points))
    
    return alt_index

def get_regularity_index(mean, std):
    """
    Calculate a regularity index based on mean and standard deviation.

    Parameters:
    - mean (float): The mean value.
    - std (float): The standard deviation.

    Returns:
    - float: The regularity index.
    """
    regularity_index = mean / std
    
    return regularity_index

def get_neighbors(vor, cells):
    """
    Count the number of neighbors for specified cells in a Voronoi diagram.

    Parameters:
    - vor (scipy.spatial.qhull.Voronoi): The Voronoi diagram.
    - cells (list): List of cell indices.

    Returns:
    - dict: A dictionary containing the number of neighbors for specified cells.
    """
    neighbors = {}

    for j in cells:
        region = vor.regions[vor.point_region[j]]
        polygon = [vor.vertices[i] for i in region]
        num_neighbors = len(polygon)
        neighbors.update({j: num_neighbors})

    return neighbors

def mean_std_dict(data_dict):
    """
    Calculate the mean and standard deviation of values in a dictionary.

    Parameters:
    - data_dict (dict): The input dictionary.

    Returns:
    - tuple: A tuple containing the mean and standard deviation.
    """
    dict_values = [value for value in data_dict.values()]
    mean = np.mean(dict_values)
    std = np.std(dict_values)

    return mean, std
