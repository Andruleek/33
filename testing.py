import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import shutil
import time

def get_files_by_extension(directory):
    files_by_extension = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            files_by_extension[ext].append(os.path.join(root, file))
    return files_by_extension

def move_files(files):
    for file in files:
        filename = os.path.basename(file)
        dest_folder = os.path.join("Sorted", filename[filename.rfind(".")+1:])  
        os.makedirs(dest_folder, exist_ok=True)
        shutil.move(file, os.path.join(dest_folder, filename))

def process_folder(directory):
    files_by_extension = get_files_by_extension(directory)
    with ThreadPoolExecutor() as executor:
        for files in files_by_extension.values():
            executor.submit(move_files, files)

def factorize_sync(numbers):
    result = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    return result

def factorize_single(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = pool.map(factorize_single, numbers)
    pool.close()
    pool.join()
    return result

def factorize(*numbers):
    result = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    return result

if __name__ == "__main__":
    # Part 1: Sorting Files
    process_folder("Хлам")
    
    # Part 2: Synchronous Factorization
    numbers = [756, 1024, 583, 690, 21, 777]
    start_time_sync = time.time()
    result_sync = factorize_sync(numbers)
    end_time_sync = time.time()
    print("Sync Execution Time:", end_time_sync - start_time_sync, "seconds")
    print("Factors (Sync):", result_sync)
    
    # Part 3: Parallel Factorization
    start_time_parallel = time.time()
    result_parallel = factorize_parallel(numbers)
    end_time_parallel = time.time()
    print("Parallel Execution Time:", end_time_parallel - start_time_parallel, "seconds")
    print("Factors (Parallel):", result_parallel)
    
    # Part 4: Factorization with Variable Arguments
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
