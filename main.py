import random
import sys
sys.path.append('./')
from typing import List, Any
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, \
    QTableWidgetItem, QFileDialog
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Slot, Qt
from gui import Ui_start, Ui_visual, Ui_testrun
from lib.generateSample import color_enum, gen, appendgen, shuffle
from openpyxl import Workbook


class SampleData:
    """这是真正的数据接口类"""

    def __init__(self):
        self.name = None
        self.testone = dict()
        self.testtwo = dict()
        self.testthree = dict()


class SampleDataInterface:
    data = SampleData()
    """
    这是一个测试数据样本信息的接口类
    它的作用就是抽象出接口，使得几个Test子类共享变量
    """

    def __init__(self):
        self.data = data


class TestTask:
    """
    这是一个基类，关于收集不同测试类的共性问题
    """

    def __init__(self):
        self.gui = None
        self.input_data = list()
        self.input_order = list()
        self.output_data = list()

    def generate_input(self):
        raise NotImplementedError

    def load_gui(self, gui_object):
        self.gui = gui_object

    def init(self):
        raise NotImplementedError

    def result(self):
        self.gui.data.testone['input_data'] = self.input_data
        self.gui.data.testone['input_order'] = self.input_order
        self.gui.data.testone['output_data'] = self.output_data


class TestOne(TestTask):

    def __init__(self):
        super().__init__()
        self.color = None
        self.test_set = None
        self.loop = 1
        self.count = 4
        self.currentindex = 1
        self.tmp_data = list()

    def init(self):
        self.loop = 1
        self.count = 4
        self.currentindex = 1
        self.tmp_data = list()
        self.gui.ui.buttonGroup.setId(self.gui.ui.radioButton, 0)
        self.gui.ui.buttonGroup.setId(self.gui.ui.radioButton_2, 1)
        self.gui.ui.buttonGroup.setId(self.gui.ui.radioButton_3, 2)
        self.gui.ui.bt_submit.clicked.connect(self.bt_slot)
        self.input_data = self.generate_input()
        self.tmp_data = gen(self.input_data)
        self.next()

    def bt_slot(self):
        print(self.loop)
        if self.gui.ui.buttonGroup.checkedButton():
            self.output_data.append(self.gui.ui.buttonGroup.
                                    checkedId())
            self.result()
            if self.currentindex == self.count:
                if self.loop == 2:
                    self.gui.ui.stackedWidget.setCurrentIndex(1)
                else:
                    self.loop = 2
                    self.gui.ui.group_num.setText('This 2 group')
                    self.currentindex = 1
                    tmp = self.generate_input()
                    [self.input_data.append(i) for i in tmp]
                    self.tmp_data = gen(tmp)
                    self.next()
            else:
                self.currentindex += 1
                self.next()
        else:
            msgBox = QMessageBox.warning(self.gui, str("Warning"),
                                         str("No button selected.\n"
                                             "Please clicked one "
                                             "button"))

    def generate_input(self):
        # 生成冷色调图像
        max_color = 100
        if self.loop == 1:
            max_color = 100
        else:
            max_color = 225
        red_start = int(random.uniform(0, max_color))
        green_start = int(random.uniform(0, max_color))
        blue_start = int(random.uniform(0, max_color))
        start = [red_start, green_start, blue_start]
        step = [5, 5, 5]
        color_set = color_enum(start, step, 5)
        first = color_set[0]
        other = color_set[1:]
        other, index = shuffle(other)
        test_list = list()
        for i, item in enumerate(other):
            if random.random() > 0.5:
                test_item = (item, first)
                self.input_order.append([index[i], 0])
            else:
                test_item = (first, item)
                self.input_order.append([0, index[i]])
            test_list.append(test_item)
        return test_list

    def next(self):
        first_item = next(self.tmp_data)
        self.gui.ui.img_1.setStyleSheet("background-color: "
                                        + first_item[0])
        self.gui.ui.img_2.setStyleSheet("background-color: "
                                        + first_item[1])

    def result(self):
        tmp = ['same' if i == 0 else i for i in self.output_data]
        tmp = ['left' if i == 1 else i for i in tmp]
        tmp = ['right' if i == 2 else i for i in tmp]
        self.gui.data.testone['input_data'] = self.input_data
        self.gui.data.testone['input_order'] = self.input_order
        self.gui.data.testone['output_data'] = tmp

    def check_process(self):
        if len(self.output_data) == 8:
            return True
        else:
            return False


