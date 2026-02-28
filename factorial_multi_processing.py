import multiprocessing
import time
import sys
import time


# Increase the maximum string digits limit
sys.set_int_max_str_digits(1000000)

## Function to compute factorial
def compute_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * compute_factorial(n - 1) 
    
if __name__ == "__main__":
    numbers = [10000, 20000, 30000, 40000, 50000]
    processes = []
    t = time.time()

    ## create processes
    for number in numbers:
        p = multiprocessing.Process(target=compute_factorial, args=(number,))
        processes.append(p)
        p.start()

    ## wait for all processes to complete
    for p in processes:
        p.join()

    print("Factorial computations completed.")
    finish = time.time()
    print(f"Time taken with multiprocessing: {finish - t} seconds")

