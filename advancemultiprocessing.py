## Multiprocessing with Pool

from concurrent.futures import ProcessPoolExecutor
import time

def square(n):
        time.sleep(2)
        return n*n

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if __name__ == "__main__":
            
    with ProcessPoolExecutor(max_workers=4) as executor:
            results = executor.map(square, numbers)

    for result in results:
            print(result)