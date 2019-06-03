#include "LinkedList.h"


//empty constructor
LinkedList::LinkedList(){

    //initializing empty linked list
    this->length = 0;
    this->head = nullptr;
    this->tail = nullptr;

}
//copy constructor
LinkedList::LinkedList(const LinkedList &list){


    //If given list is null, making this is list null.
    if(list.head == nullptr){
        this->length = 0;
        this->head = nullptr;
        this->tail = nullptr;
        return;

    }

    this->length = list.length;


    //Looking the list and declaring a new node in each
    if(list.head != nullptr){

        Node* temp;
        Node* temp2;
        this->head = new Node(*list.head);


        temp = this->head;
        temp2 = list.head;
        while(temp2!= list.tail && temp2!= nullptr){

            temp->next = new Node(*temp2->next);
            temp = temp->next;
            temp2 = temp2->next;


        }

        this->tail = temp;

    }



}


//copy assignment operator
LinkedList& LinkedList::operator=(const LinkedList& list){

    //doing same thing copy constructor except deleting this list.
    if(this->head){
        delete this->head;
    }

    this->head = nullptr;
    this->tail = nullptr;
    this->length = 0;
    Node* temp = list.head;

    while(temp != nullptr){

        pushTail(temp->name, temp->amount);
        temp = temp->next;

    }

    return *this;

}



void LinkedList::pushTail(string _name, float _amount){

    this->length++;

    //initializing node with given name and amount.
    Node* addNode = new Node(_name, _amount);
    if(this->head == nullptr){

        this->head = addNode;
        this->tail = this->head;



    } else {

        this->tail->next = addNode;
        this->tail = this->tail->next;


    }

}

//move constructor
LinkedList::LinkedList(LinkedList&& list) {

    if (list.head != nullptr) {
        this->head = move(list.head);
    }
    this->length = list.length;

    list.length=0;
    list.head= nullptr;







}

//move assignment operator
LinkedList& LinkedList::operator=(LinkedList&& list){

    delete this->head;

    if (list.head != nullptr) {
        this->head = move(list.head);
    }
    this->length = list.length;

    list.length=0;
    list.head= nullptr;

    delete list.head;

    return *this;


}




void LinkedList::updateNode(string _name, float _amount){

    //Finding the same name node according to given name.
    if(this->head != nullptr){

        Node* temp;
        temp = this->head;

        while(temp != nullptr){


            if(!temp->name.compare(_name)){


                temp->amount = _amount;

            }

            temp = temp->next;

        }

    }

}


//Destructor
LinkedList::~LinkedList(){

    if(this->head){
        delete this->head;
    }



}

