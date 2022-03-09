#include <iostream>
#include <random>
#define NDEBUG
#include <cassert>

using namespace std;

random_device dev;
mt19937 rng(dev());


void print_array(int *arr, int n) {
    cout << "int Array[" << n << "]:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << arr[i] << '\t';
    }
    cout << endl;
}

void swap(int &a, int &b) {
    int t;
    t = a;
    a = b;
    b = t;
}

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


int main() {
    const auto n = 50;
    int a[n]{0};

    uniform_int_distribution<int> dist(0, n - 1);
    int j;
    for (int i = 1; i <= n; ++i) {
        do {
            j = dist(rng);
        } while (a[j] != 0);
        a[j] = i;
    }

    print_array(a, n);
    qsort(a, n);
    print_array(a, n);

    return 0;
}
