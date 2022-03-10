#define NDEBUG
#include <cassert>

void swap(int &a, int &b);

void qsort(int *arr, int n) {
    if (n < 2) {
        return;
    }
    int l = 0;
    int r = n - 1;
    int pivot = arr[0];

    do {
        while (arr[l] < pivot) {
            ++l;
        }
        while (arr[r] >= pivot and r > 0) {
            --r;
        }
        assert(l < n);
        assert(r >= 0);
        if (l < r) {
            swap(arr[l], arr[r]);
            ++l;
            --r;
        }
        assert(l < n);
        assert(r >= 0);
    } while (l < r);

    if (arr[r] <= pivot) {
        ++r;
    }

    assert(l < n);
    assert(r >= 0);
    assert(r < n);
    qsort(arr, r);
    qsort(arr + r, n - r);
}
