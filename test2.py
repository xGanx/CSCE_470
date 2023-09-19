my_list = [
    ['Alice', 25],
    ['Bob', 30],
    ['Charlie', 20],
    ['David', 35]
]

# Sort the list based on the second value of each sublist (index 1)
sorted_list = sorted(my_list, key=lambda x: x[1])

# Print the sorted list
print(sorted_list)