class TestTwo(TestTask):
    def __init__(self):
        super().__init__()
        self.tmp_data = None
        self.loop = 1

    def generate_input(self):
        if self.loop == 1:
            max_color = 200
            step = [12, 12, 12]
        elif self.loop == 2:
            max_color = 223
            step = [8, 8, 8]
        else:
            max_color = 243
            step = [3, 3, 3]
        red_start = int(random.uniform(0, max_color))
        green_start = int(random.uniform(0, max_color))
        blue_start = int(random.uniform(0, max_color))
        start = [red_start, green_start, blue_start]
        color_set = color_enum(start, step, 5)
        color_set, index = shuffle(color_set)
        self.input_order.append(index)
        return color_set

    def init(self):
        self.loop = 1
        self.gui.ui.bt_submit_2.clicked.connect(self.bt_slot)
        self.tmp_data = self.generate_input()
        self.input_data.append(self.tmp_data)
        self.next()

    def bt_slot(self):
        if not self.checkinput():
            return False
        else:
            self.output_data.append(self.appendresult())
            self.result()
            self.clear()
            if self.loop == 1:
                self.loop = 2
                self.tmp_data = self.generate_input()
                self.input_data.append(self.tmp_data)
                self.gui.ui.group_num_2.setText('This 2 group')
                self.next()
            elif self.loop == 2:
                self.loop = 3
                self.tmp_data = self.generate_input()
                self.input_data.append(self.tmp_data)
                self.gui.ui.group_num_2.setText('This 3 group')
                self.next()
            elif self.loop == 3:
                self.gui.ui.stackedWidget.setCurrentIndex(2)

    def next(self):
        self.gui.ui.textEdit.setStyleSheet("background-color: "
                                           + self.tmp_data[0])
        self.gui.ui.textEdit_2.setStyleSheet("background-color: "
                                             + self.tmp_data[1])
        self.gui.ui.textEdit_3.setStyleSheet("background-color: "
                                             + self.tmp_data[2])
        self.gui.ui.textEdit_4.setStyleSheet("background-color: "
                                             + self.tmp_data[3])
        self.gui.ui.textEdit_5.setStyleSheet("background-color: "
                                             + self.tmp_data[4])

    def clear(self):
        self.gui.ui.textEdit.clear()
        self.gui.ui.textEdit_2.clear()
        self.gui.ui.textEdit_3.clear()
        self.gui.ui.textEdit_4.clear()
        self.gui.ui.textEdit_5.clear()

    def appendresult(self):
        tmp = list()
        tmp.append(self.gui.ui.textEdit.toPlainText())
        tmp.append(self.gui.ui.textEdit_2.toPlainText())
        tmp.append(self.gui.ui.textEdit_3.toPlainText())
        tmp.append(self.gui.ui.textEdit_4.toPlainText())
        tmp.append(self.gui.ui.textEdit_5.toPlainText())
        return tmp

    def checkinput(self):
        if self.gui.ui.textEdit.toPlainText() == '' or \
                self.gui.ui.textEdit_2.toPlainText() == '' or \
                self.gui.ui.textEdit_3.toPlainText() == '' or \
                self.gui.ui.textEdit_4.toPlainText() == '' or \
                self.gui.ui.textEdit_5.toPlainText() == '':
            msgBox = QMessageBox.warning(self.gui, str("Warning"),
                                         str("Please input code.\n"
                                             "Please input all code! "
                                             ))
            return False
        else:
            return True

    def result(self):
        self.gui.data.testtwo['input_data'] = self.input_data
        self.gui.data.testtwo['input_order'] = self.input_order
        self.gui.data.testtwo['output_data'] = self.output_data
        print(self.gui.data.testtwo)

    def check_process(self):
        if len(self.output_data) == 3:
            return True
        else:
            return False


