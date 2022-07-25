import time
import os
from PyQt5.QtWidgets import (QDialog,QDesktopWidget,QLabel,QLineEdit, QCheckBox,
                             QGridLayout, QGroupBox, QPushButton, QWidget,QMessageBox,QStackedWidget)
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

class User_Manage(QDialog):

    def __init__(self):
        super().__init__()
        self.title = '登录'
        self.setWindowTitle(self.title)
        self.setGeometry(30, 30, 400, 400)
        self.widgets = {}
        self.all_user_dict = {}
        self.center()
        self.create_widget_layout()
        self.filename = "./res/user.png"
        self.folder_path = "./data"
        self.all_user_file = "./data/user.txt"
        self.login_user = ""

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()

        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_widget_layout(self):

        self.stackedWidget = QStackedWidget()

        # login
        self.login_widget = QWidget()
        self.create_login_widget()
        self.create_login_tip_widget()

        login_layout = QGridLayout(self.login_widget)
        login_layout.addWidget(self.login_box, 0,0,1,1)
        login_layout.addWidget(self.logup_tip_box, 1, 0, 1, 1)

        # logup
        self.logup_widget = QWidget()
        self.create_logup_widget()
        logup_layout = QGridLayout(self.logup_widget)
        logup_layout.addWidget(self.logup_box, 0,0,1,1)

        # addwidget
        self.stackedWidget.addWidget(self.login_widget)
        self.stackedWidget.addWidget(self.logup_widget)
        self.stackedWidget.setCurrentWidget(self.login_widget)

        #mainlayout
        main_layout = QGridLayout(self)
        main_layout.addWidget(self.stackedWidget,0,0,1,1)


    def create_login_widget(self):

        self.login_box = QGroupBox("")

        image_Label = QLabel()
        pixmap = QPixmap("./res/user.png")
        image_Label.setPixmap(pixmap)  # 在label上显示图片
        image_Label.setScaledContents(True)
        image_Label.setStyleSheet("background-color:rgb(200,200,200);")

        user_edit = self.create_lineEdit([12,200,30],"用户名")
        passwd_edit = self.create_lineEdit([12,200,30],"密码")
        passwd_edit.setEchoMode(QLineEdit.Password)

        login_button = self.create_button("登录",[12,200,30])
        login_button.clicked.connect(self.login_request)

        layout = QGridLayout()
        layout.addWidget(image_Label,0,0,3,1)
        layout.addWidget(user_edit, 3,0,1,1)
        layout.addWidget(passwd_edit, 4,0,1,1)
        layout.addWidget(login_button, 5, 0, 1, 1)

        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(12)

        self.login_box.setLayout(layout)
        self.widgets["login_box"] = [user_edit,passwd_edit,login_button]

    def create_login_tip_widget(self):
        self.logup_tip_box = QGroupBox("")

        label = QLabel()
        label.setText("没有账户吗?")
        button = QPushButton()
        button.setText("创建新账户")
        button.clicked.connect(self.create_account)

        layout = QGridLayout()
        layout.addWidget(label, 0,0,1,1)
        layout.addWidget(button,0,1,1,1)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.logup_tip_box.setLayout(layout)
        self.widgets["logup_tip_box"] = [label, button]

    def create_logup_widget(self):

        self.logup_box = QGroupBox("")
        user_edit = self.create_lineEdit([12, 200, 30], "用户名")
        passwd_edit_1 = self.create_lineEdit([12, 200, 30], "密码")
        passwd_edit_2 = self.create_lineEdit([12, 200, 30], "重新输入密码")
        passwd_edit_1.setEchoMode(QLineEdit.Password)
        passwd_edit_2.setEchoMode(QLineEdit.Password)

        logup_button = self.create_button("注册", [12, 200, 30])
        logup_button.clicked.connect(self.logupButton_click)

        return_button = self.create_button("返回登录界面", [12, 200, 30])
        return_button.clicked.connect(self.return_button_click)

        layout = QGridLayout()
        layout.addWidget(user_edit,0,0,1,1)
        layout.addWidget(passwd_edit_1,1,0,1,1)
        layout.addWidget(passwd_edit_2,2,0,1,1)
        layout.addWidget(logup_button,3,0,1,1)
        layout.addWidget(return_button, 4, 0, 1, 1)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(13)

        self.logup_box.setLayout(layout)
        self.widgets["logup_box"] = [user_edit, passwd_edit_1, passwd_edit_2,logup_button]

    def create_lineEdit(self,sizeList,text):
        edit = QLineEdit()
        font = PyQt5.QtGui.QFont()
        font.setPointSize(sizeList[0])
        edit.setFont(font)
        edit.setPlaceholderText(text)
        edit.setMaximumSize(sizeList[1], sizeList[2])
        return edit

    def create_check_box(self, text, sizeList):
        box = QCheckBox()
        box.setText(text)
        font = PyQt5.QtGui.QFont()
        font.setPointSize(sizeList[0])
        box.setFont(font)
        return box

    def create_button(self,text,sizeList):
        button = QPushButton()
        button.setText(text)
        font = PyQt5.QtGui.QFont()
        font.setPointSize(sizeList[0])
        button.setFont(font)
        button.setMaximumSize(sizeList[1], sizeList[2])
        return button

    def login_request(self):
        user_text = str(self.widgets["login_box"][0].text()).strip()
        passwd_text = str(self.widgets["login_box"][1].text()).strip()

        #判断用户名不为中文
        if(self.is_Chinese(user_text) or self.is_Chinese(passwd_text)):
            QMessageBox.warning(self, '警告', '不能使用中文字符 !')
            self.widgets["login_box"][0].clear()
            self.widgets["login_box"][1].clear()
            return

        #获取用户字典
        self.get_user_passwd_dict()

        #判断密码正确
        if user_text in self.all_user_dict:
            if passwd_text == self.all_user_dict[user_text]:
                self.login_user = user_text
                self.accept()
            else:
                QMessageBox.warning(self, '警告', '密码输入不正确，请重新输入密码！')
                self.widgets["login_box"][1].clear()
        else:
            QMessageBox.warning(self, '警告', '没有这个用户信息，请尝试新建用户！')
            self.widgets["login_box"][0].clear()
            self.widgets["login_box"][1].clear()
            self.stackedWidget.setCurrentWidget(self.logup_widget)

    def create_account(self):
        self.title = "注册"
        self.setWindowTitle(self.title)
        self.stackedWidget.setCurrentWidget(self.logup_widget)
        self.widgets["login_box"][0].clear()
        self.widgets["login_box"][1].clear()

    def logupButton_click(self):
        user_text = str(self.widgets["logup_box"][0].text()).strip()
        passwd_text_1 = str(self.widgets["logup_box"][1].text()).strip()
        passwd_text_2 = str(self.widgets["logup_box"][2].text()).strip()

        if (user_text == "") or (passwd_text_1 == "") or (passwd_text_2 == ""):
            QMessageBox.warning(self, '警告', '不能输入空字符！')
            return

        # 判断用户名不为中文
        if (self.is_Chinese(user_text) or self.is_Chinese(passwd_text_1) or self.is_Chinese(passwd_text_2)):
            QMessageBox.warning(self, '警告', '不能使用中文字符!')
            self.widgets["logup_box"][0].clear()
            self.widgets["logup_box"][1].clear()
            self.widgets["logup_box"][2].clear()
            return

        if(passwd_text_1!=passwd_text_2):
            QMessageBox.warning(self, '警告', '两次输入的密码不同，请重新输入!')
            self.widgets["logup_box"][1].clear()
            self.widgets["logup_box"][2].clear()
            return

        # get user dict
        self.get_user_passwd_dict()
        for key in self.all_user_dict.keys():
            if key == user_text:
                QMessageBox.warning(self, '警告', f' {key} 用户存在, 请重新创建一个新的用户！')
                self.widgets["logup_box"][0].clear()
                return

        tip_message = QMessageBox.information(self, '警告', '是否创建这个用户 ?', QMessageBox.Yes|QMessageBox.No)
        if tip_message == QMessageBox.Yes:
            self.check_folder()
            with open(self.all_user_file, "a") as fp:
                fp.writelines(user_text + ":" + passwd_text_1 + "\n")
            fp.close()
            time.sleep(1)
            return_tips_message = QMessageBox.information(self, '提示', '用户创建成功，是否返回登录界面 ?',
                                                  QMessageBox.Yes | QMessageBox.No)

            if return_tips_message == QMessageBox.Yes:
                self.title = "登录"
                self.setWindowTitle(self.title)
                self.stackedWidget.setCurrentWidget(self.login_widget)

                self.widgets["logup_box"][0].clear()
                self.widgets["logup_box"][1].clear()
                self.widgets["logup_box"][2].clear()
        else:
            return

    def return_button_click(self):
        self.title = "登录"
        self.setWindowTitle(self.title)
        self.stackedWidget.setCurrentWidget(self.login_widget)
        self.widgets["logup_box"][0].clear()
        self.widgets["logup_box"][1].clear()
        self.widgets["logup_box"][2].clear()

    def get_user_passwd_dict(self):
        self.all_user_dict = {}
        self.check_folder()

        with open(self.all_user_file, "r") as fp:
            raw_data = fp.readlines()

        for data in raw_data:
            index = data.find(":")
            user = data[:index].strip()
            passwd = data[index+1:].strip()
            self.all_user_dict[user] = passwd
        fp.close()



    def is_Chinese(self,word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def check_folder(self):

        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
            fp = open(self.all_user_file, "w")
            fp.close()

        if not os.path.exists(self.all_user_file):
            fp = open(self.all_user_file, "w")
            fp.close()





if __name__ == '__main__':
    test = User_Manage()
    test.show()
