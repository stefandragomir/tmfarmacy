

from PyQt5.QtCore           import *
from PyQt5.QtGui            import *
from PyQt5.QtChart          import *
from PyQt5.QtWidgets        import * 

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Small_Button(QPushButton):

    def __init__(self,icon_normal,icon_hover,clbk, tooltip=None):

        QPushButton.__init__(self)    

        _css  = """
            border: 0px solid gray;
            background-color: #FFFFFF;
        """ 

        self.setStyleSheet(_css)

        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover
        self.clicked.connect(clbk)

        self.setIcon(QIcon(self.icon_normal))

        self.setToolTip(tooltip)

       
    def enterEvent(self, event):
        self.setIcon(QIcon(self.icon_hover))
    

    def leaveEvent(self, event):
        self.setIcon(QIcon(self.icon_normal))


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Button(QPushButton):

    def __init__(self,text,icon_normal,icon_hover,background):

        QPushButton.__init__(self,text)
        self.icon_normal = icon_normal
        self.icon_hover  = icon_hover
        self.background  = background

        self.setStyleSheet("background-color: %s" % (self.background,))
        self.setIcon(QIcon(self.icon_normal))
        
    def enterEvent(self, event):
        if self.icon_hover:
            self.setIcon(QIcon(self.icon_hover))
            self.setStyleSheet("background-color: %s" % (self.background,))      

    def leaveEvent(self, event):
        if self.icon_hover:
            self.setIcon(QIcon(self.icon_normal))
            self.setStyleSheet("background-color: %s" % (self.background,))

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_TextEdit(QTextEdit):

    def __init__(self,label=""):

        QTextEdit.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_PopUp(QMessageBox):

    def __init__(self,title,txt,msgtype="information"):

        QMessageBox.__init__(self)

        self.txt     = txt
        self.title   = title
        self.msgtype = msgtype

        self.draw_gui()

        self.exec_()

    def draw_gui(self):

        self.setWindowTitle(self.title)
        self.resize(400,40)
        self.setFixedSize(400,40)
        self.setStyleSheet("background-color: #ffffff")
        self.setText(self.txt)
        self.setWindowModality(Qt.ApplicationModal)

        if self.msgtype == "question":
            self.setIcon(QMessageBox.Question)
        else:
            if self.msgtype == "information":
                self.setIcon(QMessageBox.Information)
            else:
                if self.msgtype == "warning":
                    self.setIcon(QMessageBox.Warning)
                else:
                    if self.msgtype == "critical":
                        self.setIcon(QMessageBox.Critical)
                    else:
                        self.setIcon(QMessageBox.NoIcon)

        self.setStandardButtons(QMessageBox.Ok)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Tree(QTreeWidget):

    def __init__(self,parent=None,usefind=False):

        QTreeWidget.__init__(self)

        self.parent       = parent 
        self.setRootIsDecorated(True)
        self.setHeaderHidden(True)  

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Tab(QTabWidget):

    def __init__(self):

        QTabWidget.__init__(self)

    def add_tab(self,label):

        _widget = QWidget()

        self.addTab(_widget,label)

        return _widget

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Label(QLabel):

    def __init__(self,txt=""):

        QLabel.__init__(self,txt)

        self.setWordWrap(True)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_RadioButton(QRadioButton):

    def __init__(self,label):

        QRadioButton.__init__(self,label)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_CheckBox(QWidget):

    def __init__(self,label):

        QWidget.__init__(self)

        self.checkbox = QCheckBox()
        self.label    = QLabel(label)
        self.label.setWordWrap(True)

        self.main_layout = QHBoxLayout()        
        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Stack(QStackedWidget):

    def __init__(self):

        QStackedWidget.__init__(self)

