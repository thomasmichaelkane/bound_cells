"""
This module provides functions for various geometric and data processing tasks.

Module Functions:
- get_id(file_name): Generates an ID based on the provided file name.
- auto_dim(num_seeds, density_per_mm2, mpp): Calculates the dimensions of a square area.
- inc_range(start, stop): Returns a range from start to stop (inclusive).
- check_euc_min(seed, other, euc_min): Checks if the Euclidean distance between two points is greater than or equal to a specified minimum.
- polygon_area(vertices): Calculates the area of a polygon.
- mask_area(mask): Calculates the area of a binary mask.
- round_vertices(vertices): Rounds the coordinates of vertices to integers.
- csv_to_list(file_name): Reads a CSV file and returns its content as a list.
- coords_as_np(coords): Converts a list of coordinates to a NumPy array.
- alpha_linspace(middle, count, allowance): Generates a list of alpha values in a linear space around a middle value.
- calc_area(dim): Calculates the area of a rectangle.
- scale(points, dim): Scales a set of points based on the dimensions of a rectangle.
- save_cell_data(nn, vd, numn, name): Saves the nearest neighbor (nn), voronoi areas (vd), and number of neighbors (numn), to a csv file.
"""

import csv
import numpy as np
from scipy.spatial import distance
from shapely.geometry import Polygon

def rotate_coordinates_90_degrees(num, coordinates, dim):
    
    for _ in range(num):
        coordinates = [(y, dim[0]-x) for x, y in coordinates]
        dim = (dim[1], dim[0])
    return coordinates, dim

def get_id(file_name):
    
    file_no_ext = file_name.split('.')[0]
    file_id = file_no_ext + "_cell_stats"
    
    return file_id

def auto_dim(num_seeds, density_per_mm2, mpp):
    
    density_pix = (density_per_mm2 / 1_000_000)*(mpp**2)
    area = num_seeds / density_pix
    dim = round(np.sqrt(area))
    
    return [dim, dim]

def inc_range(start, stop):

    return range(start, stop+1)

def check_euc_min(seed, other, euc_min):
    
    separation = distance.euclidean(seed, other)
    
    if separation >= euc_min:
        return True
    else:
        return False
    
def polygon_area(vertices):
    
    poly = Polygon(vertices)
    
    return poly.area

def mask_area(mask):
    
    return mask.sum()
    
def round_vertices(vertices):
    
    rounded = [(int(round(x)), int(round(y))) for [x, y] in vertices]
    
    return rounded
    
def csv_to_list(file_name):
    
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        
        return list(reader)

def coords_as_np(coords):
    
    coords_float = [[float(p[0]), float(p[1])] for p in coords]
    array = np.array(coords_float)
    
    return array

def alpha_linspace(middle, count, allowance):

    linspace = np.linspace(1-allowance, 1+allowance, count)
    alphas = [round(middle*weight) for weight in linspace]
    
    return alphas

def calc_area(dim):
    
    area = dim[0] * dim[1]
    
    return area    

def scale(points, dim):
    
    points_scaled = [[p[0]*dim[0], p[1]*dim[1]] for p in points]
    
    return points_scaled

def save_to_text(filename, values):
    
    with open(filename, 'w') as file:
        
        for value in values:
            # write each item on a new line
            file.write(f"{value}\n")

def save_image(filename, img):
    
    img.save(filename)

def save_cell_data(nn, vd, numn, name):

    csv_filename = name + ".csv"

    with open(csv_filename, 'w', newline='') as csvFile:
        
        cell_writer = csv.writer(csvFile)
        header = ["Cell ID", "Nearest Neighbour (um)", "Voronoi Domain Area (um2)", "Number of Neighbours"]
        cell_writer.writerow(header)
        
        for i in nn:
            
            row = [i, nn[i], vd[i], numn[i]]
            cell_writer.writerow(row)
