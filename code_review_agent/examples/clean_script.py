from typing import List, Dict, Tuple

def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to average
        
    Returns:
        The arithmetic mean of the numbers
        
    Raises:
        ValueError: If numbers list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    return sum(numbers) / len(numbers)

def find_max(numbers: List[float]) -> float:
    """Find the maximum value in a list of numbers.
    
    Args:
        numbers: List of numbers to search
        
    Returns:
        The maximum value found
    """
    if not numbers:
        raise ValueError("Cannot find max of empty list")
    
    max_num = numbers[0]
    for num in numbers[1:]:
        if num > max_num:
            max_num = num
    return max_num

def process_data(data: List[Tuple[str, int]]) -> Dict[str, int]:
    """Process a list of key-value pairs into a dictionary.
    
    Args:
        data: List of (key, value) tuples
        
    Returns:
        Dictionary constructed from the input data
    """
    return dict(data)