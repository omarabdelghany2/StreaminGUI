import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QComboBox, QWidget, QLabel

from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QThread, pyqtSignal, QObject ,pyqtSlot
from PyQt6.QtCore import pyqtSignal, QObject
from dataBase import DatabaseManager
from Schedular import TaskScheduler
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.StreamStarted=False

        self.setWindowTitle("OBS Stream Scheduler")
        self.setStyleSheet("background-color: #17202A ; color: white; font-size: 14pt;")  # Setting background color to grey, text color to white, and font size to 14pt


                # Common stylesheet for buttons
        self.button_style = """
            QPushButton {
                color: white;
                font-size: 16pt;
                background-color: #566573;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #485a67;
            }
            QPushButton:pressed {
                background-color: #3b4a57;
            }
        """


        # Stylesheet for ComboBoxes
        self.combo_box_style = """
            QComboBox {
                background-color: #566573;
                color: white;
                border: 2px solid #8f8f91;
                border-radius: 10px;
                padding: 5px;
            }

        """


        # Label for YouTube Link
        youtube_label = QLabel("URL/Path", self)
        youtube_label.setGeometry(10, 60, 200, 30)  # x, y, width, height
        youtube_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # Textbox for YouTube Link
        self.youtube_link = QLineEdit(self)
        self.youtube_link.setGeometry(150, 60, 400, 30)  # x, y, width, height

        # Label for Date ComboBox
        date_label = QLabel("Select Date:", self)
        date_label.setGeometry(10, 100, 110, 30)  # x, y, width, height
        date_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # Date ComboBox
        self.date_combo = QComboBox(self)
        self.date_combo.setGeometry(130, 100, 60, 30)  # x, y, width, height
        self.date_combo.addItems([str(i) for i in range(1, 32)])
        self.date_combo.setStyleSheet(self.combo_box_style)

        # Label for Month ComboBox
        month_label = QLabel("Select Month:", self)
        month_label.setGeometry(210, 100, 130, 30)  # x, y, width, height
        month_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # Month ComboBox
        self.month_combo = QComboBox(self)
        self.month_combo.setGeometry(350, 100, 140, 30)  # x, y, width, height
        self.month_combo.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        self.month_combo.setStyleSheet(self.combo_box_style)

        # Label for Hour ComboBox
        hour_label = QLabel("Select Hour:", self)
        hour_label.setGeometry(490, 100, 120, 30)  # x, y, width, height
        hour_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # Hour ComboBox
        self.hour_combo = QComboBox(self)
        self.hour_combo.setGeometry(610, 100, 45, 30)  # x, y, width, height
        self.hour_combo.addItems([str(i) for i in range(1, 13)])
        self.hour_combo.setStyleSheet(self.combo_box_style)

        # Label for Select Minutes ComboBox
        minutes_label = QLabel("Select Minutes:", self)
        minutes_label.setGeometry(670, 100, 140, 30)  # x, y, width, height
        minutes_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # Select Minutes ComboBox
        self.minutes_combo = QComboBox(self)
        self.minutes_combo.setGeometry(810, 100, 60, 30)  # x, y, width, height
        self.minutes_combo.addItems([str(i) for i in range(0, 60)])
        self.minutes_combo.setStyleSheet(self.combo_box_style)

        # Label for AM/PM ComboBox
        ampm_label = QLabel("AM/PM:", self)
        ampm_label.setGeometry(880, 100, 70, 30)  # x, y, width, height
        ampm_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        # AM/PM ComboBox
        self.ampm_combo = QComboBox(self)
        self.ampm_combo.setGeometry(960, 100, 60, 30)  # x, y, width, height
        self.ampm_combo.addItems(["AM", "PM"])
        self.ampm_combo.setStyleSheet(self.combo_box_style)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(10, 200, 120, 30)  # x, y, width, height
        self.start_button.setStyleSheet(self.button_style)  # Setting text color to white and font size to 16pt
        self.start_button.clicked.connect(self.start)
        

        # Add Button
        self.add_button = QPushButton("Add", self)
        self.add_button.setGeometry(140, 200, 120, 30)  # x, y, width, height
        self.add_button.setStyleSheet(self.button_style)
        self.add_button.clicked.connect(self.add)

        # Platform ComboBox
        self.platform_combo = QComboBox(self)
        self.platform_combo.setGeometry(270, 200, 160, 30)  # x, y, width, height
        self.platform_combo.addItem("Flussonic")
        # self.platform_combo.addItem("Twitch")
        self.platform_combo.setStyleSheet(self.combo_box_style)
        #Queue TextEdit
        self.setWindowTitle("OBS Stream Schedule")
        self.schedule_info = QTextEdit(self)  # QTextEdit for displaying schedule information
        self.schedule_info.setGeometry(10, 240, 880, 200)  # x, y, width, height
        self.schedule_info.setReadOnly(True)  # Make it read-only
        self.scheduled_items = []  # List to store scheduled items

        #create and object fromDataBase and readIf there is an old Data 
        self.DataBase=DatabaseManager()
        if(self.DataBase.get_all_tasks()):
            print(self.DataBase.get_all_tasks())
            for task in self.DataBase.get_all_tasks(): 
                self.addToTheTextEdit(task[7],task[2],task[1],task[3],task[4],task[5],task[6],task[8])

        #create and object fromDataBase and readIf there is an old Data 
        self.Schedular=TaskScheduler()
        if(self.DataBase.get_all_tasks()):
            print(self.DataBase.get_all_tasks())
            for task in self.DataBase.get_all_tasks(): 
                self.Schedular.add_task(task[1],task[2],task[3],task[4],task[5],task[6],task[7],task[0],task[8])
        self.Schedular.TaskExcuted.connect(self.delete_item_after_excution)
        # Text box for index input
        self.delete_index_input = QLineEdit(self)
        self.delete_index_input.setGeometry(10, 460, 100, 30)  # x, y, width, height
        self.delete_index_input.setValidator(QIntValidator())

        # Button for deleting scheduled item
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setGeometry(120, 460, 100, 30)  # x, y, width, height
        self.delete_button.setStyleSheet(self.button_style)  # Setting text color to white, font size to 16pt, and background color to light grey
        self.delete_button.clicked.connect(self.delete_item)

        ampm_label = QLabel("duration in minutes", self)
        ampm_label.setGeometry(1030, 100, 180, 30)  # x, y, width, height
        ampm_label.setStyleSheet("color: white; font-size: 16pt;")  # Setting text color to white and font size to 16pt

        self.Duraion = QLineEdit(self)
        self.Duraion.setGeometry(1220, 100, 100, 30)  # x, y, width, height
        self.Duraion.setValidator(QIntValidator())


    def start(self):
        if (self.scheduled_items or self.StreamStarted==True):
            print("Start button clicked")
            self.StreamStarted= not self.StreamStarted
            if(self.StreamStarted==True):
                
                self.start_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 16pt;
                background-color: #DA3E1C;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #485a67;
            }
            QPushButton:pressed {
                background-color: #3b4a57;
            } """ )
                self.start_button.setText("Stop")
                # Add functionality to start scheduling here
                self.Schedular.start_schedule()                                                                                  
            else:
                self.start_button.setStyleSheet(self.button_style)  # Setting text color to white and font size to 16pt
                # Add functionality to stop scheduling here
                self.Schedular.stop_schedule()
                self.start_button.setText("Start")
            
    def add(self):
        if  (self.youtube_link.text()):
            youtube_link = self.youtube_link.text()
            date = self.date_combo.currentText()
            month = self.month_combo.currentText()
            hour = self.hour_combo.currentText()
            minutes = self.minutes_combo.currentText()
            ampm = self.ampm_combo.currentText()
            platform = self.platform_combo.currentText()
            duration=self.Duraion.text()
            ### add it to the array becausae its displays on gui 
            self.addToTheTextEdit(youtube_link,date,month,hour,minutes,ampm,platform,duration)

            ### add the task to the backend                                                         
            self.DataBase.add_task(month=month,day=date,hour=hour,minute=minutes,am_pm=ampm,platform=platform,url=youtube_link,duration=duration)
            ### this will be added to the schdulaed tasks                                           TODO
            self.Schedular.add_task(month=month,day=date,hour=hour,minute=minutes,am_pm=ampm,platform=platform,url=youtube_link,indexinGUI=len(self.scheduled_items),duration=duration)




    def addToTheTextEdit(self,youtube_link,date,month,hour,minutes,ampm,platform ,duration):
        schedule_text = f"{len(self.scheduled_items) + 1}) {youtube_link} - {date} {month} at {hour}:{minutes} {ampm} on {platform} for {duration} minutes "
        self.scheduled_items.append(schedule_text)
        self.schedule_info.setPlainText('\n'.join(self.scheduled_items))

    def delete_item(self):
        index_text = self.delete_index_input.text()
        try:
            index = int(index_text)
            if 1 <= index <= len(self.scheduled_items):
                del self.scheduled_items[index - 1]
                # Reindex scheduled items
                for i in range(len(self.scheduled_items)):
                    self.scheduled_items[i] = f"{i + 1}) {self.scheduled_items[i].split(' ', 1)[1]}"
                # Update schedule_info QTextEdit to display all scheduled items
                self.schedule_info.setPlainText('\n'.join(self.scheduled_items))
                self.delete_index_input.clear()
                ### this will be deleted from the schdulaed tasks  
                tasks=self.DataBase.get_all_tasks()
                task=tasks[index-1]
                self.Schedular.delete_task(task[1],task[2],task[3],task[4],task[5],int(task[8]))
                ### delete the task from the backend                                                
                self.DataBase.delete_task(index)
            else:
                print("Index out of range")
        except ValueError:
            print("Invalid index")




    @pyqtSlot(int)
    def delete_item_after_excution(self,number):
        print("i have entered deleteItem")
        try:
            
            if 0 <= number <= len(self.scheduled_items):
                print("i have entered TRY and catch")
                del self.scheduled_items[number - 1]
                # Reindex scheduled items
                for i in range(len(self.scheduled_items)):
                    self.scheduled_items[i] = f"{i + 1}) {self.scheduled_items[i].split(' ', 1)[1]}"
                # Update schedule_info QTextEdit to display all scheduled items
                self.schedule_info.setPlainText('\n'.join(self.scheduled_items))
                self.delete_index_input.clear()
                ### this will be deleted from the schdulaed tasks  
                tasks=self.DataBase.get_all_tasks()
                task=tasks[number-1]
                self.Schedular.delete_task(task[1],task[2],task[3],task[4],task[5],task[8])
                ### delete the task from the backend                                                
                self.DataBase.delete_task(number)

                print("i have finished it")
            else:
                print("Index out of range")
        except ValueError:
            print("Invalid index")        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 1500, 700)  # x, y, width, height
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
