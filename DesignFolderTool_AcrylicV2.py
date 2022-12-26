# Hello #
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import shutil
from BlurWindow.blurWindow import blur

# Read paths.txt file to get path
with open('paths.txt', encoding='utf8') as f:
    paths = f.readlines()
# End read paths.txt file to get path

# Variables
design_folder_path = paths[0]
folder_template_path = paths[1]
ECO_folder_template_name = paths[2]
new_folder_template_name = paths[3]
external_issue_folder_path = paths[4]
#---------------------------------------------------------------------------------------------------#
design_folder_path = design_folder_path[len(
    'DESIGN_FOLDER_PATH')+1:].replace("\n", "")
folder_template_path = folder_template_path[len(
    'FOLDER_TEMPLATE_PATH')+1:].replace("\n", "")
ECO_folder_template_name = ECO_folder_template_name[len(
    'ECO_FOLDER_TEMPLATE_NAME')+1:].replace("\n", "")
new_folder_template_name = new_folder_template_name[len(
    'NEW_FOLDER_TEMPLATE_NAME')+1:].replace("\n", "")
external_issue_folder_path = external_issue_folder_path[len(
    'EXTERNAL_ISSUE_FOLDER_PATH')+1:].replace("\n", "")
external_issue_folder_path = external_issue_folder_path.replace("username", os.environ.get('USERNAME'))

