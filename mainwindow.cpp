#include "mainwindow.h"
#include <QLabel>
#include <QVBoxLayout>
#include <QPushButton>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    // Create a central widget
    centralWidget = new QStackedWidget(this);
    setCentralWidget(centralWidget);

    // Create different "modes" as widgets
    createModeWidgets();

    // Set up the menu bar
    setupMenuBar();
}

void MainWindow::createModeWidgets() {
    // Mode 1
    QWidget *mode1Widget = new QWidget(this);
    QVBoxLayout *mode1Layout = new QVBoxLayout(mode1Widget);
    QLabel *mode1Label = new QLabel("This is Mode 1");
    QPushButton *mode1Button = new QPushButton("Click Me!");
    mode1Layout->addWidget(mode1Label);
    mode1Layout->addWidget(mode1Button);
    mode1Widget->setLayout(mode1Layout);
    centralWidget->addWidget(mode1Widget);

    // Mode 2
    QLabel *mode2Label = new QLabel("Compare Players WIP");
    mode2Label->setAlignment(Qt::AlignCenter);
    centralWidget->addWidget(mode2Label);

    // Mode 3
    QLabel *mode3Label = new QLabel("Fantasy Grader WIP");
    mode3Label->setAlignment(Qt::AlignCenter);
    centralWidget->addWidget(mode3Label);
}

void MainWindow::setupMenuBar() {
    // Create a menu bar
    QMenuBar *menuBar = new QMenuBar(this);
    QMenu *menu = new QMenu("Modes", menuBar);
    menuBar->addMenu(menu);
    setMenuBar(menuBar);

    // Create actions for switching modes
    QAction *mode1Action = new QAction("Team Viewer", this);
    QAction *mode2Action = new QAction("Compare Players", this);
    QAction *mode3Action = new QAction("Fantasy Grader", this);

    // Connect actions to their respective slots
    connect(mode1Action, &QAction::triggered, this, [this]() { switchMode(0); });
    connect(mode2Action, &QAction::triggered, this, [this]() { switchMode(1); });
    connect(mode3Action, &QAction::triggered, this, [this]() { switchMode(2); });

    // Add actions to the menu
    menu->addAction(mode1Action);
    menu->addAction(mode2Action);
    menu->addAction(mode3Action);
}

void MainWindow::switchMode(int index) {
    centralWidget->setCurrentIndex(index);
}
