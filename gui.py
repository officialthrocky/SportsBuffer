import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QTextEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

Titles = {
   0 : "Passing",
   1 : "Rushing",
   2 : "Receiving",
   3 : "Kicking",
   4 : "Returning",
   5 : "Punting",
   6 : "Defense",
   7 : "Division Comparison"
}

class CSVTableViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SportsBuffer - Sports Utility App & Bet Predictor")
        self.setGeometry(100, 100, 1000, 600)

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QHBoxLayout()
        table_and_menu_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        # Dropdown Menu for Tables
        self.table_selector = QComboBox(self)
        self.table_selector.addItems(["Passing","Rushing","Receiving","Kicking","Returns","Punting","Defense","Division Comparison"])
        self.table_selector.currentIndexChanged.connect(self.switch_table)
        table_and_menu_layout.addWidget(self.table_selector)

        # Label for currently selected team
        # Input Box
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Enter Team Name Here.")
        input_layout.addWidget(self.input_box)

        # Button
        self.button = QPushButton("Load Stats", self)
        self.button.clicked.connect(self.on_submit)
        input_layout.addWidget(self.button)

        # Table
        self.table = QTableWidget(self)
        table_and_menu_layout.addWidget(self.table)
        table_and_menu_layout.addLayout(input_layout)

        # Stored Text Box
        self.stored_text = QTextEdit(self)
        self.stored_text.setPlaceholderText("Team Name: Dallas Cowboys\nOwner: Jerry Jones\nHead Coach: Mike McCarthy\nOffensive Coordinator: Brian Schottenheimer\nDefensive Coordinator: Dan Quinn\nSpecial Teams Coord.: John Fassel\n")
        self.stored_text.setPlainText("Team Name: Dallas Cowboys\nOwner: Jerry Jones\nHead Coach: Mike McCarthy\nOffensive Coordinator: Brian Schottenheimer\nDefensive Coordinator: Dan Quinn\nSpecial Teams Coord.: John Fassel\n")
        self.stored_text.setReadOnly(False)

        # Add to Main Layout
        main_layout.addLayout(table_and_menu_layout, 3)
        main_layout.addWidget(self.stored_text, 1)

        # Set Main Layout
        main_widget.setLayout(main_layout)

        # CSV File Paths - I THINK THIS IS WHERE THE MAGIC WILL HAPPEN

        # Load in the cowboys as default
        self.default_team_selected = "Cowboys"
        self.csv_files = []
        for key, value in Titles.items():
            self.csv_files.append(f"Data/{self.default_team_selected}/{self.default_team_selected}_{value}_stats.csv")
        try:
            self.current_csv_file = self.csv_files[0]
        except:
            print("Error loading default table info")
        # Load Initial Table
        self.load_csv(self.current_csv_file)

    def load_csv(self, csv_file):
        """
        Load CSV data into the table.
        """
        if not os.path.exists(csv_file):
            print(f"{self.current_csv_file} | Was not found. Exiting program")
            exit()

        df = pd.read_csv(csv_file)
        self.populate_table(df)

    def update_text(self, team_name = "Cowboys"):
        df = pd.read_csv("Data/"+ team_name + "/" + team_name + "_info.csv")
        line = f"Selected Team: {df.iloc[0,0]} {df.iloc[0,1]}\nOwner: {df.iloc[0,2]}\nHead Coach: {df.iloc[0,3]}\nOffensive Coordinator: {df.iloc[0,4]}\nDefensive Coordinator: {df.iloc[0,5]}\nSpecial Teams: {df.iloc[0,6]}"
        self.stored_text.setPlainText(line) 

    def populate_table(self, df):
        """
        Populate the QTableWidget with a DataFrame.
        """
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                self.table.setItem(row, column, QTableWidgetItem(str(df.iat[row, column])))
                self.table.item(row, column).setTextAlignment(Qt.AlignCenter)

    def switch_table(self, index):
        """
        Switch the displayed table to the selected CSV file.
        """
        self.current_csv_file = self.csv_files[index]
        self.load_csv(self.current_csv_file)

    def on_submit(self):
        """
        Handle the button click event to load the new set of data files
        """
        user_input = self.input_box.text()
        if not user_input:
            QMessageBox.warning(self, "Input Error", "You need to enter a team name to display stats")
            return
        
        # Use the entered team name to load in all the possible csv files for that team
        self.csv_files.clear()
        # add function to correct and/or match to known team name
        for key, value in Titles.items():
            self.csv_files.append(f"Data/{user_input}/{user_input}_{value}_stats.csv")
        self.current_csv_file[self.table_selector.currentIndex()]

        # Load current CSV into a DataFrame
        df = pd.read_csv(self.current_csv_file)


        # Save back to CSV and refresh the table
        self.populate_table(df)
        self.input_box.clear()

        # Manually refresh the selector to show newly updated stats in table
        self.table_selector.setCurrentIndex(1)
        self.table_selector.setCurrentIndex(0)
        self.update_text(user_input)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVTableViewer()
    viewer.show()
    sys.exit(app.exec_())


