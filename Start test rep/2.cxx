#include <iostream>
using namespace std;

const char b = '<';

int main()
{
	char t;
	unsigned int n;
	int d = 0;
	cin >> n;

	for(unsigned int i=0; (i < n) and (d >= 0); i++){
	    cin >> t;
	    d += (b - t) + 1;
	    cout << d<<' ';
	}
	if(d == 0){
	    cout << "Right" << endl;}
	else {
	    cout << "Wrong" << endl;}
	return 0;
}