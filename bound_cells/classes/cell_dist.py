"""
This class represents a distribution of cells and provides methods for analyzing and visualizing cell distributions.

Class Attributes:
- points (list): List of points representing cell coordinates.
- dim (tuple): Dimensions of the image.
- mpp (float): Microns per pixel.
- id (str): Identifier for the cell distribution.

Instance Attributes:
- points_array (np.array): Numpy array of points.
- alpha_override (float): Override value for the alpha parameter.
- dil_factor_override (float): Override value for the dilation factor.
- alpha (float): Alpha parameter for the Voronoi diagram.
- dilation_strength (float): Strength of dilation for border expansion.
- stat_prec (int): Precision for statistical values.
- vor (scipy.spatial.Voronoi): Voronoi diagram object.
- image_area (float): Area of the image.
- estimated_area (float): Estimated area of the cell distribution.
- num_unbound_cells (int): Number of unbound cells.
- cells (list): List of cell indices.
- dilated_poly (list): List of vertices for the dilated polygon.
- bound_cells (list): List of indices for bound cells.
- num_bound_cells (int): Number of bound cells.

Methods:
- set_dilation_factor(): Sets the dilation factor based on the override value.
- find_bound_cells(): Finds bound cells using the Voronoi diagram and dilated polygon.
- update_alpha(new_alpha): Updates the alpha parameter with a new value.
- find_border(): Finds the border of the cell distribution using the Voronoi diagram.
- dilate_border(): Dilates the border of the cell distribution.
- show_voronoi(): Displays the Voronoi diagram for bound cells.
- show_voronoi_unbound(): Displays the Voronoi diagram for all cells.
- show_points_with_border(): Displays the cell distribution with the dilated border.
- show_mask(): Displays the mask image.
- show_dil_mask(): Displays the dilated mask image.
- calc_stats(): Calculates various statistical measures for the cell distribution.
- show_histograms(): Displays histograms for various statistical measures.
- print_report_full(): Prints a detailed report with global and bound cell statistics.
- print_report(): Prints a concise report with key statistical measures.
- save(): Saves cell data to an output file.
- get_bound_stats(): Retrieves statistics for bound cells.
- get_icd(): Retrieves the mean inter-cell distance.
- get_nn(): Retrieves the mean nearest neighbor distance.
- get_mean_cell_area(): Retrieves the mean Voronoi domain cell area.
- get_nnri(): Retrieves the nearest neighbor regularity index.
- get_alt_nnri(): Retrieves an alternative nearest neighbor regularity index.
- get_vdri(): Retrieves the Voronoi domain regularity index.
- get_points_array(): Retrieves the array of cell points.
- get_area(): Retrieves the estimated area of the cell distribution.
"""

from scipy.spatial import Voronoi

from bound_cells.cells import stats, geometry
from bound_cells.visualization import display, image_manip
from bound_cells.utils.util_functions import *
from bound_cells.utils.enums import PointType

