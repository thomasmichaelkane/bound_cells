"""
This module provides functions for geometric processing, including alpha shapes, graph operations, and boundary checking.

Module Functions:
- polygon_from_edges(points, edges): Extracts a subset of points forming a polygon from a set of edges.
- find_next_point(edge_pair, point_indices): Finds the next point index in a sequence of edges.
- add_edge(edges, i, j, only_outer): Adds an edge between two points if not in the list already.
- alpha_shape(points, alpha, only_outer=True): Computes the alpha shape (concave hull) of a set of points.
- get_outline(points, alpha): Retrieves the largest shape from the alpha shape.
- graph_from_edges(edges): Creates a graph from a set of edges.
- get_largest_subgraph(graph): Retrieves the largest subgraph from a graph.
- define_mask(): Defines an example mask as a Shapely Polygon.
- check_bound(vor, cell_id, mask): Checks if a Voronoi cell is within a specified mask.
"""

import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
import networkx as nx

from ..utils.utils import *
from ..visualization import display

import cv2
import numpy as np

def define_polygon(points, dim, thumbnail_factor=0.1):

    # Create a black image with a white background
    img = np.zeros((dim[0], dim[1], 3), dtype=np.uint8)
    img.fill(0)

    # Plot the points as red circles
    for point in points:
        cv2.circle(img, tuple(map(int, point)), 15, (0, 0, 255), -1)

    img = cv2.resize(img, (0,0), fx=thumbnail_factor, fy=thumbnail_factor) #cv2.flip( ,0)
    # Create an empty list to store the polygon vertices
    
    polygon_points = user_polygon(img)
    polygon_points = [(x*1/thumbnail_factor, dim[1]-y*1/thumbnail_factor) for (x, y) in polygon_points]
    
    return polygon_points
    
