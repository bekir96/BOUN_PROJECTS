#include <QApplication>
#include <QPushButton>
#include <window.h>


int main(int argc, char **argv)
{

    QApplication app (argc, argv);

    srand(uint(time(nullptr)));

    Window window;

    //Create opening screen and construct size and title.
    QWidget start;
    start.setFixedSize(219, 181);
    start.setWindowTitle("Hello!");

    //Opening screen message
    QLabel* message= new QLabel("Find all pairs\nTo start press OK", &start);

    //Set font, alignment and size of message.
    message->setFont(QFont("Calibri", 15, -1, false));
    message->setAlignment(Qt::AlignCenter);
    message->setGeometry(45,45,message->minimumSizeHint().width(),message->minimumSizeHint().height());

    //Create start button 'OK', set geometry and connect it with window.
    QPushButton* ok = new QPushButton("OK", &start);
    ok->setGeometry(10, 121, 199, 50);
    QObject::connect(ok, SIGNAL(clicked()), &start, SLOT(close()));
    QObject::connect(ok, SIGNAL(clicked()), &window, SLOT(show()));
    QObject::connect(ok, SIGNAL(clicked()), &window, SLOT(slotStartTimer()));

    start.show();

    return app.exec();
}
