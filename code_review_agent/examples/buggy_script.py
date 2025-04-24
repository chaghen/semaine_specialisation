def calculate_average(numbers):
    sum = 0
    for i in range(len(numbers)):
        sum += numbers[i]
    average = sum / len(numbers)
    return average

def find_max(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

def process_data(data):
    # Process data and return result
    result = {}
    for item in data:
        key = item[0]
        value = item[1]
        result[key] = value
    return result