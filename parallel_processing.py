## Process that runs in parallel
import multiprocessing
import time

def square_numbers():
    for i in range(1, 6):
        time.sleep(1)
        print(f"Square: {i*i}")

def cube_numbers():
    for i in range(1, 6):
        time.sleep(1)
        print(f"Cube: {i*i*i}")

if __name__ == "__main__":
    t = time.time()

    ## create processes
    p1 = multiprocessing.Process(target=square_numbers)
    p2 = multiprocessing.Process(target=cube_numbers)

    ## start the processes
    p1.start()
    p2.start()
    
    ## wait for both processes to complete
    p1.join()
    p2.join()

    print("Both processes completed.")
    finish = time.time()
    print(f"Time taken with multiprocessing: {finish - t} seconds") 