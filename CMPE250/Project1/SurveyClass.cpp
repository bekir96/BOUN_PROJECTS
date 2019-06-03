#include "SurveyClass.h"

//empty constructor
SurveyClass::SurveyClass(){

    this->members = new LinkedList();

}

//copy constructor
SurveyClass::SurveyClass(const SurveyClass &other){

    this->members = new LinkedList(*other.members);

}

//copy overload assignment
SurveyClass& SurveyClass::operator=(const SurveyClass& list){

    delete this->members;

    if(list.members->head != nullptr){


        this->members = new LinkedList(*list.members);
    }


    return *this;

}

//move constructor
SurveyClass::SurveyClass(SurveyClass&& other){


    if(other.members->head != nullptr){

        this->members = move(other.members);
    }

    this->members->length = other.members->length;

    other.members->length = 0;

    other.members = nullptr;







}

//move overload assignment
SurveyClass& SurveyClass::operator=(SurveyClass&& list){

    delete this->members;

    if(list.members->head != nullptr){

        this->members = move(list.members);
    }

    this->members->length = list.members->length;

    list.members->length = 0;

    list.members = nullptr;

    return *this;

}


void SurveyClass::handleNewRecord(string _name, float _amount){

    Node* temp = this->members->head;

    //In order to select function in linkedlist, control checks name will add.
    bool control = true;

    while(temp != nullptr){
        if(!temp->name.compare(_name)){

            control = false;

        }

        temp = temp->next;

    }

    if(control){

        this->members->pushTail(_name, _amount);


    } else {

        this->members->updateNode(_name, _amount);
    }



}

//Destructor
SurveyClass::~SurveyClass(){
    if(this->members != nullptr){
        delete this->members;

    }

}

float SurveyClass::calculateMinimumExpense(){

    Node* temp = this->members->head;

    //min is minimum amount of all elements in survey class.
    float min = temp->amount ;

    while(temp != nullptr){

        if(min >  temp->amount){

            min = temp->amount;
        }

        temp = temp->next;

    }

    min = (int) (min * 100) / 100.0;

    return min;


}

float SurveyClass::calculateAverageExpense(){

    //sum is the sum of the amoount of all elements.
    float sum = 0;

    Node* temp;

    temp = this->members->head;

    while(temp != nullptr){

        sum = sum + temp->amount;
        temp = temp->next;

    }

    float avrExp = sum / this->members->length;

    avrExp = (int) (avrExp * 100 ) / 100.0 ;

    return avrExp;

}

float SurveyClass::calculateMaximumExpense(){

    Node* temp = this->members->head;

    //max is the max amount of all elements.
    float max = temp->amount ;

    while(temp != nullptr){

        if(max <  temp->amount){

            max = temp->amount;
        }

        temp = temp->next;

    }

    max = (int) (max * 100) / 100.0;

    return max;


}



