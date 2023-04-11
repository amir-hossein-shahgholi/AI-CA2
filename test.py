import random

numbers = [100,1,1,1,1,0]


total = sum(numbers)
print(numbers)
numbers = [x/total for x in numbers]
numbers.append(1 - sum(numbers))
print(numbers)
