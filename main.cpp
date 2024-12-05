#include <QApplication>
#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MainWindow window;
    window.resize(800, 600);
    window.setWindowTitle("SportsBuffer - Football Utility & Companion App");
    window.show();

    return app.exec();
}
