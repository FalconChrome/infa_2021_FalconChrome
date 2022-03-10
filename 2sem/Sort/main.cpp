#include <iostream>
#include <random>

void qsort(int *arr, int n);
void heapsort(int *arr, int n);
void heapify(int *arr, int n, int k);


void print_array(int *arr, int n) {
    std::cout << "int Array[" << n << "]:" << std::endl;
    for (int i = 0; i < n; ++i) {
        std::cout << arr[i] << '\t';
    }
    std::cout << std::endl;
}

void print_heap(int *arr, int n) {
    std::cout << "Heap(int Array[" << n << "]):" << std::endl;
    std::cout << arr[0] << std::endl;
    int log2k = 0, k = 4;
    while(k < n){
        k <<= 1;
        ++log2k;
    }
    for (int k = 2; k < n; k *= 2){
        for (int j = k - 1; (j < 2 * k - 1) and (j < n); ++j) {
            std::cout << arr[j];
            for (int i = 0; i < (1 << log2k); ++i) {
                std::cout << '\t';
            }
        }
        std::cout << std::endl;
        --log2k;
    }
}

void swap(int &a, int &b) {
    int t;
    t = a;
    a = b;
    b = t;
}

void gen_rand_arr(int *arr, int n, std::mt19937 rng){
    std::uniform_int_distribution<int> dist(0, 99);
    for (int i = 1; i <= n; ++i) {
        arr[i] = dist(rng);
    }
}


int main() {
    const auto n = 14;
    int a[n]{0};
    int log2n = 0, k = 1;
    while(k < n){
        k <<= 1;
        ++log2n;
    }


    std::random_device dev;
    std::mt19937 rng(dev());

    gen_rand_arr(a, n, rng);
    std::cout << "Quick sort:" << std::endl;
    print_array(a, n);
    qsort(a, n);
    print_array(a, n);

    gen_rand_arr(a, n, rng);
    std::cout << "\nHeap sort:" << std::endl;
    print_heap(a, n);
    print_array(a, n);
    heapsort(a, n);
    print_array(a, n);

    return 0;
}