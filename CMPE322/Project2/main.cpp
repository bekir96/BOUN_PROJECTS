#include <pthread.h>
#include <iostream>
#include <stdio.h>  /* printf, scanf, NULL */
#include <stdlib.h>  /* malloc, free, rand, exit */
#include <string>   
#include <string.h>  /* strtok_rs */
#include <unistd.h> /* UNIX and POSIX constants and functions */
#include <queue> 

#define MAX_THREADS 10  /* Number of ATM threads */
#define MAX_CUSTOMER 300    /* Number of MAX CUSTOMER */
#define BILL_TYPE_NUMBER 5  /* Number of bill type */
#define NANO_SECOND_MULTIPLIER 1000000 /* REFERENCE: https://stackoverflow.com/questions/7684359/how-to-use-nanosleep-in-c-what-are-tim-tv-sec-and-tim-tv-nsec */

// Defining enum BILL 
enum BILL {
    ELECTRICITY, WATER, GAS, TELECOMMUNICATION, CABLETV
};

/*
    This function takes parameter 'bill' as pointer to pointer to char and  finds appropriate 
    case to perform required process which is wanted to implement for us. 'Task which is performed 
    by bill writes beside.'
*/
BILL findBill(std::string bill){
    if(!(strcmp(bill.c_str(), "electricity"))) return ELECTRICITY;
    else if(!(strcmp(bill.c_str(), "water"))) return WATER;
    else if(!(strcmp(bill.c_str(), "gas"))) return GAS;
    else if(!(strcmp(bill.c_str(), "telecommunication"))) return TELECOMMUNICATION;
    else if(!(strcmp(bill.c_str(), "cableTV"))) return CABLETV;
}

struct Customer{
    int customerID; /* Hold number of which input */
    int sleepTime;  /* Hold sleep time of customer */
    int atmInstance;    /* Hold which ATM will execute the customer. */
    std::string billType; /* Hold the bill type of customer. */
    int amount; /* Hold the bill amount of costumer. */
};

int array[10] = {0,1,2,3,4,5,6,7,8,9};  /* To pass safe parameter to atm thread*/
int customer_array[MAX_CUSTOMER];
int temp_array[2];  /* temp_array[0] hold current customer and temp_array[1] count executed customer. */

typedef struct Customer state; 
state customer[MAX_CUSTOMER];   /* Declare array of struct Customer */

/* Mutex thread declaration */
pthread_mutex_t billMutex[BILL_TYPE_NUMBER];    /* Control change of bill type variable */
pthread_mutex_t atmMutex[MAX_THREADS];  /* Control each atm queue */
pthread_mutex_t customerMutex;  /* Control customer number */
pthread_mutex_t writeMutex; /* Control writing to file */
pthread_t atmid[MAX_THREADS],tid[MAX_CUSTOMER]; // Declaration atm and customer threads */

/* Thread function declaration */
void *atmFunc(void *vargp);
void *customerFunc(void *vargp);


/* Global variables of output */
int electricity = 0;
int water = 0;
int gas = 0;
int telecommunication = 0;
int cableTV = 0;

/* Global variables of customer size */
int max_customer = 0;
int customerNumber = 0;

std::vector<std::queue<struct Customer> > atm_queue;
std::string file_output; /* Declare parsed file_output */

/*  
    This function takes a input as pointer to const char. We use the library function 'strtok_r'
    to split the string by the character 'space' and return the array of strings instead. We also
    terminate the array 'NULL'. Currently our command buffer allocates 8 blocks only. If we enter 
    a command which has more than 8 words, our command will not work as expected. But in this
    project, input which is greater than 4 words is invalid input.
*/
char** get_input(char *input) {
    char **command = (char**)malloc(4 * sizeof(char *));
    if (command == NULL) { /* It can fail if the OS runs out of memory. We should exit the program. */
        perror("malloc failed");
        exit(1);
    }
    char *separator = (char* )",";  // seperator
    char *parsed, *brkt;    //  used for srttok_r parameter
    int index = 0;  // used for memmove control 

    parsed = strtok_r(input, separator, &brkt);
    // Go through the parsed string and store each argument in command.
    while (parsed) {
        command[index] = parsed;
        index++;
        parsed = strtok_r(NULL, separator, &brkt);
    }
    command[index] = NULL;
    return command;
}

/*
    remove all current spesific from string.
*/
std::string removeAll( std::string str, const std::string& from) {
    size_t start_pos = 0;
    while( ( start_pos = str.find( from)) != std::string::npos) {
        str.erase( start_pos, from.length());
    }
    return str;
}


