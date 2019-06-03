#include "Passenger.h"

Passenger::Passenger(int timeComesToT, int timeFlight, int timeLuggage, int timeSecurity, bool vip, bool luggage, bool firstToFly) {

    this->vip = vip;

    this->luggage = luggage;

    this->timeComesToT = timeComesToT;

    this->timeFlight = timeFlight;

    if(luggage == true){

        this->timeLuggage = 0;

    } else {

        this->timeLuggage = timeLuggage;

    }

    if(vip == true){

        this->timeSecurity = 0;

    } else {

        this->timeSecurity = timeSecurity;

    }

    this->procedureTime = this->timeComesToT;

    this->procedureType = "E";

    this->firstToFly = firstToFly;

}