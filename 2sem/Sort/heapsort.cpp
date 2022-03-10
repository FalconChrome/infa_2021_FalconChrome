void swap(int &a, int &b);
void print_heap(int *arr, int n);

int* min(int *a, int *b){
    if (*a < *b){
        return a;
    }
    return b;
}

void heapify(int *arr, int n, int k){
    int children = n - 2 * k - 1;
    if (children <= 0){
        return; // no children for k
    }
    if (children > 2){
        heapify(arr, n, 2 * k + 1);
        heapify(arr, n, 2 * k + 2);
    }
    if(children == 1){ // k with 1 child
        if (arr[2 * k + 1] < arr[k]){
            swap(arr[2 * k + 1], arr[k]);
        }
        return;
    }
    // else k with 2 children
    int *m = min(arr + 2 * k + 1, arr + 2 * k + 2);
    if (*m < arr[k]){
        swap(*m, arr[k]);
    }
}

void heapsort(int *arr, int n) {
    for (; n > 0; --n) {
        heapify(arr, n, 0);
//        print_heap(arr, n);
        swap(arr[0], arr[n - 1]);
    }
}

