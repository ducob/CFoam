//
//
//  golden_mean_stability
//
//  Created by Duco Bouter on 03-02-15.
//  Copyright (c) 2015 Duco Bouter. All rights reserved.
//

#include <iostream>
#include <cmath>

using namespace std;


//Direct PHI calculation
float single_direct_phi(int n){

    float phi = (sqrt(5.) - 1.)/2.;
    return pow(phi, n);
}

//Recursive PHI calculation
float single_rec_phi(int n){

    float phi = (sqrt(5.) - 1.)/2.;
    float phi_n;
    float first = pow(phi,1);
    float second = pow(phi,2);

    if (n==1 || n==2){
        phi_n = pow(phi, n);
    }
    else{
        for (int i=0; i<(n-2); i++) {
            phi_n = first - second;
            first = second;
            second = phi_n;
        }
    }

    return phi_n;
}


int main() {

    float error = 0;
    int n = 1;



    while (error <= 0.001){
        error = abs((single_direct_phi(n) - single_rec_phi(n)));

        cout << "Power= " << n << " Error=" << error << endl;
        n++;
    }

    return 0;
}
