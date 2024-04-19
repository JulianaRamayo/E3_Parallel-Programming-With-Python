import math
from multiprocessing import Pool

def compute_pi(N):
    """
    Approximates the value of pi using numerical integration via the method of Riemann sums.

    Parameters:
    N (int): The number of intervals (rectangles) to use in the approximation. A higher value
             improves the accuracy of the approximation.

    Returns:
    float: An approximation of pi.
    """
    
    # Calculate the width of each rectangle (delta_x) based on the number of intervals (N)
    delta_x = 1 / N
    
    # Define the function that represents the upper boundary of the quarter circle.
    # f(x) = sqrt(1 - x^2) where x is in the interval [0, 1]
    def f(x):
        return math.sqrt(1 - x**2)

    # Initialize the sum of the areas of the rectangles
    area_sum = 0
    
    # Iterate over each interval, calculate the x coordinate of the left side of the rectangle,
    # compute the rectangle's area using the function f(x) evaluated at x_i, and add to the total area
    for i in range(N):
        x_i = i * delta_x  # x coordinate of the left side of the rectangle
        area_sum += f(x_i) * delta_x  # Add the area of the rectangle to the total sum

    # Multiply the total area of the quarter circle by 4 to approximate the area of the full circle,
    # which gives an approximation of pi
    pi_approx = 4 * area_sum
    
    return pi_approx

def f(x):
    """
    Represents the upper boundary of the quarter circle.
    f(x) = sqrt(1 - x^2) where x is in the interval [0, 1]
    """
    return math.sqrt(1 - x**2)

def compute_partial_area(args):
    """
    Computes the area of rectangles for a given range of x values.
    """
    start, end, delta_x = args
    partial_sum = 0
    for i in range(start, end):
        x_i = i * delta_x
        partial_sum += f(x_i) * delta_x
    return partial_sum

def compute_pi_parallel(N, num_processes=4):
    """
    Approximates the value of pi using numerical integration via the method of Riemann sums,
    utilizing multiple processes to parallelize the computation.

    Parameters:
    N (int): The number of intervals (rectangles) to use in the approximation.
    num_processes (int): The number of parallel processes to use.

    Returns:
    float: An approximation of pi.
    """
    delta_x = 1 / N
    # Create a pool of processes
    with Pool(num_processes) as pool:
        # Divide the task among the processes
        ranges = [(i * (N // num_processes), (i + 1) * (N // num_processes), delta_x) for i in range(num_processes)]
        # Collect the results from all processes
        results = pool.map(compute_partial_area, ranges)
        total_area = sum(results)
    # Multiply the total area of the quarter circle by 4 to approximate the full circle's area
    pi_approx = 4 * total_area
    return pi_approx