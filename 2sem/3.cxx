#include <iostream>
using namespace std;

void reverse(int &x){
    int r = 0;
    while(x != 0){
        r = 10 * r + x % 10;
        x /= 10;
    }
    x = r;
}

int main()
{
	int x;
	cin >> x;
	reverse(x);
	cout << x << endl;
	return 0;
}