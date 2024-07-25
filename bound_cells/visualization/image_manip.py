"""
This module provides functions for image processing, including conversion between polygons and masks, dilation of masks, and extraction of polygons from masks.

Module Functions:
- polygon_to_mask(polygon, dim, style="fill", show=True): Converts a polygon to a binary mask.
- dilate_mask(mask, strength, show=True): Dilates a binary mask.
- mask_to_polygon(mask): Extracts a polygon from a binary mask.
"""
import cv2
import numpy as np
from scipy.ndimage.morphology import binary_dilation
from PIL import Image, ImageDraw, ImageOps
from imantics import Mask

from ..cells import geometry
from ..visualization import display

def density_map(densities, rescale):
    
    (x, y, z) = densities
    density_scaling = (1/z.max())
    
    dmap = (z*density_scaling).reshape(x.shape)
    dmap_scaled = cv2.resize(dmap, (0,0), fx=rescale, fy=rescale)

    return dmap, dmap_scaled

def user_density_roi(dmap_scaled, dim, scale, name):
    
    density_roi = geometry.user_polygon(dmap_scaled, name=name)
    scaled_roi = [(x*1/scale, dim-y*1/scale) for (x, y) in density_roi]
    return scaled_roi

# def get_density_rois(densities, rescale=1):

#     (x, y, zi) = densities
#     dim = (len(x), len(y))
#     zmax = zi.max()
#     colour_scaling = (1/zmax)
    
#     z_small = (zi*colour_scaling).reshape(x.shape)
#     z = cv2.resize(z_small, (0,0), fx=rescale, fy=rescale)
    
#     num_rois = 2
#     polygons = []
#     img = z.copy()
    
#     for _ in range(num_rois):
        
#         polygons.append(get_density_roi(img, dim, rescale))
    
def show_density_rois(densities, density_rois, dmap, dim):
    
    (x, y, z) = densities
    masks = []
    density_pops = {}
    colours = [[255, 128, 0], [255, 0, 255]]
    
    overlay = cv2.cvtColor((dmap.copy()*255).astype("uint8"), cv2.COLOR_GRAY2RGB)
        
    for i, (key, roi) in enumerate(density_rois.items()):

        mask, mask_img = polygon_to_mask(roi, (dim, dim))
        density_map = np.multiply(mask/255, z.reshape(x.shape))
        
        bool_mask = mask > 0

        densities = [d for d in density_map.flatten() if d != 0]
        display.histogram_list(densities, "densities", bins=30)
        
        masks.append(bool_mask)
        density_pops.update({key: densities})
        overlay = mask_color_img(overlay, bool_mask, color=colours[i])
    
    overlay_img = Image.fromarray(overlay)
    overlay_img.show()
    
    return density_pops, overlay_img
        
        
def mask_color_img(img, mask, color=[255, 255, 0], alpha=0.3):
    '''
    img: cv2 image
    mask: bool or np.where
    color: BGR triplet [_, _, _]. Default: [0, 255, 255] is yellow.
    alpha: float [0, 1]. 

    Ref: http://www.pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/
    '''
    out = img.copy()
    img_layer = img.copy()
    print(img_layer)
    img_layer[mask] = color
    out = cv2.addWeighted(img_layer, alpha, out, 1 - alpha, 0, out)
    return(out)

def polygon_to_mask(polygon, dim, style="fill", show=False):
    """
    Converts a polygon to a binary mask.

    Parameters:
    - polygon (list): List of (x, y) coordinates representing the polygon.
    - dim (tuple): Dimensions (width, height) of the output mask.
    - style (str): Style of the mask ("fill" for filled, "outline" for outlined).
    - show (bool): If True, displays the generated mask.

    Returns:
    - tuple: Binary mask as a NumPy array and corresponding PIL Image.

    Raises:
    - None
    """
    if style == "fill":
        outline, fill = None, 255
    elif style == "outline":
        outline, fill = 255, None

    img = Image.new('L', (dim[0], dim[1]), color=0)
    ImageDraw.Draw(img).polygon(polygon, outline=outline, fill=fill)
    img = ImageOps.flip(img)
    mask = np.array(img)

    if show:
        img.show()

    return mask, img

def dilate_mask(mask, strength, show=True):
    """
    Dilates a binary mask.

    Parameters:
    - mask (np.array): Binary mask as a NumPy array.
    - strength (float): Strength of dilation.
    - show (bool): If True, displays the dilated mask.

    Returns:
    - tuple: Dilated mask as a NumPy array and corresponding PIL Image.

    Raises:
    - None
    """
    strength = int(round(strength))
    strel = np.ones((strength, strength))
    dilated = binary_dilation(mask, structure=strel)
    img = Image.fromarray(dilated)

    if show:
        img.show()

    return dilated, img

def mask_to_polygon(mask):
    """
    Extracts a polygon from a binary mask.

    Parameters:
    - mask (np.array): Binary mask as a NumPy array.

    Returns:
    - list: List of (x, y) coordinates representing the extracted polygon.

    Raises:
    - None
    """
    mask = np.flip(mask, 0)
    polygons = Mask(mask).polygons()

    polygon_lengths = [len(poly) for poly in polygons.points]
    max_val = max(polygon_lengths)
    i = polygon_lengths.index(max_val)

    new_poly = polygons.points[i]

    return new_poly
