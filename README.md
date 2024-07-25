<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/thomasmichaelkane/bound_cells">
    <img src="docs/images/bound_cells.gif" alt="Logo" width="200">
  </a>

<h3 align="center">bound_cells</h3>

  <p align="center">
    Modelling cell distributions that are contained by an arbitrary boundary shape
    <br />
    <a href="https://github.com/thomasmichaelkane/bound_cells"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/thomasmichaelkane/bound_cells/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/thomasmichaelkane/bound_cells/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#classes">Classes</a></li>
        <li><a href="#functions">Functions</a></li>
      </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is to allow analysis of cell distributions that have an arbitrary boundary shape. The initial inspiration was analysing the distributions of cells in mounted retina, where the cells are sparse enough that using a rectangular area would omit significant amounts of collected data.

By using this code you can estimate the border of any cell distribution by simply supplying a the coordinates of these cells, and obtain statistics from voronoi analysis, and visualise the distribution in many ways.

<img src="docs/images/clustering.png" alt="Logo" width="200">
<img src="docs/images/cells_from_clusters.png" alt="Logo" width="200">

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python.py]][Python-url]
* [![SciPy][SciPy.py]][SciPy-url]
* [![Shapely][Shapely.py]][Shapely-url]
* [![NetworkX][NetworkX.py]][NetworkX-url]
* [![Pillow][Pillow.py]][Pillow-url]
* [![Imantics][Imantics.py]][Imantics-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.


### Installation

1. Clone the repo at the desired location
   ```sh
   git clone https://github.com/thomasmichaelkane/bound_cells.git
   cd bound_cells
   ```
2. Create a virtual environment
   ```sh
   python -m venv .venv
   ```
2. Activate environment
  <small>Windows</small>
   ```sh
   .venv/Scripts/activate.ps1  
   ```
   <small>Mac/Linux</small>
   ```sh
   source .venv/bin/activate
   ```
3. Install prerequisites
   ```sh
   python -m pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Included in this project is one YAML config file and four scripts, that can be used to run the cell distribution class easily, alongside other functionality. 

## Scripts

These are example scripts that can be run on the command line to use the bound_cells class easily. These scripts rely on settings in the config.yaml file, so these should be changed first.

### run_bound_cells.py

Uses the CellDist class and settings in the config.yaml file to use most of the core functionality of this package. The functionality is listed below, and non relevant sections can be commented out. For more detail on each of these sections, look at the API documentation.

The dimensions refer to the dimensions of the original image, though you can use a large square that encompasses all coordinates if dimensions are unknown.

- creates cell distriubution object
- calulcates densities with config
- show density and contour plots
- examine density ROIS
- show undilated voronoi
- dilate the border
- console log key stats
- show dilated voronoi
- save results
- display alpha border processing steps

```sh
python run_bound_cells.py path/to/coordinates dim [dim-y] [microns_per_pixel] [rotation]
```
- *Arguments:*
  - `path/to/coordinates` (path): The path to the coordinates file (csv file).
  - `dim` (int): The first (or only) dimension - X. If no other argumented are parsed, this singular dimension will be used to make a square. (pixels)
  - `dim` (int, optional): The second dimension - Y. (pixels)
  - `microns_per_pixel` (float, optional): The scaling factor. How many microns per pixel in the original image. The default is 1.
  - `rotation` (int, optional): How many times to rotate the coordinates 90 degrees if desired. The default is no rotation.

### random_cell_dist.py

Creates a random cell distribution to visualise for comparison with real distributions.

```sh
python random_cell_dist.py [number_of_cells] [dim] [dim-y] [min_separation]
```
- *Arguments:*
  - `number_of_cells` (int, optional): The number of cells. How many cells will be distributed.
  - `dim` (int, optional): The first (or only) dimension - X. If no other argumented are parsed, this singular dimension will be used to make a square. The default
    value is 100. (pixels)
  - `dim-y` (int, optional): The second dimension - Y. The default value is 100. (pixels)
  - `minimum separation` (float, optional): The minimum separation between cells. Bare in mind this number cannot be too high, or the program will fail, as it will not be able to find new locations that are at the minimum separation. The default value is 0. (PIXELS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### random_average.py

Creates many iterations of random cell distribution and averages them to compare statistics with real distributions.

```sh
python random_average.py [number_of_iterations] [number_of_cells] [microns_per_pixel] [desnity] [min_separation]
```
- *Arguments:*
  - `number_of_iterations` (int, optional): The number of iterations to run before finding an average. The default value is 10.
  - `number_of_cells` (int, optional): The number of cells. How many cells will be distributed.
  - `microns_per_pixel` (float, optional): The scaling factor. How many microns per pixel in the original image. The default is 1.
  - `density` (float, optional): The density of the cells (per mm2). The default value is 1000.
  - `minimum separation` (float, optional): The minimum separation between cells. Bare in mind this number cannot be too high, or the program will fail, as it will not be able to find new locations that are at the minimum separation. The default value is 0. (PIXELS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### visualise_alpha.py

This script is used to visualise the effect of different alpha values when trying to estimate the border of a cell distribution. The default value of the average inter-cell distance is normally very good, but with a particularly irregular distribution this function can be used to compare the effects of different values in order to find the best one. You can iterate up and down from the command line once the script has been run.

```sh
python visualise_alpha.py path/to/coordinates dim [dim-y] [size] [alpha_count] [alpha_allowance]
```
- *Arguments:*
  - `path/to/coordinates` (path): The relative or absolute path to the coordinates file. This file should be a two column csv file containing x and y coordinates of all cell centres (in pixels).
  - `dim` (int): The first (or only) dimension - X. If no other argumented are parsed, this singular dimension will be used to make a square. (pixels)
  - `dim` (int, optional): The second dimension - Y. (pixels)
  - `alpha count` (int, optional): How many values of alpha will be trailed each time, and how many graphs will be displayed. The default is 3.
  - `alpha allowance` (float, optional): The limits of the linspace of trialled alphas. The lowest and highest alpha values that will be shown each time compared with the middle value. The default is 0.1, which will show 10% above and below the central value.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## API


### Class: CellDist

CellDist description

The class can be imported like so:

```py
from bound_cells import CellDist
```

---

#### Constructor

```py
__init__(path):
```
The class is constructed by .....

- *Parameters:*
  - `path` (str): The path 

---

#### Methods

todo

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Functions

Loading the configuration file. This will load all additional settings from the config.yaml file into a dictionary called *config*.

   ```py
   from bound_cells import load_config

   config = load_config()
   ```

todo

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Thomas Kane - thomas.kane.ucl@gmail.com

Me: https://thomasmichaelkane.github.io/me/

Project Link: [https://github.com/thomasmichaelkane/bound_cells](https://github.com/thomasmichaelkane/bound_cells)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: docs/images/screenshot.png

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/

[Python.py]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[OpenCV.py]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/

[Matplotlib.py]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
[Matplotlib-url]: https://matplotlib.org/

[scikit-learn.py]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[scikit-learn-url]: https://scikit-learn.org/stable/

[SciPy.py]: https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white
[SciPy-url]: https://scipy.org/

[NetworkX.py]: https://img.shields.io/badge/NetworkX-red?style=for-the-badge
[NetworkX-url]: https://networkx.org/

[imantics.py]: https://img.shields.io/badge/Imantics-purple?style=for-the-badge
[imantics-url]: https://imantics.org/

[pillow.py]: https://img.shields.io/badge/Pillow-orange?style=for-the-badge
[pillow-url]: https://python-pillow.org/

[shapely.py]: https://img.shields.io/badge/shapely-green?style=for-the-badge
[shapely-url]: https://pypi.org/project/shapely/

[Arduino.ino]: https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white
[Arduino-url]: https://www.arduino.cc/reference/en/