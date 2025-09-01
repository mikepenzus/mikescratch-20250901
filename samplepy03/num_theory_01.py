import numpy
import numpy as np
import math
import time
import sys


def triang(n):
    return n*(n+1) // 2


def factorial(n):
    if n < 1:
        return 1
    current_product = 1
    for i in range(2, n+1):
        current_product *= i
    return current_product


def binomial(n, k):
    return factorial(n) // (factorial(n - k) * factorial(k))


how_many_numbers = 10

first_numbers = [x+1 for x in range(how_many_numbers)]
squares = [x*x for x in first_numbers]
print("Squares", squares)

cubes = [x*x*x for x in first_numbers]
print("Cubes", cubes)

triang_numbers = [triang(x) for x in first_numbers]
print("Triangular numbers", triang_numbers)

fibonacci_numbers = np.ones(how_many_numbers, dtype=numpy.int64)
for index in range(2, how_many_numbers):
    fibonacci_numbers[index] = fibonacci_numbers[index-1] + fibonacci_numbers[index-2]
print("Fibonacci numbers", fibonacci_numbers)

factorials = [factorial(x) for x in first_numbers]
print("Factorials", factorials)

print("Pascal triangle:")
for n in range(how_many_numbers+1):
    current_line = [binomial(n, k) for k in range(n+1)]
    print(current_line)


start_number = 80
results = [start_number]
max_no_results = 20
current_number = start_number
for n in range(max_no_results-1):
    if current_number % 2 == 0:
        current_number = current_number // 2
    else:
        current_number = current_number*3+1
    results.append(current_number)
print("Collatz conjecture from", start_number, results)

sys.set_int_max_str_digits(100000)
start_time = time.time()
print("math.factorial", math.factorial(6000))
end_time = time.time()
print("time", end_time - start_time)

start_time = time.time()
print("my factorial  ", factorial(6000))
end_time = time.time()
print("time", end_time - start_time)

