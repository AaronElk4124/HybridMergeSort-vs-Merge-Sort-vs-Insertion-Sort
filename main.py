import time
import random
import timeit

import pandas as pd
from matplotlib import pyplot as plt

# Implementation used from: https://www.geeksforgeeks.org/python-program-for-merge-sort/
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# l is for left index and r is right index of the
# sub-array of arr to be sorted


def mergeSort(arr, l, r):
    if l < r:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l + (r - l) // 2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


# Implementation used from: https://www.geeksforgeeks.org/python-program-for-insertion-sort/
def insertionSort(arr):
    n = len(arr)  # Get the length of the array

    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[i]  # Store the current element as the key to be inserted in the right position
        j = i - 1
        while j >= 0 and key < arr[j]:  # Move elements greater than key one position ahead
            arr[j + 1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j + 1] = key  # Insert the key in the correct position


def measure_time(sort_function, arr, merge=False):
    start_time = timeit.default_timer()
    for i in range(100):
        if merge:
            sort_function(arr.copy(), 0, len(arr) - 1)
        else:
            sort_function(arr.copy())
    return (timeit.default_timer() - start_time) / 100


def main():
    results = []
    input_sizes = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120,
                   125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220,
                   225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320,
                   325, 330, 335, 340, 345, 350]

    for size in input_sizes:
        arr = []
        for i in range(size):
            arr.append(random.randint(0, 100000))

        insertion_time = measure_time(insertionSort, arr)

        merge_time = measure_time(mergeSort, arr, merge=True)

        results.append({"Input Size": size, "Insertion Sort Time": round(insertion_time, 10), "Merge Sort Time": round(merge_time, 10)})

    df = pd.DataFrame(results)
    df.to_csv("sort_times.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(df["Input Size"], df["Insertion Sort Time"], label="Insertion Sort Time", marker="o")
    plt.plot(df["Input Size"], df["Merge Sort Time"], label="Merge Sort Time", marker="o")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Comparison of Insertion Sort and Merge Sort Times")
    plt.legend()
    plt.grid(True)
    plt.savefig("sort_comparison_plot.png")

    plt.show()

if __name__ == '__main__':
    main()