class CellDist:
    def __init__(self, points, dim, mpp=1, id=None):
        """
        Initializes a CellDist object.

        Parameters:
        - points (list): List of points representing cell coordinates.
        - dim (tuple): Dimensions of the image.
        - mpp (float): Microns per pixel.
        - id (str): Identifier for the cell distribution.
        """
        self.points = points
        self.dim = dim
        self.id = id
        self.mpp = mpp
        
        self.points_array = coords_as_np(self.points)
        
        self.density_rois = {}
        
        self.stat_prec = 3
        
        self.vor = Voronoi(self.points)
        self.image_area = calc_area(self.dim)
        self.estimated_area = self.image_area
        
        self.num_unbound_cells = len(self.vor.points)
        self.cells = [i for i in range(self.num_unbound_cells)]
        self.num_bound_cells = self.num_unbound_cells
        self.bound_cells = self.cells
                      
        self.poly = [(0, 0), (self.dim[0], 0), (self.dim[0], self.dim[1]), (0, self.dim[1]), (0, 0)]
        self.mask, self.mask_img = image_manip.polygon_to_mask(self.poly, self.dim)#, style=style, show=show)

        self.calc_stats()
        self.find_border()
        self.find_bound_cells()
        
    def find_bound_cells(self):

        self.bound_cells = [i for i in range(self.num_unbound_cells) if geometry.check_bound(self.vor, i, self.poly)] 
        self.num_bound_cells = len(self.bound_cells)
    
    def find_border(self, custom_alpha=None):
        
        self.alpha = self.mean_icd if custom_alpha is None else custom_alpha 
            
        edges = geometry.get_outline(self.points, self.alpha).edges()
    
        self.poly = round_vertices(geometry.polygon_from_edges(self.points, edges))
        self.mask, self.mask_img = image_manip.polygon_to_mask(self.poly, self.dim)#, style=style, show=show)
        
        self.orig_mask = self.mask
        self.orig_poly = self.poly
    
    def find_densities(self, bandwidth=0.1, grid_density=500, cutoff=None):
        
        self.grid_density = grid_density
        (x, y, z) = stats.kde_density(self.points, bandwidth, grid_density, cutoff)
        z_per_mm = z* 1_000_000*(1/self.mpp)
        self.densities = (x, y, z_per_mm)
        self.density_view_scale = 750/self.grid_density
        self.dmap, self.dmap_scaled = image_manip.density_map(self.densities, self.density_view_scale)
    
    def dilate_border(self, dilation_factor=0.5):

        self.dilation_strength = dilation_factor * self.alpha
        
        self.mask, self.dil_img = image_manip.dilate_mask(self.mask, strength=self.dilation_strength)#, show=show)
        self.poly = image_manip.mask_to_polygon(self.mask)
        
        self.estimated_area = mask_area(self.mask)
        
        self.find_bound_cells()
        self.calc_stats()
        
    def get_user_defined_border(self):
        
        self.poly = geometry.define_polygon(self.points, self.dim)
        self.mask, self.mask_img = image_manip.polygon_to_mask(self.poly, self.dim)#, style=style, show=show)
        
        self.find_bound_cells()

    def show_voronoi(self, 
                     bound=True, 
                     fill=True, 
                     point_type=PointType.POINT, 
                     point_style=".", 
                     point_color='black', 
                     point_size=3, 
                     line_color="black", 
                     line_width=1, 
                     neighbor_scale=[3, 10], 
                     neighbor_colormap="Oranges"):
        
        cells = self.bound_cells if bound is True else self.cells
        
        display.show_voronoi(self.vor,
                             self.dim, 
                             cells,
                             fill, 
                             point_type, 
                             point_style, 
                             point_color, 
                             point_size,
                             line_color,
                             line_width,
                             neighbor_scale,
                             neighbor_colormap)
    
    def show_points_with_border(self, mask_color="red", point_color="white", point_size=3):
        
        display.show_polygon(self.poly, 
                             self.dim,
                             mask_color, 
                             point_color, 
                             point_size,  
                             self.points_array)
        
    def show_density_plot(self):
        
        display.density_plot(self.points, self.densities)
        
    def show_contour_plot(self, contour_levels):
        
        display.contour_plot(self.points, self.densities, contour_levels)
        
    # def show_densities_as_image(self):
        
    #     self.roi_densities, self.roi_overlay = image_manip.density_map(self.densities)

    def define_density_roi(self, name):
        
        if self.density_rois.get(name) is None:
            self.density_rois.update({name: image_manip.user_density_roi(self.dmap_scaled, self.grid_density, self.density_view_scale, name)})
        else:
            print("An ROI with that name already exists")

    def show_density_rois(self):
        
        if len(self.density_rois) > 0:
            self.roi_densities, self.roi_overlay = image_manip.show_density_rois(self.densities, self.density_rois, self.dmap, self.grid_density)
        else:
            print("no rois have been defined")

    def save_rois(self, filename):
        
        for key, roi in self.roi_densities.items():
            roi_name = filename + "_roi_" + key + ".txt"
            save_to_text(roi_name, roi)
        
        overlay_name = filename + "_overlay.tif"
        save_image(overlay_name, self.roi_overlay)

    def show_mask(self):
        
        self.mask_img.show()
        
    def show_dil_mask(self):
        
        self.dil_img.show()
      
    def calc_stats(self):

    ## Global
        # (Estimated) Total Retina Area (microns)
        self.estimated_area_um = self.estimated_area * (self.mpp**2)
        # (Estimated) Cell Density (cells per mm^2)
        self.estimated_density = self.num_unbound_cells / self.estimated_area_um * 1_000_000

    ## Bound
        # Mean Inter Cell Distance (microns) +- ICD_std
        self.icd = stats.get_icds(self.vor, self.bound_cells)
        self.icd_um = stats.convert_dict(self.icd, self.mpp)
        self.mean_icd, self.std_icd = stats.mean_std_dict(self.icd)
        self.mean_icd_um, self.std_icd_um = self.mean_icd * self.mpp, self.std_icd * self.mpp
        
        # Mean Nearest Neighbor (microns) +- NN_std  
        self.nn = stats.get_nn_distances(self.vor, self.bound_cells)
        self.nn_um = stats.convert_dict(self.nn, self.mpp)
        self.mean_nn, self.std_nn = stats.mean_std_dict(self.nn)
        self.mean_nn_um, self.std_nn_um = self.mean_nn * self.mpp, self.std_nn * self.mpp
        
        # Mean Voronoi Domain Cell Area (microns^2) +- VD_std    
        self.vd_areas = stats.get_areas(self.vor, self.bound_cells)
        self.vd_um = stats.convert_dict(self.vd_areas, self.mpp)
        self.mean_vd, self.std_vd = stats.mean_std_dict(self.vd_areas)
        self.mean_vd_um, self.std_vd_um = self.mean_vd * (self.mpp**2), self.std_vd * (self.mpp**2)
        
        # Mean Number of Neighbors  +- NumN_std   
        self.num_neighbors = stats.get_neighbors(self.vor, self.bound_cells)
        self.mean_num_neighbors, self.std_num_neighbors = stats.mean_std_dict(self.num_neighbors)
        
        # Total (VD) Area (microns)
        self.total_vd_area_um = sum(self.vd_areas.values()) * (self.mpp**2)
        # Cell Density (cells per mm^2)
        self.bound_density = (self.num_bound_cells / self.total_vd_area_um) * 1_000_000
        
        # Nearest Neighbor Regularity Index
        self.nnri = stats.get_regularity_index(self.mean_nn, self.std_nn)
        # Voronoi Domain Regularity Index
        self.vdri = stats.get_regularity_index(self.mean_vd, self.std_vd)
        # Alteranative NNRI
        self.alt_nnri = stats.get_alt_index(self.mean_nn, self.total_vd_area_um, self.num_bound_cells)

    def show_histograms(self):
        
        display.histogram(self.icd_um, "ICD (um)")
        display.histogram(self.nn_um, "Nearest Neighbour Distance (um)")
        display.histogram(self.vd_um, "VD Cell Area (um2)")
        display.histogram(self.num_neighbors, "Number of Neighbours", bins=6)

    def print_report_full(self):
        
        print('______________________________________________________________________________')
        print('\n')
        
        print('_________________Global____________________\n')
        print('ID                                         {}'.format(self.id))
        print('Image dimensions (pixels)                  {} x {}'.format(self.dim[0], self.dim[1]))
        print('Image area (pixels^2)                      {:.0f}'.format(self.image_area, prec=self.stat_prec))
        print('Microns per pixel                          {:.{prec}f}'.format(self.mpp, prec=self.stat_prec))
        if self.alpha is not None:
            print('Alpha value                            {:.{prec}f}'.format(self.alpha, prec=self.stat_prec))
            # print('Dilation factor                        {:.{prec}f}'.format(self.dilation_factor, prec=self.stat_prec))
        
        print('_________________Unbound___________________\n')
        print('Total number of cells                      {}'.format(self.num_unbound_cells))
        print('(Estimated) Retina area (microns^2)        {:.0f}'.format(self.estimated_area_um, prec=self.stat_prec))
        print('(Estimated) Cell density (cells per mm^2)  {:.0f}'.format(self.estimated_density, prec=self.stat_prec))
      
        print('_________________Bound_____________________\n')
        print('Mean ICD (microns)                         {:.{prec}f} +- {:.{prec}f}'.format(self.mean_icd_um, self.std_icd_um, prec=self.stat_prec))
        print('Mean NN (microns)                          {:.{prec}f} +- {:.{prec}f}'.format(self.mean_nn_um, self.std_nn_um, prec=self.stat_prec))
        print('Mean VD cell area (microns)                {:.{prec}f} +- {:.{prec}f}'.format(self.mean_vd_um, self.std_vd_um, prec=self.stat_prec))
        print('Mean number of neighbors                   {:.{prec}f} +- {:.{prec}f}'.format(self.mean_num_neighbors, self.std_num_neighbors, prec=self.stat_prec))
        print('Number of bound cells                      {}'.format(self.num_bound_cells))
        print('Total VD area                              {:.{prec}f}'.format(self.total_vd_area_um, prec=self.stat_prec))
        print('(True) Bound cell density (cells per mm^2) {:.{prec}f}'.format(self.bound_density, prec=self.stat_prec))
        print('NNRI                                       {:.{prec}f}'.format(self.nnri, prec=self.stat_prec))
        print('VDRI                                       {:.{prec}f}'.format(self.vdri, prec=self.stat_prec))
        print('ALT NNRI                                   {:.{prec}f}'.format(self.alt_nnri, prec=self.stat_prec))     
        
        print('______________________________________________________________________________')
        print('\n')
        
    def print_report(self):
        
        print('ID {:03} | ICD {:.{prec}f} | NN {:.{prec}f} | AREA {:.{prec}f} | NEIGHBORS {:.{prec}f} | NNRI {:.{prec}f} | VDRI {:.{prec}f}'
              .format(self.id,
                      self.mean_icd_um,
                      self.mean_nn_um,
                      self.mean_cell_area_um,
                      self.mean_num_neighbors,
                      self.nnri,
                      self.vdri,
                      prec=self.stat_prec))
        
    def save(self):
        
        save_cell_data(self.nn, self.vd_areas, self.num_neighbors, self.id)
    
    def get_bound_stats(self):
        
        stats = {
            "id": self.id,
            "num_bound_cells": self.num_bound_cells,
            "total_bound_area": self.total_vd_area_um,
            "bound_density": self.bound_density,
            "mean_icd": self.mean_icd_um,
            "std_icd": self.std_icd_um,
            "mean_nn": self.mean_nn_um,
            "std_nn": self.std_nn_um,
            "mean_vd": self.mean_vd_um,
            "std_vd": self.std_vd_um,
            "mean_num_neighbors": self.mean_num_neighbors,
            "std_num_neighbors": self.std_num_neighbors,
            "nnri": self.nnri,
            "vdri": self.vdri,
            "alt_nnri": self.alt_nnri
        }
        
        return stats
    
    def get_icd(self):
        
        return self.mean_icd
        
    def get_nn(self):
        
        return self.mean_nn
        
    def get_mean_cell_area(self):
        
        return self.mean_cell_area
        
    def get_nnri(self):
        
        return self.nnri
    
    def get_alt_nnri(self):
        
        return self.alt_nnri
    
    def get_vdri(self):
        
        return self.vdri
    
    def get_points_array(self):
        
        return self.points_array
    
    def get_area(self):
        
        return self.estimated_area
    
        
        
        