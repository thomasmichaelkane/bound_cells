from enum import Enum

class PointType(Enum):
    """
    Enumeration of point types.

    Enum Values:
    - NONE (int): No point shown (1).
    - INDEX (int): Index of the cell is shown (2).
    - NEIGHBORS (int): Number of neighbors is shown (3).
    - POINT (int): Matlab point style is shown (4).
    """

    NONE = 1
    INDEX = 2
    NEIGHBORS = 3
    POINT = 4
