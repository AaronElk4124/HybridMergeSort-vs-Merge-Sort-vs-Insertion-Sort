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


#Using my solution for the hybrid merge sort from when I took CSE 331
def hybrid_merge_sort(arr, threshold: int = 40):
    """
    Performs an insertion sort on a list when the length of the list is less than the threshold and if it's greater
    than the threshold, performs a selection sort on the list.

    :param threshold: K value to start using Insertion Sort
    :param arr: list of data to be sorted
    :return: None
    """
    data_len = len(arr)
    if data_len > threshold:
        if data_len < 2:
            return
        mid = data_len // 2
        left_list = arr[:mid]
        right_list = arr[mid:]
        hybrid_merge_sort(left_list)
        hybrid_merge_sort(right_list)
        i = j = 0
        while i + j < len(arr):
            if j == len(right_list) or (i < len(left_list) and left_list[i] < right_list[j]):
                arr[i + j] = left_list[i]
                i += 1
            else:
                arr[i + j] = right_list[j]
                j += 1
    else:
        insertionSort(arr)

def measure_time(sort_function, arr, merge=False, k=0, hybrid=False):
    start_time = timeit.default_timer()
    for i in range(100):
        if merge:
            sort_function(arr.copy(), 0, len(arr) - 1)
        elif hybrid:
            sort_function(arr.copy(), k)
        else:
            sort_function(arr.copy())
    return (timeit.default_timer() - start_time) / 100


def main():
    results = []
    input_sizes = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115,
                   120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215,
                   220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315,
                   320, 325, 330, 335, 340, 345, 350]
    for size in input_sizes:
        arr = [random.randint(0, 100000) for _ in range(size)]

        insertion_time = measure_time(insertionSort, arr)
        merge_time = measure_time(mergeSort, arr, merge=True)

        for k in range(0, 110, 10):
            hybrid_merge_time = measure_time(hybrid_merge_sort, arr, k=k, hybrid=True)

            results.append({
                "Input Size": size,
                "k": k,
                "Hybrid Merge Sort Time": hybrid_merge_time,
                "Merge Sort Time": merge_time,
                "Insertion Sort Time": insertion_time
            })

    df = pd.DataFrame(results)
    df.to_csv("hybrid_merge_sort_comparison.csv", index=False)

    for k in range(0, 110, 10):
        subset = df[df["k"] == k]

        plt.figure(figsize=(10, 6))
        plt.plot(subset["Input Size"], subset["Hybrid Merge Sort Time"], label=f"Hybrid Merge Sort Time (k={k})",
                 marker="o")

        plt.plot(subset["Input Size"], subset["Merge Sort Time"], label="Merge Sort Time", marker="x", linestyle="--")
        plt.plot(subset["Input Size"], subset["Insertion Sort Time"], label="Insertion Sort Time", marker="x",
                 linestyle="--")

        plt.xlabel("Input Size (n)")
        plt.ylabel("Time (seconds)")
        plt.title(f"Comparison of Hybrid Merge Sort (k={k}), Merge Sort, and Insertion Sort Times")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"hybrid_merge_sort_comparison_k{k}.png")
        plt.show()


if __name__ == '__main__':
    main()
