"""
This module provides functions for visualizing data, including histograms, point plots, Voronoi diagrams, and alpha plots.

Module Functions:
- histogram(pop, xlabel, bins=15): Displays a histogram of a given population.
- plot_text(x, y, text, color, size): Plots text at a specified position on the graph.
- plot_point(x, y, index=None, neighbors=None, style='.', color="r", size="3"): Plots a point on the graph.
- plot_sides(polygon): Plots the sides of a polygon on the graph.
- fill_cell(polygon, color): Fills the interior of a polygon with a specified color.
- show_voronoi(vor, cells): Displays a Voronoi diagram.
- add_neighbor_legend(ax): Adds a legend for the number of neighbors in a Voronoi diagram.
- get_neighbors_color(num_neighbors): Calculates the color based on the number of neighbors.
- show_polygon(polygon_vertices, dim, points=None): Displays a polygon on the graph.
- alpha_plots(edge_sets, points, alphas): Displays alpha plots based on edge sets and points.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors, patches

from ..utils.utils import *
from ..utils.enums import PointType
from ..utils.settings import display_settings

def contour_plot(points, densities, contour_levels):
    pcm = density_plot(points, densities, show=False)
    plt.close()
    x, y = map(np.array, zip(*points))
    (xi, yi, zi) = densities

    fig = plt.figure(figsize=(7,8))
    ax = fig.add_subplot(111)
    
    # Create more contour levels
    contour_levels = np.linspace(zi.min(), zi.max(), contour_levels)

    ax.contourf(xi, yi, zi.reshape(xi.shape), contour_levels, alpha=1)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())

    ax.set_aspect('equal')
    
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label('Density (cells/mm²)')
    
    plt.gca().invert_yaxis()
    plt.show()

def density_plot(points, densities, show=True):
    x, y = map(np.array, zip(*points))
    (xi, yi, zi) = densities

    fig = plt.figure(figsize=(7,8))
    ax = fig.add_subplot(111)
    
    pcm = ax.pcolormesh(xi, yi, zi.reshape(xi.shape), alpha=1)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    ax.set_aspect('equal')
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label('Density (cells/mm²)')
    
    if show:
        plt.gca().invert_yaxis()
        plt.show()
    
    return pcm

def histogram_list(pop_list, xlabel, bins=15):
    """
    Displays a histogram of a given population.

    Parameters:
    - pop (list): Population data in list format.
    - xlabel (str): Label for the x-axis.
    - bins (int): Number of bins in the histogram.

    Returns:
    - None
    """
    plt.hist(pop_list, bins=bins)
    plt.xlabel(xlabel)
    plt.show()

def histogram(pop, xlabel, bins=15):
    """
    Displays a histogram of a given population.

    Parameters:
    - pop (dict): Population data in dictionary format.
    - xlabel (str): Label for the x-axis.
    - bins (int): Number of bins in the histogram.

    Returns:
    - None
    """
    pop_list = list(pop.values())
    plt.hist(pop_list, bins=bins)
    plt.xlabel(xlabel)
    plt.show()

def plot_text(x, y, text, color, size):
    """
    Plots text at a specified position on the graph.

    Parameters:
    - x (float): X-coordinate of the text position.
    - y (float): Y-coordinate of the text position.
    - text (str): Text to be displayed.
    - color (str): Color of the text.
    - size (int): Font size of the text.

    Returns:
    - None
    """
    plt.text(x, y, text, fontdict=None, ha="center", va="center", color=color, fontsize=size)

def plot_point(x, y, index, neighbors, type, style, color, size):
    """
    Plots a point on the graph.

    Parameters:
    - x (float): X-coordinate of the point.
    - y (float): Y-coordinate of the point.
    - index (int): Index value for the point.
    - neighbors (int): Number of neighbors for the point.
    - type (PointType): Type of point.
    - style (str): Marker style for the point.
    - color (str): Color of the point.
    - size (int): Size of the point.

    Returns:
    - None
    """
    if type == PointType.INDEX:
        plot_text(x, y, index, color, size)
    elif type == PointType.NEIGHBORS:
        plot_text(x, y, neighbors, color, size)
    else:
        plt.plot(x, y, marker=style, color=color, markersize=size)

def plot_sides(polygon, color, linewidth):
    """
    Plots the sides of a polygon on the graph.

    Parameters:
    - polygon (list): List of (x, y) coordinates representing the polygon.

    Returns:
    - None
    """
    first_vertex = polygon[0]
    polygon.append(first_vertex)
    plt.plot(*zip(*polygon), color, linewidth)

def fill_cell(polygon, color):
    """
    Fills the interior of a polygon with a specified color.

    Parameters:
    - polygon (list): List of (x, y) coordinates representing the polygon.
    - color (str): Color for filling the polygon.

    Returns:
    - None
    """
    plt.fill(*zip(*polygon), color)

def show_voronoi(vor, cells, fill, point_type, point_style, point_color, point_size, line_color, line_width, neighbor_scale, neighbor_colormap):
    """
    Displays a Voronoi diagram.

    Parameters:
    - vor: Voronoi diagram object.
    - cells (list): List of indices representing Voronoi cells.

    Returns:
    - None
    """
    ax = plt.axes()

    for j in cells:
        region = vor.regions[vor.point_region[j]]
        (x, y) = vor.points[j]
        cell_polygon = [vor.vertices[i] for i in region]
        num_neighbors = len(cell_polygon)

        plot_sides(cell_polygon, line_color, line_width)

        if fill is True:
            color = get_neighbors_color(num_neighbors, neighbor_scale, neighbor_colormap)
            fill_cell(cell_polygon, color)

        if point_type is not PointType.NONE:
            plot_point(x, y, index=j,
                       neighbors=num_neighbors,
                       type=point_type,
                       style=point_style,
                       color=point_color,
                       size=point_size)

    if fill is True:
        add_neighbor_legend(ax, neighbor_scale, neighbor_colormap)

    ax.set_aspect("equal")
    plt.gca().invert_yaxis()
    plt.show()

def add_neighbor_legend(ax, scale, colormap):
    """
    Adds a legend for the number of neighbors in a Voronoi diagram.

    Parameters:
    - ax: Matplotlib axis object.

    Returns:
    - None
    """
    legend_patches = []
    neighbor_range = inc_range(*scale)

    for i in neighbor_range:
        color = get_neighbors_color(i, scale, colormap)
        patch = patches.Patch(color=color, label=i)
        legend_patches.append(patch)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    ax.legend(handles=legend_patches, loc="right", bbox_to_anchor=(1.2, 0.5), fancybox=True, shadow=True)

def get_neighbors_color(num_neighbors, scale, colormap):
    """
    Calculates the color based on the number of neighbors.

    Parameters:
    - num_neighbors (int): Number of neighbors for a Voronoi cell.

    Returns:
    - str: Hex color code.
    """
    alpha = (num_neighbors - scale[0]) * (1 / (scale[1] - scale[0]))
    cmap = cm.get_cmap(colormap)
    color = colors.to_hex(cmap(alpha))
    return color

def show_polygon(polygon_vertices, dim, mask_color, point_color, point_size, points=None):
    """
    Displays a polygon on the graph.

    Parameters:
    - polygon_vertices (list): List of (x, y) coordinates representing the polygon.
    - dim (tuple): Dimensions of the graph.
    - points (list): List of (x, y) coordinates representing points to be plotted.

    Returns:
    - None
    """
    fig, ax = plt.subplots()

    polygon = patches.Polygon(polygon_vertices,
                              closed=True,
                              fill=True,
                              color=mask_color)

    if points is not None:
        for (x, y) in points:
            plot_point(x, y,
                       color=point_color,
                       size=point_size)

    ax.add_patch(polygon)
    ax.set_xlim([0, dim[0]])
    ax.set_ylim([0, dim[1]])
    plt.show()

def alpha_plots(edge_sets, points, alphas):
    """
    Displays alpha plots based on edge sets and points.

    Parameters:
    - edge_sets (list): List of sets representing edges.
    - points (np.array): Array of shape (n, 2) representing points.
    - alphas (list): List of alpha values.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(18, 4))
    num_plots = len(alphas)

    for k, alpha in enumerate(alphas):
        plt.subplot(1, num_plots, k + 1)
        plt.plot(points[:, 0], points[:, 1], '.')
        for i, j in edge_sets[k]:
            plt.plot(points[[i, j], 0], points[[i, j], 1])

        plt.text(2000, 6200, f"alpha={alpha}", size=18)

    plt.show()
