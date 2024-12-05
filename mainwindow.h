#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QMenuBar>
#include <QMenu>
#include <QAction>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void switchMode(int index);

private:
    QStackedWidget *centralWidget;

    void createModeWidgets();
    void setupMenuBar();
};

#endif // MAINWINDOW_H
