"""
This module provides functions for parsing various input arguments.

Module Functions:
- iter(arg): Validates and returns the number of iterations.
- num_seeds(arg): Validates and returns the number of seeds (points to plot).
- mpp(arg): Validates and returns the microns per pixel (mpp) value.
- density(arg): Validates and returns the density value.
- dim(arg): Validates and returns the dimension value.
- file_name(arg): Validates and returns the file name, ensuring it is a valid CSV file.
- min_sep(arg): Validates and returns the minimum separation value.
- alpha_count(arg): Validates and returns the alpha count, ensuring it is an odd number and not too high.
- alpha_allowance(arg): Validates and returns the alpha allowance, ensuring it is between 0 and 1.
- alpha_input(alphas): Handles user input for alpha values, providing options to confirm or choose new values.
"""

def iter(arg):
    
    try:
        
        num_iter = int(arg)
        
        if num_iter < 1:
            
            raise ValueError("Please enter at least 1 iteration")
        
        return num_iter
        
    except TypeError as e:
        
        print(e)

def num_seeds(arg):
    
    try:
        
        num_seeds = int(arg)
        
        if num_seeds < 10:
            
            raise ValueError("Please enter more than 10 points to plot")
        
        return num_seeds
        
    except TypeError as e:
        
        print(e)

def rotate(arg):
    
    try:
        
        rotate = int(arg)
        
        if rotate < 0:
            
            raise ValueError("Num rotations must be positive")  
        
        return rotate
        
    except TypeError as e:
        
        print(e)

def mpp(arg):
    
    try:
        
        mpp = float(arg)
        
        return mpp
        
    except TypeError as e:
        
        print(e)
    
def density(arg):
    
    try:
        
        density = float(arg)
        
        return density
    
    except TypeError as e:
        
        print(e)
 
def dim(arg):
    
    try:
        
        dim = int(arg)
        
        return dim
        
    except TypeError as e:
        
        print(e)

def mpp(arg):
    
    
    try:
    
        mpp = float(arg)
        
        return mpp
    
    except TypeError as e:
    
        print(e)

def file_name(arg):
    
    if arg.endswith(".csv"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be a csv file")

def min_sep(arg):
    
    try:
    
        min_sep = float(arg)
        
        return min_sep
    
    except TypeError as e:
    
        print(e)

def alpha_count(arg):
    
    try:
        
        count = int(arg)
        
        if count % 2 == 0: raise KeyError("Alpha count should be an odd number")
        
        if count > 9: raise KeyError("Alpha count too high")
        
        return count
        
    except TypeError as e:
        
        print(e)
       
def alpha_allowance(arg):
    
    try:
        
        allowance = float(arg)
        
        if (allowance <= 0) or (allowance > 1): raise KeyError("Allowance should be between 0 and 1")
        
        return allowance
        
    except TypeError as e:
        
        print(e)
        
def alpha_input(alphas):
    
    cmd = input("Please confirm alpha value by typing 0, 1, or 2, or type D or U to see new alpha values [U, D, 0, 1, 2]: ")
    
    if cmd == "U":
        trial_alpha = alphas[2]
        alpha = None
    elif cmd == "D":
        trial_alpha = alphas[0]
        alpha = None
    elif cmd in ["0", "1", "2"]:
        trial_alpha = None
        alpha = alphas[int(cmd)]
    else:
        print("Invalid response.. please try again [U, D, 0, 1, 2]: ")
            
    return alpha, trial_alpha