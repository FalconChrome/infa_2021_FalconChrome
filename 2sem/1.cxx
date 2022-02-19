#include <iostream>
using namespace std;


bool prime(unsigned int x){
    bool res = true;
    if(x <= 1) 
        res = false;
    if(x == 2)
        res = true; 
    else
        if(x % 2 == 0)
            res = false;
        else {
            for(int t = 3; t * t <= x; t += 2){
                if (x % t == 0){
                    res = false;
                    break;
                }
            }
        }
    return res;
}


unsigned int reversed(unsigned int x){
    unsigned int r = 0;
    while(x > 0){
        r = 10 * r + x % 10;
        x /= 10;
    }
    return r;
}

bool palindrom(unsigned int x){
    return x == reversed(x);
}


int main()
{
	unsigned int n, t;
	cin >> n;
    	for(int i=0; i<n; i++){
	    cin >> t;
	    cout << "– " << (prime(t)? "" : "не") << "простое, "
	         << (palindrom(t)? "" : "не") << "палиндром" << endl;
	}
	return 0;
}