__build__ = True
#--------------------------------------------------------------------------------------------------------------------------#
# Start App class
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Design Folder Tool"
        self.width = 550
        self.height = 150
        
        screen = app.primaryScreen()
        self.left = int(screen.size().width()/2) - int(self.width/2)
        self.top = int(screen.size().height()/2) - int(self.height/2) - 100

        self.suffix = "-xx"
        self.initUI()

    def initUI(self):
        # Set blur effect to window
        blur(self.winId())

        # Setup window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint) 
          
        #Set Title
        self.Title = QLabel("Welcome", self)
        self.Title.setFont(QFont('Arial', 15))

        # Set message
        self.message = QLabel("", self)
        self.message.setFont(QFont('Arial', 10))
        self.message.setStyleSheet(
            "color: rgb(0,255,0);background-color: rgba(0, 0, 0, 0)")

        if os.environ.get('USERNAME') == "pnnhien":
            self.message.setStyleSheet(
                "color: rgb(255,255,255);background-color: rgba(0, 0, 0, 0)")

        # Part number label
        self.part_number_label = QLabel("Part number", self)
        self.part_number_label.setFont(QFont('Arial', 10))
        self.part_number_label.setStyleSheet(
            'color: rgb(255,255,255); background-color: rgba(0, 0, 0, 0)')

        # Design folder link (label)
        design_folder_link_label = QLabel(design_folder_path, self)
        design_folder_link_label.setFont(QFont('Arial', 8))
        design_folder_link_label.setStyleSheet(
            "color: rgb(255,255,255); background-color: rgba(0, 0, 0, 0)")

        # Part number box
        self.part_number_textbox = QLineEdit(self)
        self.part_number_textbox.setFont(QFont('Arial', 12))
        self.part_number_textbox.setToolTip(
            '(1) Typing PCX-000000 or pcx-000000, \n      MSP-000000 or msp-000000 then enter.\n(2) Ctrl+E to search in external issue folder')

        # ECO number label
        self.ECO_number_label = QLabel("ECO")
        self.ECO_number_label.setFont(QFont('Arial', 10))
        self.ECO_number_label.setStyleSheet(
            'color: rgb(255,255,255); background-color: rgba(0, 0, 0, 0)')

        self.ECO_part_number_textbox = QLineEdit(self)
        self.ECO_part_number_textbox.setFont(QFont('Arial', 12))
        self.ECO_part_number_textbox.setToolTip('Enter ECO number, ex: 12345')

        # Create Buttons
        CloseWindowButton = QPushButton("Close", self)
        MinWindowButton = QPushButton("Minimize", self)

        Create_ECO_button = QPushButton(" Create \n ECO Folder ", self)
        Create_button = QPushButton("Create \n Folder", self)
        Open_button = QPushButton("Open \n Folder", self)
        Open_ECO_button = QPushButton("Open ECO \n Folder", self)
        Open_Latest_ECO_button = QPushButton("Open latest \n ECO Folder", self)

        radiobutton_xx = QRadioButton("-xx")
        radiobutton_xx.setChecked(True)
        radiobutton_01 = QRadioButton("-01")
        radiobutton_01.setStyleSheet(
            'color: rgb(255,255,255);background-color: rgba(0, 0, 0, 0)')
        radiobutton_xx.setStyleSheet(
            'color: rgb(255,255,255);background-color: rgba(0, 0, 0, 0)')

        # Buttons function
        Create_button.clicked.connect(self.Create_Folder)
        Create_ECO_button.clicked.connect(self.Create_ECO_Folder)
        
        Open_button.clicked.connect(self.Open_Folder)
        Open_ECO_button.clicked.connect(self.Open_ECO_Folder)
        Open_Latest_ECO_button.clicked.connect(self.Open_Latest_ECO_Folder)
        
        design_folder_link_label.mousePressEvent = self.Open_Parent_Design_Folder
        
        radiobutton_xx.toggled.connect(self.radiobutton_xx_Clicked)
        radiobutton_01.toggled.connect(self.radiobutton_01_Clicked)
        
        CloseWindowButton.clicked.connect(self.Close_window)
        MinWindowButton.clicked.connect(self.Minimize_window)

        # Set Font for buttons
        Create_button.setFont(QFont('Arial', 10))
        Create_ECO_button.setFont(QFont('Arial', 10))
        Open_button.setFont(QFont('Arial', 10))
        Open_ECO_button.setFont(QFont('Arial', 10))
        Open_Latest_ECO_button.setFont(QFont('Arial', 10))

        #------------------------------------------------------------------#
        # Button icon
        if __build__ == True:
            self.setWindowIcon(QIcon('icon/search.png'))
            Open_button.setIcon(
                QIcon('icon/find.png'))
            Open_ECO_button.setIcon(
                QIcon('icon/find_eco.png'))
            Create_button.setIcon(
                QIcon('icon/create.png'))
            Create_ECO_button.setIcon(
                QIcon('icon/create_eco.png'))
            Open_Latest_ECO_button.setIcon(
                QIcon('icon/find_eco.png'))
        else:
            self.setWindowIcon(QIcon('my_app_venv_01/app/dist/icon/icon.png'))
            Open_button.setIcon(
                QIcon('my_app_venv_01/app/dist/icon/find.png'))
            Open_ECO_button.setIcon(
                QIcon('my_app_venv_01/app/dist/icon/find_eco.png'))
            Create_button.setIcon(
                QIcon(r'my_app_venv_01\app\dist\icon\create.png'))
            Create_ECO_button.setIcon(
                QIcon(r'my_app_venv_01\app\dist\icon\create_eco.png'))
            Open_Latest_ECO_button.setIcon(
                QIcon(r'my_app_venv_01\app\dist\icon\find_eco.png'))
        #------------------------------------------------------------------#
        # Window Title Style Sheet
        self.setStyleSheet("background-color: rgba(0, 0, 0, 80)")

        # Title style sheet in window
        self.Title.setStyleSheet(
            "color: rgb(255,255,255);background-color: rgba(0, 0, 0, 0)")

        # Text box Style
        self.part_number_textbox.setStyleSheet("QLineEdit{"
                                               "border-radius: 7px;"
                                               "border: 1px solid black;"
                                               "color: rgb(255,255,255);"
                                               "}"
                                               )
        self.ECO_part_number_textbox.setStyleSheet("QLineEdit{"
                                                   "border-radius: 7px;"
                                                   "border: 1px solid black;"
                                                   "color: rgb(255,255,255);"
                                                   "}"
                                                   )
        # BUttons Style
        CloseWindowButton.setStyleSheet("QPushButton"
                                        "{"
                                        "border-radius: 0px;"
                                        "color: rgb(255,255,255);"
                                        "background-color: rgba(0,0,0,0);"
                                        "}"
                                        "QPushButton::pressed"
                                        "{"
                                        "background-color : #CDCDCD;"
                                        "}"
                                        )
        MinWindowButton.setStyleSheet("QPushButton"
                                      "{"
                                      "border-radius: 0px;"
                                      "color: rgb(255,255,255);"
                                      "background-color: rgba(0,0,0,0);"
                                      "}"
                                      "QPushButton::pressed"
                                      "{"
                                      "background-color : #CDCDCD;"
                                      "}"
                                      )
        Create_button.setStyleSheet("QPushButton"
                                    "{"
                                    "background-color : #CCECFF;"
                                    "}"
                                    "QPushButton::pressed"
                                    "{"
                                    "background-color : #B3E6FF;"
                                    "}"
                                    "QPushButton"
                                    "{"
                                    "border: 1px solid #3399FF;"
                                    "}"
                                    "QPushButton"
                                    "{"
                                    "border-radius: 10px;"
                                    "color: rgb(0,0,0);"
                                    "}"
                                    )
        Open_button.setStyleSheet("QPushButton"
                                  "{"
                                  "background-color : #D9FFEC;"
                                  "}"
                                  "QPushButton::pressed"
                                  "{"
                                  "background-color : #C5FFE2;"
                                  "}"
                                  "QPushButton"
                                  "{"
                                  "border: 1px solid #33CC33;"
                                  "}"
                                  "QPushButton"
                                  "{"
                                  "border-radius: 10px;"
                                  "color: rgb(0,0,0);"
                                  "}"
                                  )
        Create_ECO_button.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color : #FFFFCC;"
                                        "}"
                                        "QPushButton::pressed"
                                        "{"
                                        "background-color : #FFFFFF;"
                                        "}"
                                        "QPushButton"
                                        "{"
                                        "border: 1px solid #FF9933;"
                                        "}"
                                        "QPushButton"
                                        "{"
                                        "border-radius: 10px;"
                                        "color: rgb(0,0,0);"
                                        "}"
                                        )
        Open_ECO_button.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : #D9FFEC;"
                                      "}"
                                      "QPushButton::pressed"
                                      "{"
                                      "background-color : #C5FFE2;"
                                      "}"
                                      "QPushButton"
                                      "{"
                                      "border: 1px solid #33CC33;"
                                      "}"
                                      "QPushButton"
                                      "{"
                                      "border-radius: 10px;"
                                      "color: rgb(0,0,0);"
                                      "}"
                                      )
        Open_Latest_ECO_button.setStyleSheet("QPushButton"
                                             "{"
                                             "background-color : #EEDDFF;"
                                             "}"
                                             "QPushButton::pressed"
                                             "{"
                                             "background-color : #DBB7FF;"
                                             "}"
                                             "QPushButton"
                                             "{"
                                             "border: 1px solid #6600FF;"
                                             "}"
                                             "QPushButton"
                                             "{"
                                             "border-radius: 10px;"
                                             "color: rgb(0,0,0);"
                                             "}"
                                             )

        # Describe buttons function
        Open_button.setToolTip('Click to open folder \nor press Enter!')
        Open_ECO_button.setToolTip(
            'Click to open ECO folder \nor press Enter!')
        Open_Latest_ECO_button.setToolTip('Click to open LATEST ECO folder!')
        
        Create_button.setToolTip('Click to create folder!')
        Create_ECO_button.setToolTip('Click to create ECO folder!')
        
        MinWindowButton.setToolTip('Minimize')
        CloseWindowButton.setToolTip('Close')

        # Create a vertical layout
        vbox2 = QVBoxLayout()
        vbox2.addWidget(radiobutton_xx)
        vbox2.addWidget(radiobutton_01)

        # Create horizontal layouts
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.part_number_label)
        hbox1.addWidget(self.part_number_textbox)
        hbox1.addLayout(vbox2)
        hbox1.addWidget(self.ECO_number_label)
        hbox1.addWidget(self.ECO_part_number_textbox)
        hbox1.addWidget(Create_ECO_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(Create_button)
        hbox2.addWidget(Open_button)
        hbox2.addWidget(Open_ECO_button)
        hbox2.addWidget(Open_Latest_ECO_button)

        # Create search result list
        self.listwidget = ListWidget()
        self.listwidget.setStyleSheet(
            "color: rgb(255,255,255); border-radius: 10px; background-color : rgba(150,150,150,80);")
        
        self.listwidget.itemClicked.connect(self.listwidget.Initial)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.Title)
        hbox3.addStretch(1)
        hbox3.addWidget(self.message)
        hbox3.addStretch(1)
        hbox3.addWidget(MinWindowButton)
        hbox3.addWidget(CloseWindowButton)

        # Create vertical layout
        vbox = QVBoxLayout()
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(design_folder_link_label)
        vbox.addWidget(self.listwidget)

        # Set layout
        self.setLayout(vbox)

        # Show layout
        self.show()

    def Open_Folder(self):
        
        self.message.setText("")
        self.listwidget.clear()  # Clearing list for new searching
        if self.part_number_textbox.text() != "":  # if the part number is available
            # Set full part number format
            #part_number = self.part_number_textbox.text().upper() + "-xx"
            part_number = self.part_number_textbox.text().upper() + self.suffix

            # Get  full path of folder
            path = design_folder_path + chr(92) + part_number

            # Check folder exists
            if os.path.exists(path) == 1:
                os.startfile(path, 'open')
            # If folder don't exist, runing Advanced Search mode
            else:
                list_result = AdvancedSearch(
                    self.part_number_textbox.text(), design_folder_path)  # result a list type

                if len(list_result) < 1:  # is empty
                    self.message.setText("Folder don't exist")

                if len(list_result) == 1:  # has only a folder
                    Open_Folder2(design_folder_path, list_result[0])

                if len(list_result) > 1:  # is not empty
                    if list_result[0] != "":  # has data
                        for i in list_result:
                            self.listwidget.addItem(i)
                    else:  # has not data
                        self.message.setText("Folder don't exist")
                
                self.listwidget.itemClicked.disconnect()
                self.listwidget.itemClicked.connect(self.listwidget.Clicked1)
            # End of Advanced Search mode
        else:  # if the part number is not available
            # self.MsgBox(
            #     "Warning!", "Please type Part Number!", 1)
            self.message.setText("Please type Part Number!")

    def Open_ECO_Folder(self, eco_number=""):
        self.message.setText("")
        status = True

        if eco_number == False and self.ECO_part_number_textbox.text() == "":
            #self.MsgBox("Warning!", "Please type ECO Number!", 1)
            self.message.setText("Please type ECO Number!")
            status = False

        if eco_number == False and self.ECO_part_number_textbox.text() != "":
            eco_number = self.ECO_part_number_textbox.text()
            if ECO_number_format(eco_number) == 0:
                #Msg(text = "The ECO info is not a number!")
                self.message.setText("Folder don't exist")
                return 0
            status = True

        if status == True:
            count = False
            for folder_name in os.listdir(design_folder_path):
                folder_name_temp = folder_name.upper()
                if folder_name_temp.find("ECO") != -1:
                    temp_number = folder_name[folder_name_temp.find("ECO")+3:]
                    temp_number = temp_number.replace("-", "")
                    temp_number = temp_number.replace(" ", "")
                    temp_number = temp_number.replace("_", "")
                    temp_number = temp_number.replace("#", "")
                    if eco_number == temp_number:
                        count = True
                        eco_number = folder_name

            if count == True:
                path = design_folder_path + chr(92) + eco_number
                os.startfile(path, 'open')
                return 0
            else:
                #self.MsgBox("Warning!", "The ECO number don't exist, please check again!", 1)
                self.message.setText("The ECO number don't exist")
                return 0

    def Open_Latest_ECO_Folder(self):
        self.message.setText("")
        part_number = self.part_number_textbox.text().upper()
        if part_number != "":
           # count = False
            temp_number_list = []
            for folder_name in os.listdir(design_folder_path):
                folder_name_temp = folder_name.upper()
                if folder_name_temp.find("ECO") != -1:
                    if folder_name[0:10] == part_number:
                        temp_number = folder_name[folder_name_temp.find(
                            "ECO")+3:]
                        temp_number = temp_number.replace("-", "")
                        temp_number = temp_number.replace(" ", "")
                        temp_number = temp_number.replace("_", "")
                        temp_number = temp_number.replace("#", "")
                        temp_number_list.append(temp_number)

            if len(temp_number_list) == 0:
                #self.MsgBox( "Warning!", "No ECO Folder!", 1)
                self.message.setText("No ECO Folder!")
                return 0

            max = int(temp_number_list[0])
            for i in temp_number_list[1:]:
                if max < int(i):
                    max = int(i)
            self.Open_ECO_Folder(eco_number=str(max))
        else:
            #self.MsgBox( "Warning!", "Please type Part Number!", 1)
            self.message.setText("Please type Part Number!")

    def Open_Parent_Design_Folder(self, event):
        self.message.setText("")
        os.startfile(design_folder_path, 'open')

    def Create_Folder(self):
        self.message.setText("")
        if self.part_number_textbox.text() != "":
            status, prefix_type = Part_Number_Fomat(
                self.part_number_textbox.text().upper())

            if status == 0:
                #self.MsgBox("Warning!", "Wrong format!", 1)
                self.message.setText("Wrong format!")
                return 0

            part_number = self.part_number_textbox.text().upper() + self.suffix
            path = design_folder_path + chr(92) + part_number

            if os.path.exists(path) == 0:  # not existed
                scr = folder_template_path + chr(92) + new_folder_template_name

                shutil.copytree(scr, path)

                # Remove "desktop.ini" file has been automatially created
                if os.path.exists(path+chr(92)+"desktop.ini") == 1:
                    os.remove(path+chr(92)+"desktop.ini")

                os.startfile(path, 'open')
            else:  # existed
                #self.MsgBox("Warning!", "Folder Existed, please check again!", 1)
                self.message.setText("Folder Existed, please check again!")
        else:
            #self.MsgBox("Warning!", "Please type Part Number!", 1)
            self.message.setText("Please type Part Number!")

    def Create_ECO_Folder(self):
        self.message.setText("")
        if self.part_number_textbox.text() != "":
            status, prefix_type = Part_Number_Fomat(
                self.part_number_textbox.text().upper())
            if status == 0:
                # self.MsgBox("Warning!", "Wrong format!", 1)
                self.message.setText("Wrong format!")
                return 0

            if self.ECO_part_number_textbox.text() != "":

                # Check ECO format before creating ECO folder
                if ECO_number_format(self.ECO_part_number_textbox.text()) == 0:
                    #self.MsgBox("Warning!", "Wrong format!", 1)
                    self.message.setText("Wrong format!")
                    return 0

                # Get part number and ECO number
                part_number = self.part_number_textbox.text().upper() + self.suffix + "_ECO "
                eco_number = self.ECO_part_number_textbox.text()

                # Get path
                path = design_folder_path + chr(92) + part_number + eco_number
                if os.path.exists(path) == 0:  # if ECO folder did not exist
                    scr = folder_template_path + \
                        chr(92) + ECO_folder_template_name

                    shutil.copytree(scr, path)  # Copy

                    # remove "desktop.ini" file has been automatially created
                    if os.path.exists(path+chr(92)+"desktop.ini") == 1:
                        os.remove(path+chr(92)+"desktop.ini")
                    os.startfile(path, 'open')
                else:  # if ECO folder existed
                    # self.MsgBox(
                    #     "Warning!", "Folder Existed, please check again!", 1)
                    self.message.setText("Folder Existed, please check again!")
            else:
                #self.MsgBox("Warning!", "Please type ECO Number!", 1)
                self.message.setText("Please type ECO Number!")
        else:
            #self.MsgBox("Warning!", "Please type Part Number!", 1)
            self.message.setText("Please type Part Number!")

    # def MsgBox(self, title, text, icon):
    #     self.msg = QMessageBox()
    #     self.msg.setWindowTitle(title)
    #     self.msg.setText(text)
    #     if icon == 0:
    #         self.msg.setIcon(QMessageBox.Critical)
    #     if icon == 1:
    #         self.msg.setIcon(QMessageBox.Warning)
    #     if icon == 2:
    #         self.msg.setIcon(QMessageBox.Information)
    #     if icon == 3:
    #         self.msg.setIcon(QMessageBox.Question)
    #     return self.msg.exec_()
    def Open_External_Issue_Folder(self):
        self.message.setText("")
        self.listwidget.clear()  # Clearing list for new searching
        
        if self.part_number_textbox.text() != "":  # if the part number is available
            # Set full part number format
            #part_number = self.part_number_textbox.text().upper() + "-xx"
            part_number = self.part_number_textbox.text().upper() + self.suffix

            # Get  full path of folder
            path = external_issue_folder_path + chr(92) + part_number

            # Check folder exists
            if os.path.exists(path) == 1:
                os.startfile(path, 'open')
            # If folder don't exist, runing Advanced Search mode
            else:
                list_result = AdvancedSearch(
                    self.part_number_textbox.text(), external_issue_folder_path)  # result a list type

                if len(list_result) < 1:  # is empty
                    #self.MsgBox("Error!", "Folder don't exist, please check again!.", 0)
                    self.message.setText("Folder don't exist")

                if len(list_result) == 1:  # has only a folder
                    Open_Folder2(external_issue_folder_path, list_result[0])

                if len(list_result) > 1:  # is not empty
                    if list_result[0] != "":  # has data
                        for i in list_result:
                            self.listwidget.addItem(i)
                    else:  # has not data
                        #self.MsgBox("Error!", "Folder don't exist, please check again!.", 0)
                        self.message.setText("Folder don't exist")
                self.listwidget.itemClicked.disconnect()
                self.listwidget.itemClicked.connect(self.listwidget.Clicked2)
            # End of Advanced Search mode
        else:  # if the part number is not available
            # self.MsgBox(
            #     "Warning!", "Please type Part Number!", 1)
            self.message.setText("Please type Part Number!")
        
    def keyPressEvent(self, event):
        self.message.setText("")
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_E and self.part_number_textbox.text() != "":
            self.Open_External_Issue_Folder()
        
        elif (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.part_number_textbox.text() != "":
            self.Open_Folder()

        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ECO_part_number_textbox.text() != "":
            if ECO_number_format(self.ECO_part_number_textbox.text()):
                self.Open_ECO_Folder(self.ECO_part_number_textbox.text())
               
    def radiobutton_xx_Clicked(self):
        self.message.setText("")
        self.radiobutton_xx = self.sender()
        if self.radiobutton_xx.isChecked():
            self.suffix = "-xx"

    def radiobutton_01_Clicked(self):
        self.message.setText("")
        self.radiobutton_01 = self.sender()
        if self.radiobutton_01.isChecked():
            self.suffix = "-01"

    def mousePressEvent(self, event):
        self.message.setText("")
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        self.message.setText("")
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

    def Close_window(self):
        self.close()

    def Minimize_window(self):
        self.showMinimized()

# End of App class #
#---------------------------------------------------------------------------------------------------------------------------#
def Part_Number_Fomat(part_number=""):
    # Full part number example: MSP-XXXXXX-xx, 402-XXXXXX-01, HAN-XXXXXX-01, etc.....
    cond1 = 1  # For length of part_number
    cond2 = 1  # For number
    cond3 = 1  # For suffix
    prefix_type = ""

    # Check length of part_number
    if len(part_number) >= 10:
        # must include "-" char at the third position from left to right
        if part_number[3] == "-":
            cond1 = 1  # exist
        else:
            cond1 = 0  # not exit
    else:
        return 0, prefix_type

    # Check prefix format
    str_ = part_number[0:3]
    for i in str_:
        if (i >= chr(65) and i <= chr(90)) or (i >= chr(97) and i <= chr(122)):  # check prefix is letter
            cond2 *= 1
            prefix_type = 'letter'
        else:
            cond2 = 0
            prefix_type = ""

    if cond2 == 0:
        cond2 = 1
        for i in str_:
            if i >= chr(48) and i <= chr(57):  # check prefix is letter
                cond2 *= 1
                prefix_type = 'letter'
            else:
                cond2 = 0
                prefix_type = ""

    # Check number series format
    str_ = part_number[4:]
    for i in str_:
        if i >= chr(48) and i <= chr(57):  # check number series is numberic
            cond3 *= 1
        else:
            cond3 = 0

    # Result
    result = cond1*cond2*cond3
    if result == 1:
        return result, prefix_type
    if result == 0:
        return result, prefix_type


def ECO_number_format(number):
    result = 1
    for i in number:
        if i >= chr(48) and i <= chr(57):
            result *= 1
        else:
            result = 0

    if result == 1:
        return result
    else:
        return 0

# AdvancedSearch() function
def AdvancedSearch(name, folder_path):
    if name == "":
        return 0
    result_list = []
    for folder_name in os.listdir(folder_path):
        fist_position = folder_name.upper().find(name.upper())
        if fist_position > -1:  # found
            # print(folder_name)
            folder_name_temp = folder_name[fist_position:fist_position +
                                           len(name)]
            if name.upper() == folder_name_temp.upper():
                result_list.append(folder_name)
    return result_list
# end of AdvancedSearch() function

# Start Open_Folder2() function
def Open_Folder2(path, name):
    os.startfile(path+chr(92)+name, 'open')
    return
# End of Open_Folder2() function

# Start ListWidget class
class ListWidget(QListWidget):    
    def Clicked1(self, item):
        Open_Folder2(design_folder_path, item.text())
          
    def Clicked2(self, item):
        Open_Folder2(external_issue_folder_path, item.text())

    def Initial(self):
        return

# End of ListWidget class
#----------------------------------------------------------------------------------------------------------------------------#
# Run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
# End
#-----------------------------------------------------------------------------------------------------------------------------#