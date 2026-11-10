# Find the largest and smallest list values

def largest_smallest(arr):
  if  len(arr) <= 1:
    return None, None 
  
  large,small = float("-inf"),float("inf")
  for num in arr:
    if num > large:
      large = num
    elif num < small:
      small = num

  return large,small
arr =  [3, 5, 1, 8, 2]
print(largest_smallest(arr))



# Find the second-largest distinct number without sorting the complete list.
def second_largest(arr):
    if len(arr) < 2:
        return None  

    first = second = float("-inf")
    for num in arr:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num

    return second
arr = [3, 5, 1, 8, 2]
result = second_largest(arr)
print(result)



# Remove duplicates while preserving order

def remove_duplicates(arr):
   if len(arr) <= 0:
      return ''
   result = []
   for  i in arr:
    if i not in result:
        result.append(i)
   return result
arr = [3, 5, 1, 8, 2]
result = remove_duplicates(arr)
print(result)



# Separate even and odd numbers.

def separate_even_odd(arr):
    even_numbers = []
    odd_numbers = []

    for num in arr:
        if num % 2 == 0:
            even_numbers.append(num)
        else:
            odd_numbers.append(num)

    return even_numbers, odd_numbers

arr = [3, 5, 1, 8, 2]
even, odd = separate_even_odd(arr)
print("Even numbers:", even)
print("Odd numbers:", odd)



# • Find common values between two lists.

def common_value(arr1, arr2):
    # Handle empty lists
    if not arr1 or not arr2:
        return "Error: Lists cannot be empty."

    common_val = []
    for i in arr1:
        if i in arr2 and i not in common_val:
            common_val.append(i)
    return common_val
  
# Input lists
arr1 = [1, 2,3, 4, 5, 6, 7]
arr2 = [5, 6, 7, 3, 2, 8, 9]

result = common_value(arr1, arr2)
print(result)



# Count frequency of each number
def count_frequency(arr):
    # Handle empty list
    if not arr:
        return "Error: List cannot be empty."

    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1

    return frequency

arr = [1, 2, 3, 2, 1, 4, 5, 3, 2]
result = count_frequency(arr)
print(result)



# 7 . Create a marks dictionary and find the highest scorer, lowest scorer and average
def marks_analysis(marks_dict):
    # Handle empty dictionary
    if not marks_dict:
        return "Error: Marks dictionary cannot be empty."

    highest_scorer = max(marks_dict, key=marks_dict.get)
    lowest_scorer = min(marks_dict, key=marks_dict.get)
    average_score = sum(marks_dict.values()) / len(marks_dict)

    return highest_scorer, lowest_scorer, average_score

# Example usage
marks = {"Arjit": 85, "ram": 92, "shyam": 78, "Diya": 96}

highest, lowest, average = marks_analysis(marks)
print(f"Highest scorer: {highest}")
print(f"Lowest scorer: {lowest}")
print(f"Average score: {average}")