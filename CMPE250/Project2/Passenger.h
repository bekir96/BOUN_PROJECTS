#ifndef Passenger_H
#define Passenger_H

#include <iostream>

#include <string>

using namespace std;


class Passenger {

    public:

        int timeComesToT;

        int timeFlight;

        int timeLuggage;

        int timeSecurity;

        int procedureTime;

        string procedureType;

        bool vip;

        bool luggage;

        bool firstToFly;

        Passenger(int timeComesToT, int timeFlight, int timeLuggage, int timeSecurity, bool Vip, bool luggage, bool firstToFly);




};


#endif

