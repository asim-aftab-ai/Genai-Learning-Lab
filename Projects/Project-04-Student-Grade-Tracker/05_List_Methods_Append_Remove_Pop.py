# .append adds a new item at the end of the list

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
nums.append(11)
print(nums) #output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

nums.append(12)
print(nums) #output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Removes a specific value (not index)

nums.remove(5)
nums.remove(10)
nums.remove(12)

print(nums) #output: [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]


#.pop Removes item using index

nums.pop(0)  # Removes the item at index 0
nums.pop(3)  # Removes the item at index 3 (which is now 6 after the previous pop)
nums.pop()   # Removes the last item (which is 12)

print(nums) #output: [2, 3, 4, 6, 7, 8, 9, 10, 11, 12]
