#include "Probability.h"

Probability::Probability(int x) {

    if(x == 0){

        this->firstToFly = false;

        this->noSecurityVip = false;

        this->usingOnline = false;

    }

    if(x == 1){

        this->firstToFly = true;

        this->noSecurityVip = false;

        this->usingOnline = false;

    }

    if(x == 2){

        this->firstToFly = false;

        this->noSecurityVip = true;

        this->usingOnline = false;

    }

    if(x == 3){

        this->firstToFly = true;

        this->noSecurityVip = true;

        this->usingOnline = false;

    }

    if(x == 4){

        this->firstToFly = false;

        this->noSecurityVip = false;

        this->usingOnline = true;

    }

    if(x == 5){

        this->firstToFly = true;

        this->noSecurityVip = false;

        this->usingOnline = true;

    }

    if(x == 6){

        this->firstToFly = false;

        this->noSecurityVip = true;

        this->usingOnline = true;

    }

    if(x == 7){

        this->firstToFly = true;

        this->noSecurityVip = true;

        this->usingOnline = true;

    }

}