class TestThree(TestTask):
    def __init__(self):
        super().__init__()
        self.mix_data = None
        self.tmp_data = None
        self.loop = 1

    def generate_input(self):
        if self.loop == 1:
            max_color = 200
            step = [12, 12, 12]
        elif self.loop == 2:
            max_color = 223
            step = [8, 8, 8]
        else:
            max_color = 243
            step = [3, 3, 3]
        red_start = int(random.uniform(0, max_color))
        green_start = int(random.uniform(0, max_color))
        blue_start = int(random.uniform(0, max_color))
        start = [red_start, green_start, blue_start]
        color_set = color_enum(start, step, 5)
        mix_set = color_enum(start, [i + 2 for i in step], 10)
        random.shuffle(mix_set)
        color_set, index = shuffle(color_set)
        self.input_order.append(index)
        return color_set, mix_set

    def init(self):
        self.loop = 1
        self.gui.ui.bt_submit_3.clicked.connect(self.bt_slot)
        self.tmp_data, self.mix_data = self.generate_input()
        self.input_data.append(self.tmp_data)
        self.next()

    def bt_slot(self):
        if not self.checkinput():
            return False
        else:
            self.output_data.append(self.appendresult())
            self.result()
            self.clear()
            if self.loop == 1:
                self.loop = 2
                self.tmp_data, self.mix_data = self.generate_input()
                self.input_data.append(self.tmp_data)
                self.gui.ui.group_num_3.setText('This 2 group')
                self.next()
            elif self.loop == 2:
                self.loop = 3
                self.tmp_data, self.mix_data = self.generate_input()
                self.input_data.append(self.tmp_data)
                self.gui.ui.group_num_3.setText('This 3 group')
                self.next()
            else:
                msgBox = QMessageBox.warning(self.gui, str("Warning"),
                                             str("Test over, please "
                                                 "check the results! "
                                                 ))

    def next(self):
        # 排序色块填充
        self.gui.ui.textEdit_6.setStyleSheet("background-color: "
                                             + self.tmp_data[0])
        self.gui.ui.textEdit_12.setStyleSheet("background-color: "
                                              + self.tmp_data[1])
        self.gui.ui.textEdit_16.setStyleSheet("background-color: "
                                              + self.tmp_data[2])
        self.gui.ui.textEdit_13.setStyleSheet("background-color: "
                                              + self.tmp_data[3])
        self.gui.ui.textEdit_10.setStyleSheet("background-color: "
                                              + self.tmp_data[4])
        # 混合色块填充
        self.gui.ui.textEdit_7.setStyleSheet("background-color: "
                                             + self.mix_data[0])
        self.gui.ui.textEdit_8.setStyleSheet("background-color: "
                                             + self.mix_data[1])
        self.gui.ui.textEdit_9.setStyleSheet("background-color: "
                                             + self.mix_data[2])
        self.gui.ui.textEdit_14.setStyleSheet("background-color: "
                                              + self.mix_data[3])
        self.gui.ui.textEdit_11.setStyleSheet("background-color: "
                                              + self.mix_data[4])
        self.gui.ui.textEdit_15.setStyleSheet("background-color: "
                                              + self.mix_data[5])
        self.gui.ui.textEdit_17.setStyleSheet("background-color: "
                                              + self.mix_data[6])
        self.gui.ui.textEdit_18.setStyleSheet("background-color: "
                                              + self.mix_data[7])
        self.gui.ui.textEdit_19.setStyleSheet("background-color: "
                                              + self.mix_data[8])
        self.gui.ui.textEdit_20.setStyleSheet("background-color: "
                                              + self.mix_data[9])

    def clear(self):
        self.gui.ui.textEdit_6.clear()
        self.gui.ui.textEdit_12.clear()
        self.gui.ui.textEdit_16.clear()
        self.gui.ui.textEdit_13.clear()
        self.gui.ui.textEdit_10.clear()

    def appendresult(self):
        tmp = list()
        tmp.append(self.gui.ui.textEdit_6.toPlainText())
        tmp.append(self.gui.ui.textEdit_12.toPlainText())
        tmp.append(self.gui.ui.textEdit_16.toPlainText())
        tmp.append(self.gui.ui.textEdit_13.toPlainText())
        tmp.append(self.gui.ui.textEdit_10.toPlainText())
        return tmp

    def checkinput(self):
        if self.gui.ui.textEdit_6.toPlainText() == '' or \
                self.gui.ui.textEdit_12.toPlainText() == '' or \
                self.gui.ui.textEdit_16.toPlainText() == '' or \
                self.gui.ui.textEdit_13.toPlainText() == '' or \
                self.gui.ui.textEdit_10.toPlainText() == '':
            msgBox = QMessageBox.warning(self.gui, str("Warning"),
                                         str("Please input code.\n"
                                             "Please input all code! "
                                             ))
            return False
        else:
            return True

    def result(self):
        self.gui.data.testthree['input_data'] = self.input_data
        self.gui.data.testthree['input_order'] = self.input_order
        self.gui.data.testthree['output_data'] = self.output_data
        print(self.gui.data.testthree)

    def check_process(self):
        if len(self.output_data) == 3:
            return True
        else:
            return False


class TestSetInterface:
    test_set = [
        TestOne(),
        TestTwo(),
        TestThree()
    ]


class TestGui(QWidget, SampleDataInterface):
    def __init__(self):
        super().__init__()
        self.test_type = 1
        self.ui = Ui_testrun()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.run()

    def run(self):
        for i in TestSetInterface.test_set:
            i.load_gui(self)
            i.init()

    def keyPressEvent(self, event) -> None:
        """
        定义键盘快捷键，回车键等同于点确定
        :param event: pyside6 事件
        """
        if event.key() == Qt.Key_Return:
            if self.ui.stackedWidget.currentIndex() == 0:
               self.ui.bt_submit.clicked.emit()
            else:
               self.ui.bt_submit_2.clicked.emit()

    def check_process(self):
        for i in TestSetInterface.test_set:
            if not i.check_process():
                return False
        return True


