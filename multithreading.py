## Multithreading example
import threading
import time

def printnumbers():
    for i in range(1, 6):
        time.sleep(2)
        print(f"Number: {i}")

def printletters():
    for letter in "abcde":
        time.sleep(2)
        print(f"Letter: {letter}")  

## create threads
t1 = threading.Thread(target=printnumbers)  
t2 = threading.Thread(target=printletters)


t = time.time()

##start threads
t1.start()
t2.start()


## wait for both threads to complete
t1.join()
t2.join()


printnumbers()
printletters()
finish = time.time()-t
print(f"Time taken without threading: {finish} seconds")    