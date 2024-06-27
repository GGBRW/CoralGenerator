import time

# Number of iterations
num_iterations = 100000

# Loop with print statements
start_time_with_print = time.time()
for i in range(num_iterations):
    print(i, end='\r')  # Using end='\r' to overwrite the line in console
end_time_with_print = time.time()
duration_with_print = end_time_with_print - start_time_with_print

# Loop without print statements
start_time_without_print = time.time()
for i in range(num_iterations):
    pass  # Do nothing
end_time_without_print = time.time()
duration_without_print = end_time_without_print - start_time_without_print

# Print the results
print("\nDuration with print: {:.6f} seconds".format(duration_with_print))
print("Duration without print: {:.6f} seconds".format(duration_without_print))