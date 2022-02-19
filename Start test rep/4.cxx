#include <iostream>
using namespace std;


void printtimes(char c, int n){
    for(int i=0; i<n; i++){
        cout << c;
    }
}

void printsucc(char c, int n){
    char stop = c + n;
    for(; c < stop; ++c){
        cout << c;
    }
}

void printback(char c, int n){
    char stop = c - n;
    for(; c > stop; --c){
        cout << c;
    }
}

void printrow(int n, int k){
    printsucc('A', k);
    printtimes(' ', 2 * (n - k) - 1);
    printback('A' + k - 1, k);
}


int main()
{
	int n;
	cin >> n;

	printsucc('A', n);
    printback('A' + n - 2, n - 1);

	for(int i=n-1; i>0; i--){
	    cout << endl;
	    printrow(n, i);
	}
	return 0;
}