int main(int argc, char**argv){
    char** cmd; // To hold parsed line input *//
    int i = 0;
    char str[100]; // To hold each line of input txt

    /* Control number of arguments */
    if(argc !=2){
        printf("usage: %s <input.txt>\n", argv[0]);
        exit(0);
    }    

    /* Initializes vector of queue with size 10. */
    std::queue<struct Customer> q;
    for(i=0 ; i<10 ; i++ ) atm_queue.push_back(q);

    /* open input and output file respectively stdin and stdout */
    freopen(argv[1], "r", stdin);
    file_output = removeAll( argv[1], ".txt") + "_log.txt";
    freopen(file_output.c_str(), "w", stdout);
    
    scanf("%d", &temp_array[0]);

    /* Pass atmFunc to atmid[atm_number] with atm_number */
    for(i = 0; i < MAX_THREADS; i++)    pthread_create(&atmid[array[i]], NULL, atmFunc, &array[i]);
    

    i = 0;
    /* Read input from file and fill field of struct Customer */
    while(i != temp_array[0]){
        scanf("%s",str);
        cmd = get_input(str);
        customer[i].customerID = i+1;
        customer[i].sleepTime = atoi(cmd[0]);
        customer[i].atmInstance = atoi(cmd[1]);
        customer[i].billType = cmd[2];
        customer[i].amount = atoi(cmd[3]);
        i++;
    }
    /* Pass customerFunc to tid[customer_number] with proper struct Customer */
    for(i=0 ; i < temp_array[0]; i++)   pthread_create(&tid[i], NULL, customerFunc, &customer[i]);

    for(i = 0 ; i < temp_array[0] ; i++)    pthread_join(tid[customer_array[i]], NULL);
    for(i = 0 ; i < MAX_THREADS ; i++)  pthread_join(atmid[array[i]], NULL);

    /* Write output log to file as requested from us. */
    printf("%s\n%s: %d\n%s: %d\n%s: %d\n%s: %d\n%s: %d","All payments are completed.","CableTv",
                    cableTV,"Electricity",electricity,"Gas",gas,"Telecommunication",telecommunication,"Water",water);

    // Let the OS know everything is a-okay.
    return 0;
}

/* Shortly, add customer instance to proper atm queue by control from atmMuex */
void *customerFunc(void *vargp){
    struct Customer customer = *(struct Customer*)vargp;
    int atmInstance = customer.atmInstance-1;
    timespec sleepValue = {0};
    sleepValue.tv_nsec = customer.sleepTime*NANO_SECOND_MULTIPLIER;
    nanosleep(&sleepValue, NULL);
    pthread_mutex_lock(&atmMutex[atmInstance]);
    atm_queue[customer.atmInstance-1].push(customer);
    pthread_mutex_unlock(&atmMutex[atmInstance]);
    return NULL;
}

/*
    In regard of the value of atmMutex, billMutex, customerMutex and writeMutex, respectively do 
    pop from proper atm queue, sum and write bill type variable, write output file and inc 
    customerNumber
*/
void *atmFunc(void *vargp){
    int atm_number = *(int *)vargp;
    while(temp_array[1] != temp_array[0]){
        /* If queue is not empty, atm can execute transaction. */
        while(!atm_queue[atm_number].empty()){
            pthread_mutex_lock(&atmMutex[atm_number]);
            struct Customer customer = atm_queue[atm_number].front();   /* To get fifo from queue */
            switch(findBill(customer.billType)){
                case ELECTRICITY:   /* Enter if input bill type format is 'electiricity' */
                {
                    pthread_mutex_lock(&billMutex[static_cast<int>(BILL::ELECTRICITY)]);
                    electricity+= customer.amount;
                    pthread_mutex_unlock(&billMutex[static_cast<int>(BILL::ELECTRICITY)]);
                break;}

                case WATER: /* Enter if input bill type format is 'water' */
                {
                    pthread_mutex_lock(&billMutex[static_cast<int>(BILL::WATER)]);
                    water+= customer.amount;
                    pthread_mutex_unlock(&billMutex[static_cast<int>(BILL::WATER)]);
                break;}

                case GAS:   /* Enter if input bill type format is 'gas' */
                {
                    pthread_mutex_lock(&billMutex[static_cast<int>(BILL::GAS)]);
                    gas+= customer.amount;
                    pthread_mutex_unlock(&billMutex[static_cast<int>(BILL::GAS)]);
                break;}

                case TELECOMMUNICATION: /* Enter if input bill type format is 'telecommunication' */
                {
                    pthread_mutex_lock(&billMutex[static_cast<int>(BILL::TELECOMMUNICATION)]);
                    telecommunication+= customer.amount;
                    pthread_mutex_unlock(&billMutex[static_cast<int>(BILL::TELECOMMUNICATION)]);
                break;}

                case CABLETV:   /* Enter if input bill type format is 'cableTV' */
                {
                    pthread_mutex_lock(&billMutex[static_cast<int>(BILL::CABLETV)]);
                    cableTV+= customer.amount;
                    pthread_mutex_unlock(&billMutex[static_cast<int>(BILL::CABLETV)]);
                break;}
            }
            /* Write section*/
            pthread_mutex_lock(&writeMutex);
            printf("%s%d,%d,%s\n","Customer",customer.customerID, customer.amount, customer.billType.c_str());
            pthread_mutex_unlock(&writeMutex);

            /* Change shared variable section */
            pthread_mutex_lock(&customerMutex);
            temp_array[1]++;
            pthread_mutex_unlock(&customerMutex);
            
            atm_queue[atm_number].pop();
            pthread_mutex_unlock(&atmMutex[atm_number]);
        }
    }
}
