#include "Passenger.h"
#include "Probability.h"
#include <fstream>
#include <string>
#include <queue>

struct PassengerCompare {

    bool operator() (const Passenger* p1, const Passenger* p2) const {

        if(p1->procedureTime == p2->procedureTime){

            if (p1->procedureType == p2->procedureType) {

                return p1->timeComesToT > p2->timeComesToT;

            } else {

                return p1->procedureType < p2->procedureType;

            }

        } else {

            return p1->procedureTime > p2->procedureTime;

        }
    }

};

struct PassengerCompare2 {

    bool operator() (const Passenger* p1, const Passenger* p2) const {

        if(p1->firstToFly == true  || p2->firstToFly == true){

            if(p1->timeFlight == p2->timeFlight){

                return p1->timeComesToT > p2->timeComesToT;

            } else {

                return p1->timeFlight > p2->timeFlight;

            }

        }

        else {

            if(p1->procedureTime == p2->procedureTime){

                return p1->timeComesToT > p2->timeComesToT;

            } else {

                return p1->procedureTime > p2->procedureTime;

            }

        }

    }

};

priority_queue <Passenger*, vector<Passenger*>, PassengerCompare> passenger;

priority_queue <Passenger*, vector<Passenger*>, PassengerCompare2> luggageWait;

priority_queue <Passenger*, vector<Passenger*>, PassengerCompare2> securityWait;

int main(){

    queue<Probability*> probabQueue;

    for(int control = 0; control < 8; control++){

        Probability* newProbabiliy = new Probability(control);

        probabQueue.push(newProbabiliy);

    }

    while(probabQueue.size() != 0){

        int population, luggageNo, securityNo;

        ifstream infile("/Users/bekiryildirim/Desktop/inputLarge2.txt");

        infile >> population >> luggageNo >> securityNo ;

        int timeComesToT, timeFlight, timeLuggage, timeSecurity;

        string vip, luggage;

        int luggageCount = 0;

        int securityCount = 0;

        float waitingTime = 0;

        int missPlaneCount = 0;

        Probability* controlProbab = probabQueue.front();

        bool controlVip = false;

        bool controlLuggage = false;

        bool controlFirstToFly = controlProbab->firstToFly;

        for(int i = 0 ; i < population ; i++){

            infile >> timeComesToT >> timeFlight >> timeLuggage >> timeSecurity >> vip >> luggage;

            if(controlProbab->noSecurityVip == true && !vip.compare("V")) {

              controlVip = true;

            }

            if(controlProbab->usingOnline == true && !luggage.compare("N")){

            controlLuggage = true;

            }

            Passenger* newPassenger = new Passenger(timeComesToT, timeFlight, timeLuggage, timeSecurity, controlVip, controlLuggage, controlFirstToFly);

            passenger.push(newPassenger);

            controlVip = false;

            controlLuggage = false;

        }

        while(passenger.size() != 0 ){

            Passenger* passengerChange = passenger.top();

            passenger.pop();

            if(!passengerChange->procedureType.compare("E")){

                if(passengerChange->luggage == true){

                    passengerChange->procedureTime += passengerChange->timeLuggage;

                    passengerChange->procedureType = "L";

                    passenger.push(passengerChange);

                    luggageCount++;

                } else {

                    if(luggageCount < luggageNo){

                        passengerChange->procedureTime += passengerChange->timeLuggage;

                        passengerChange->procedureType = "L";

                        passenger.push(passengerChange);

                        luggageCount++;

                    } else {

                        luggageWait.push(passengerChange);

                    }

                }

            }

            else if(!passengerChange->procedureType.compare("L")){

                luggageCount--;

                int tempTime = passengerChange->procedureTime;

                if(passengerChange->vip != true){

                    if(securityCount < securityNo){

                        passengerChange->procedureTime += passengerChange->timeSecurity;

                        passengerChange->procedureType = "S";

                        passenger.push(passengerChange);

                        securityCount++;

                    } else {

                        securityWait.push(passengerChange);

                    }

                } else {

                    waitingTime+= tempTime - passengerChange->timeComesToT;

                    if(tempTime > passengerChange->timeFlight) {

                        missPlaneCount++;

                    }

                }

                while(luggageWait.size() > 0 && luggageCount < luggageNo){

                    Passenger* deleteWaitL = luggageWait.top();

                    luggageWait.pop();

                    deleteWaitL->procedureTime = tempTime + deleteWaitL->timeLuggage;

                    deleteWaitL->procedureType = "L";

                    passenger.push(deleteWaitL);

                    luggageCount++;

                }

            }

            else if(!passengerChange->procedureType.compare("S")){

                securityCount--;

                int tempTimeSecurity = passengerChange->procedureTime;

                if(tempTimeSecurity > passengerChange->timeFlight){

                    missPlaneCount++;

                }

                waitingTime += tempTimeSecurity - passengerChange->timeComesToT;

                while(securityWait.size() > 0 && securityCount < securityNo){

                    Passenger* deleteWaitS = securityWait.top();

                    securityWait.pop();

                    deleteWaitS->procedureTime = tempTimeSecurity + deleteWaitS->timeSecurity;

                    deleteWaitS->procedureType = "S";

                    passenger.push(deleteWaitS);

                    securityCount++;

                }

            }

        }

        float averageWaiting = waitingTime / population;

        cout << averageWaiting << " " << missPlaneCount << endl;

        probabQueue.pop();

    }

}
