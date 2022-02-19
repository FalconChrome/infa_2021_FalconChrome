#include <iostream>
using namespace std;

int linsearch(int arr[], int n, int x, int &cnt){
    int i=-1;
    for (i=0; i<n; i++){
        if(arr[i] == x){
            break;
        }
        cnt++;
    }
    return i;
}


int binsearch(int arr[], int n, int x, int &cnt){
    int a = 0;
    while (n > 1){
        if(x < arr[a + n / 2]){
            n /= 2;
        } else {
            a += n / 2;
            n = (n + 1) / 2;
        }
        cnt++;
    }
    if (arr[a] == x){
        return a;
    } else {
        return -1;
    }
}

void printsearch(int var, int arr[], int size, int x){
    int cnt = 0;
    int res;
    char s;
    switch(var){
        case 1:
            res = linsearch(arr, size, x, cnt);
            s = 'l';
            break;
        case 2:
            res = binsearch(arr, size, x, cnt);
            s = 'b';
            break;
    }
    cout << s << "in search: " << "res – " << res << ", n steps – " << cnt << endl;
}

int main()
{
	int arrgh[12] {0,1,2,3,4,5,6,7,8,9,10,11};
	//int arr1[6] {-7,-2,14,25,27,31};
//	int arr2[9] {2,2,2,4,4,4,4,10,10};
//	int rarr[8] {6,72,23,12,-13,8,-44,1};
	
	int x, size;
	int *arr;

	arr = arrgh;
	size = 12;
	//x = 24;

    for(int i=0; i<size; i++){cout << arr[i]<<' ';} cout << endl;   
    cin >> x;

    for (int var=1; var <= 2; var++){
        printsearch(var, arr, size, x);
    }

	return 0;
}