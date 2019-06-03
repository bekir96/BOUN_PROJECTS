#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include <QPushButton>
#include <QSignalMapper>
#include <QStack>
#include <QLabel>
#include <QTimer>

class QPushButton;
class Window : public QWidget
{
    Q_OBJECT
public:
    explicit Window(QWidget *parent = nullptr);
    //initialize trialCounter which holds trial and pairCounter which holds pairs.
    int trialCounter=0;
    int pairCounter=0;

    //initialize button1 and button2 which hold last 2 clicked button.
    QPushButton* button1= nullptr;
    QPushButton* button2= nullptr;
    QLabel* pairs;
    QLabel* trials;

    //initialize font for restart, pushButtons and trial and pairs buttons.
    QFont* buttonFont = new QFont("Calibri", 30, -1, false);
    QFont* restartFont  = new QFont("Calibri", 15, -1, false);
    QFont* infoFont  = new QFont("Calibri", 20, -1, false);

    bool used[24] = {false};
    QStack <QPushButton*> buttonStack;
    QSignalMapper* mapper;
    QPushButton * pushButtons [6][4];
    //To fill 6x4 table with letters
    QString alphabet[24] = {"A","B","C","D","E","F","G","H","I","J","K","L","A","B","C","D","E","F","G","H","I","J","K","L"};
    //Holds real content.
    QString realLetters[6][4];
    QString chooseLetter();
    void initializeButton(int x, int y);
    void checkPairs();
    void deactive();
    void active();

//To connect signal with functions, create slots.
public slots:
    void slotRestartClicked();
    void slotCloseCards();
    void slotPairFound();
    void slotButtonClicked(int );
    void slotWrongCards();
    void slotCongratulate();
    void slotStartTimer();

//Create to send finish signal
signals:
    void finished();

};

#endif // WINDOW_H
