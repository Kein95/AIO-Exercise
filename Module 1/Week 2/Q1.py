num_list = [3, 4, 5, 1, -44, 5, 10, 12, 33, 1]
k = 3

def my_function(num_list, k): 
  result = []
  for i in range(len(num_list) - k + 1):
    max_value = max(num_list[i:i+k])
    result.append(max_value)
  return result
print(my_function(num_list, k))