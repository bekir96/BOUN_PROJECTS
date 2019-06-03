#include <QPushButton>
#include <window.h>
#include <QApplication>
#include <QTimer>
#include <QSignalMapper>
#include <QLabel>
#include <QKeyEvent>

//Construct Window with using QWidget
Window::Window(QWidget *parent):QWidget(parent) {
    //Set size of the Window
    setFixedSize(550, 430);
    //Set title of Window
    setWindowTitle("Find The Pairs");

    //Create, position and font the restart button
    QPushButton *restart = new QPushButton("Restart",this);
    restart->setGeometry(370,10,170,50);
    restart->setFont(*restartFont);

    //connect provides when restart button is clicked slotRestartClicked is responded.
    connect(restart, SIGNAL (clicked()), this, SLOT (slotRestartClicked()));

    //Create, position(margin and indent), font and string the pairs and trials labels.
    pairs = new QLabel("Pair: " + QString::number(pairCounter)+ "       ",this);
    trials = new QLabel("Try: " + QString::number(trialCounter) + "       ",this);
    pairs->setFont(*infoFont);
    trials->setFont(*infoFont);
    pairs->setMargin(15);
    trials->setIndent(175);
    trials->setMargin(15);

    //Create mapper to map all push buttons to SLOT in one connect signal.
    mapper = new QSignalMapper(this);
    connect(mapper,SIGNAL(mapped(int)),this,SLOT(slotButtonClicked(int)));

    //Construct all 24 button with initialized it.
    for (int x=0 ; x<6 ; x++) {
        for (int y=0; y<4 ; y++) {
            //initalize button configuration
            initializeButton(x,y);
            //To find button coordinate use 10*x+y
            mapper->setMapping(pushButtons[x][y], 10*x+y);
            connect(pushButtons[x][y], SIGNAL(clicked()), mapper, SLOT(map()));
        }
    }

    //connect provides when finish signal is emitted slotCongratulate is responded.
    connect(this, SIGNAL(finished()),this, SLOT(slotCongratulate()));
}

//Initialize alphabetic button with font, position
void Window::initializeButton(int x, int y){
    pushButtons[x][y] = new QPushButton(this);
    pushButtons[x][y]->setFont(*buttonFont);
    pushButtons[x][y]->setGeometry( 10+x*90, 70+y*90, 80, 80);
    pushButtons[x][y]->setCheckable(true);
    //Set text of pushButtons as a randomly chosen letters.
    realLetters[x][y]=chooseLetter();
    pushButtons[x][y]->setText(realLetters[x][y]);

}

//Functions to make process for clicked pushButtons.
void Window::slotButtonClicked(int coor){

    //x coordinate of pushButtons
    int xcoor=int(coor/10);
    //y coordinate of pushButtons
    int ycoor=coor%10;

    //If situation to control clicked cards is open or close.
    if (pushButtons[xcoor][ycoor]->isChecked()) {
        //Count trial number.
        this->trialCounter++;
        //Control clicked buttons to keep them in stack.
        buttonStack.push(pushButtons[xcoor][ycoor]);
        //When button is clicked, show real text of button.
        pushButtons[xcoor][ycoor]->setText(realLetters[xcoor][ycoor]);
        if(trialCounter%2==0){
            //Grammar correctly control for string 'Trial'
            if(trialCounter == 2){
                trials->setText("Try: " + QString::number(trialCounter/2));
            } else {
                trials->setText("Tries: " + QString::number(trialCounter/2));
            }
            checkPairs();
        }
    }
    else {
        pushButtons[xcoor][ycoor]->setChecked(true);
    }
}

void Window::deactive(){
    for (int x=0 ; x<6 ; x++) {
        for (int y=0; y<4 ; y++) {
            pushButtons[x][y]->setCheckable(false);
        }
    }
    if(button1!=nullptr & button2!=nullptr){
        button1->setCheckable(true);
        button1->setChecked(true);
        button2->setCheckable(true);
        button2->setChecked(true);
    }
}

void Window::active(){

    for (int x=0 ; x<6 ; x++) {
        for (int y=0; y<4 ; y++) {
            pushButtons[x][y]->setCheckable(true);
        }
    }
}

//construct all pushButtons with randomly chosen letters.
QString Window::chooseLetter(){
    int index = rand()%24;
    while(used[index]== true){
        index = rand()%24;
    }
    used[index]=true;
    return alphabet[index];
}

//To close all cards with letter 'X' when user select cards.
void Window::slotCloseCards(){
    for (int x=0 ; x<6 ; x++) {
        for (int y=0; y<4 ; y++) {
            pushButtons[x][y]->setText("X");
        }
    }
    active();
}

void Window::checkPairs(){

    //Checkable first button
    button1 = buttonStack.pop();
    //Checkable second button
    button2 = buttonStack.pop();

    deactive();

    QTimer *timer2 = new QTimer(this);
    timer2->setSingleShot(true);
    timer2->start(1000);

    //Control text of first and second buttons.
    if(button1->text() == button2->text()){
        //Grammar correctly control for string 'Pair'
        if(pairCounter==0)
            pairs->setText("Pair: " + QString::number(++pairCounter));
        else
            pairs->setText("Pairs: " + QString::number(++pairCounter));
        connect(timer2, SIGNAL(timeout()), this, SLOT(slotPairFound()));
        //If situation to pass finish case.
        if(pairCounter==12){
            emit finished();
        }
    }
    else
        connect(timer2, SIGNAL(timeout()), this, SLOT(slotWrongCards()));
}

//Functions for open cards to not enabled if pairs are finded as a correct.
void Window::slotPairFound(){
    button1->setText("");
    button1->setEnabled(false);
    button2->setText("");
    button2->setEnabled(false);
    active();
}

//Functions for open cards to close if pairs are finded as a wrong.
void Window::slotWrongCards(){
    button1->setText("X");
    button1->setChecked(false);
    button2->setText("X");
    button2->setChecked(false);
    active();
}

//Functions to make process for restart.
void Window::slotRestartClicked(){

    //Create newGame Window and show and set Timer
    Window *newGame = new Window;
    newGame->show();
    newGame->slotStartTimer();
    close();
}

//Functions to make process finish and congratulate.
void Window::slotCongratulate(){

    //Create theEnd QWidget with size and window title as 'Done!'
    QWidget *theEnd= new QWidget();
    theEnd->setFixedSize(428, 212);
    theEnd->setWindowTitle("Done!");

    //Construct message of win status
    QLabel* message= new QLabel("Congratulations, \n you found 12 pairs with " + QString::number(trialCounter/2) + " tries!", theEnd);

    //Create, font, alignment and geometry message.
    message->setFont(*restartFont);
    message->setAlignment(Qt::AlignCenter);
    message->setGeometry(45,45,message->minimumSizeHint().width(),message->minimumSizeHint().height());

    //Create ok button and set geometry
    QPushButton* ok = new QPushButton("OK", theEnd);
    ok->setGeometry(10, 152, 408, 50);

    //connect provides when ok button is clicked close is responded.
    connect(ok, SIGNAL(clicked()), theEnd, SLOT(close()));

    //show theEnd QWidget on the screen.
    theEnd->show();
}

//Show all cards as open for a while seconds.
void Window::slotStartTimer(){
    QTimer *timer = new QTimer(this);
    timer->setSingleShot(true);
    timer->start(1500);
    deactive();
    connect(timer, SIGNAL(timeout()), this, SLOT(slotCloseCards()));
}