def user_polygon(img, name="Image"):
    
    polygon_points = []

    # Callback function for mouse events
    def draw_polygon(event, x, y, flags, param):
        nonlocal polygon_points

        if event == cv2.EVENT_LBUTTONDOWN:
            # Draw a point where the user clicked
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
            cv2.imshow(name, img)
            polygon_points.append((x, y))

    # Create a window and set the mouse callback
    cv2.namedWindow(name)
    cv2.setMouseCallback(name, draw_polygon)

    print("Click to define polygon vertices. Press 'c' to close the polygon when finished.")
    
    while True:
        cv2.imshow(name, img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            if len(polygon_points) >= 3:
                break
            else:
                print("Please define at least 3 vertices for the polygon.")
        elif key == 27:  # Press 'Esc' to exit without defining a polygon
            cv2.destroyAllWindows()
            return None

    cv2.destroyAllWindows()

    # Convert the list of points to a numpy array
    polygon_points = np.array(polygon_points)

    return polygon_points


def polygon_from_edges(points, edges):
    """
    Extracts a subset of points forming a polygon from a set of edges.

    Parameters:
    - points (np.array): An array of shape (n, 2) representing points.
    - edges (set): A set containing edges represented as (i, j) pairs.

    Returns:
    - list: A list of points forming the polygon subset.
    """
    initial_point_index = list(edges())[0][0]
    initial_edge_pair = list(edges(initial_point_index))

    point_indices = [initial_edge_pair[0][0], initial_edge_pair[0][1]]

    point_index = find_next_point(initial_edge_pair, point_indices)
    point_indices.append(point_index)

    for _ in range(len(edges) - 2):
        edge_pair = edges(point_index)
        point_index = find_next_point(edge_pair, point_indices)
        if point_index is not None:
            point_indices.append(point_index)

    subset = [points[i] for i in point_indices]

    return subset

def find_next_point(edge_pair, point_indices):
    """
    Finds the next point index in a sequence of edges.

    Parameters:
    - edge_pair (set): A set of two edges.
    - point_indices (list): A list of indices representing points.

    Returns:
    - int or None: The next point index, or None if not found.
    """
    flat_edge = list(set([index for edge in edge_pair for index in edge]))

    try:
        point_index = list(set(flat_edge).difference(point_indices))[0]
    except IndexError:
        point_index = None

    return point_index

def add_edge(edges, i, j, only_outer):
    """
    Add an edge between the i-th and j-th points if not in the list already.

    Parameters:
    - edges (set): A set containing edges represented as (i, j) pairs.
    - i (int): Index of the first point.
    - j (int): Index of the second point.
    - only_outer (bool): If True, only add edges that are part of the outer border.

    Returns:
    - None
    """
    if (i, j) in edges or (j, i) in edges:
        assert (j, i) in edges
        if only_outer:

            edges.remove((j, i))
        return
    edges.add((i, j))

def alpha_shape(points, alpha, only_outer=True):
    """
    Compute the alpha shape (concave hull) of a set of points.

    Parameters:
    - points (np.array): An array of shape (n, 2) representing points.
    - alpha (float): The alpha value.
    - only_outer (bool): If True, only keep the outer border; otherwise, include inner edges as well.

    Returns:
    - set: A set of (i, j) pairs representing edges of the alpha-shape. (i, j) are the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    tri = Delaunay(points)
    edges = set()

    # Loop over triangles: ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]

        # Computing radius of triangle circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)

        if circum_r < alpha:
            add_edge(edges, ia, ib, only_outer)
            add_edge(edges, ib, ic, only_outer)
            add_edge(edges, ic, ia, only_outer)

    return edges

def get_outline(points, alpha):
    """
    Retrieves the largest shape from the alpha shape.

    Parameters:
    - points (np.array): An array of shape (n, 2) representing points.
    - alpha (float): The alpha value.

    Returns:
    - set: A set of (i, j) pairs representing edges of the alpha-shape forming the largest shape. (i, j) are the indices in the points array.
    """
    init_edges = alpha_shape(points, alpha=alpha, only_outer=True)
    graph = graph_from_edges(init_edges)
    largest_shape = get_largest_subgraph(graph)

    return largest_shape

def graph_from_edges(edges):
    """
    Creates a graph from a set of edges.

    Parameters:
    - edges (set): A set containing edges represented as (i, j) pairs.

    Returns:
    - nx.Graph: A networkx graph.
    """
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph

def get_largest_subgraph(graph):
    """
    Retrieves the largest subgraph from a graph.

    Parameters:
    - graph (nx.Graph): A networkx graph.

    Returns:
    - nx.Graph: The largest subgraph.
    """
    connected_sets = nx.connected_components(graph)
    subgraphs = []

    for set in connected_sets:
        subgraph = graph.subgraph(set)
        subgraphs.append(subgraph)

    largest = max(subgraphs, key=lambda x: x.number_of_nodes())
    return largest

def define_mask():
    """
    Defines an example mask as a Shapely Polygon.

    Returns:
    - Polygon: A Shapely Polygon representing an example mask.
    """
    example_mask = Polygon([(50, 50), (50, 100), (100, 50), (100, 100)])
    return example_mask

def check_bound(vor, cell_id, mask):
    """
    Checks if a Voronoi cell is within a specified mask.

    Parameters:
    - vor: Voronoi diagram object.
    - cell_id (int): Index of the Voronoi cell.
    - mask (Polygon): Shapely Polygon representing the mask.

    Returns:
    - bool: True if the Voronoi cell is within the mask; False otherwise.
    """
    region = vor.regions[vor.point_region[cell_id]]
    mask_poly = Polygon(mask)
    cell = Polygon([vor.vertices[i] for i in region])

    if (-1 in region) or (cell == []):
        return False

    if mask_poly.contains(cell):
        return True
    else:
        return False
    
def test_alpha(points, alpha, count, allowance):
    """
    Test the effect of different alpha values on the Voronoi diagram of a set of points.

    Parameters
    ----------
    points (np.array): An array of shape (n, 2) representing the coordinates of the points.
    alpha (float): The starting alpha value.
    count (int): The number of alpha values to generate.
    allowance (float): The step size between consecutive alpha values.

    Returns
    -------
    list: A list of alpha values used in the test.
    """
    
    alphas = alpha_linspace(alpha, count, allowance)
    outlines = [get_outline(points, alpha) for alpha in alphas]
    edge_sets = [outline.edges() for outline in outlines]
    display.alpha_plots(edge_sets, points, alphas)
    
    return alphas
