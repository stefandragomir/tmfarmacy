
import sip

from PyQt5.QtCore              import *
from PyQt5.QtGui               import *
from PyQt5.QtChart             import *
from PyQt5.QtWidgets           import * 
from pharm_icons.pharm_icons   import Pharm_Pixmap

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

    def __init__(self,text):

        QWidget.__init__(self)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("color: #b1b1b1")

        self.text     = QTextEdit()
        self.text.setPlainText(text)
        self.text.setReadOnly(True)

        self.set_text_normal()
        
        self.main_layout = QHBoxLayout()   
        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addWidget(self.text)

        self.setLayout(self.main_layout)

    def hide_check(self):

        self.checkbox.setEnabled(False)

    def show_check(self):

        self.checkbox.setEnabled(True)

    def register_checkbox_clbk(self,clbk):

        self.checkbox.stateChanged.connect(clbk)

    def set_check_state(self,state):

        if state:
            self.checkbox.setCheckState(Qt.Checked)
        else:
            self.checkbox.setCheckState(Qt.Unchecked)

    def set_text(self,text):

        self.text.setPlainText(text)                                                                                       

    def set_text_incorrect(self):

        self.text.setStyleSheet("font-size: 21px; font-weight: normal; border: 2px solid #e81a1a;")

    def set_text_corect(self):

        self.text.setStyleSheet("font-size: 21px; font-weight: normal;  border: 2px solid #37e64b;")

    def set_text_normal(self):

        self.text.setStyleSheet("font-size: 21px; font-weight: normal; border: 1px solid #ffffff;")


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Stack(QStackedWidget):

    def __init__(self):

        QStackedWidget.__init__(self)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_WDG_Plot_StackedBar_Periods(QObject):

    draw_sgn  = pyqtSignal(list) 
    clear_sgn = pyqtSignal()

    def __init__(self,parent=None):

        QObject.__init__(self)

        self.chart            = QChart()
        self.chart_view       = QChartView(self.chart)    
        self.series           = QStackedBarSeries()
        self._title           = "" 
        self._values          = [[[]]] 
        self._y_labels        = [""] 
        self._y_label_colors  = ["#000000"] 
        self._x_labels        = [""] 
        self._y_labels_vis    = [True]
        self.has_values       = False
        self.parent           = parent

        self.__draw_values(self._values)

        self.draw_sgn.connect(self.__draw_values)
        self.clear_sgn.connect(self.clear)

    def clear(self):

        if self.chart.series() != []:

            self.chart.removeSeries(self.series)

    def draw(self,title,values,y_labels,y_label_colors,x_labels):

        self._title           = title
        self._values          = values
        self._y_labels        = y_labels
        self._y_label_colors  = y_label_colors
        self._x_labels        = x_labels
        self._y_labels_vis    = [True] * len(y_labels)

        self.__draw_values(self._values)

    def __draw_values(self,values):

        self.has_values = True

        self.series  = QStackedBarSeries()
        _x_axis      = QBarCategoryAxis()
        _barsets     = []

        for _index in range(len(self._y_labels)):

            _barset = QBarSet(self._y_labels[_index])
            _barset.setColor(QColor(self._y_label_colors[_index]))
            _barsets.append(_barset)

            for _value in values[_index]:

                _barsets[-1].append(_value)

        for _barset in _barsets:

            self.series.append(_barset)

        self.chart.addSeries(self.series)
        self.chart.setTitle(self._title)        
        _x_axis.append(self._x_labels)
        _x_axis.setLabelsAngle(-90)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(_x_axis, self.series)
        self.chart.setAnimationOptions(QChart.NoAnimation)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.__register_hover() 

    def __register_hover(self):

        self.series.hovered.connect(self.__clbk_bar_hover)
 
    def __clbk_bar_hover(self,status,index,barset):

        if status:

            _total = 0

            for _value in self._values:

                _total += _value[index]

            _x_label = self._x_labels[index]
            _y_label = barset.label()
            _value   = barset.at(index)

            _point = self.chart_view.mapFromGlobal(QCursor.pos());

            _x = _point.x()
            _y = _point.y()

            self.hover_rect = QGraphicsRectItem(self.chart)
            self.hover_rect.setBrush(QBrush(QColor("#f9ec9f")))
            self.hover_rect.setRect(_x, _y, 120, 60)  

            self.hover_txt  = QGraphicsTextItem (self.hover_rect)  
            self.hover_txt.setPos(_x, _y,)    
            self.hover_txt.setPlainText("%s\n%s\n%s\nTotal: %s" % (_y_label,_value,_x_label,_total))
            self.hover_rect.setZValue(10)

        self.hover_rect.setVisible(status)

    def __clbk_marker_hovered(self, status):

        if status:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