class RegisterGui(QWidget, SampleDataInterface):
    def __init__(self):
        super().__init__()
        self.name = None
        self.ui = Ui_start()
        self.ui.setupUi(self)
        self.ui.bt_start.clicked.connect(self.bt_submit)

    def bt_submit(self):
        self.data.name = self.ui.lineEdit.text()

    def keyPressEvent(self, event) -> None:
        """
        定义键盘快捷键，回车键等同于点确定
        :param event: pyside6 事件
        """
        if event.key() == Qt.Key_Return:
            self.ui.bt_start.clicked.emit()


class Visual(QWidget, SampleDataInterface):
    def __init__(self):
        super().__init__()
        self.wb = Workbook()
        self.wb.create_sheet(index=0, title='sheet1')
        self.ui = Ui_visual()
        self.ui.setupUi(self)
        self.ui.ep.clicked.connect(self.ep_slot)

    def ep_slot(self):
        file = QFileDialog.getSaveFileName(self, str("Save File"))
        filename = file[0]
        self.wb.save(filename)

    def vi(self):
        # 创建excel文件
        ws = self.wb.active

        row1 = len(self.data.testone['input_data'])
        row2 = len(self.data.testtwo['input_data'])
        row3 = len(self.data.testthree['input_data'])
        self.ui.tb.setColumnCount(3)
        self.ui.tb.setRowCount(row1 + row2 + row3)

        for i in range(row1):
            input_color = str(self.data.testone['input_data'][i])
            input_order = str(self.data.testone['input_order'][i])
            output = str(self.data.testone['output_data'][i])
            color_item = QTableWidgetItem(input_color)
            order_item = QTableWidgetItem(input_order)
            output_item = QTableWidgetItem(output)
            self.ui.tb.setItem(i, 0, color_item)
            self.ui.tb.setItem(i, 1, order_item)
            self.ui.tb.setItem(i, 2, output_item)
            ws.append([input_color,input_order,output])

        for i in range(row2):
            # 测试2 数据可视化
            input_color = str(self.data.testtwo['input_data'][i])
            input_order = str(self.data.testtwo['input_order'][i])
            output = str(self.data.testtwo['output_data'][i])
            color_item = QTableWidgetItem(input_color)
            order_item = QTableWidgetItem(input_order)
            output_item = QTableWidgetItem(output)
            self.ui.tb.setItem(row1 + i, 0, color_item)
            self.ui.tb.setItem(row1 + i, 1, order_item)
            self.ui.tb.setItem(row1 + i, 2, output_item)
            ws.append([input_color,input_order,output])

        for i in range(row3):
            # 测试3 数据可视化
            input_color = str(self.data.testthree['input_data'][i])
            input_order = str(self.data.testthree['input_order'][i])
            output = str(self.data.testthree['output_data'][i])
            color_item = QTableWidgetItem(input_color)
            order_item = QTableWidgetItem(input_order)
            output_item = QTableWidgetItem(output)
            self.ui.tb.setItem(row1 + row2 + i, 0, color_item)
            self.ui.tb.setItem(row1 + row2 + i, 1, order_item)
            self.ui.tb.setItem(row1 + row2 + i, 2, output_item)
            ws.append([input_color,input_order,output])


class Controller:
    def __init__(self):
        """
        这是一个控制器类，用来协调各个窗口之间的交互
        regwin，testwin 用来初始化两个窗口类
        并设定好两个窗口之间的信号与槽函数
        """
        super().__init__()
        self.regwin = RegisterGui()
        self.testwin = TestGui()
        self.visualwin = Visual()
        self.regwin.ui.bt_start.clicked.connect(self.start)
        self.testwin.ui.resume.clicked.connect(self.bt_resume)
        self.testwin.ui.result.clicked.connect(self.bt_result)
        self.regwin.show()

    def bt_resume(self):
        self.testwin.data.testone = dict()
        self.testwin.data.testtwo = dict()
        self.testwin.data.testthree = dict()
        self.__init__()
        self.testwin.close()
        self.regwin.show()

    def bt_result(self):
        if not self.testwin.check_process():
            msgBox = QMessageBox.warning(self.testwin,
                                         str("Warning"),
                                         str("The tests are not "
                                             "over yet"))
        else:
            self.visualwin.vi()
            self.visualwin.show()

    @Slot()
    def start(self):
        """
        是注册窗口的槽函数，用来接受鼠标点击事件，并且打开测试页面
        """
        self.regwin.close()
        self.testwin.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Controller()

    sys.exit(app.exec())
