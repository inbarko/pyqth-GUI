import os
import sys
import psutil

from datetime import date

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTreeWidgetItem, QTreeWidget, \
    QTreeWidgetItemIterator
from ui_mainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt
from subprocess import Popen
import names
import threading



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_Path = []
        self.browse.clicked.connect(self.browsedef)
        self.runButton.clicked.connect(self.runTest)
        self.logsBtn.clicked.connect(self.logTest)
        self.unselectBtn.clicked.connect(self.unSelectAll)
        self.selectBtn.clicked.connect(self.selectAll)
        self.path_dir = "C:/Users/inbar/code/bootcamp/CrmFinal/"
        self.stopBtn.clicked.connect(self.stop)
        self.checked = []
        self.process = ""

    def random_name(self):
        rand_name = names.get_full_name()
        self.pushButton_2.setText(rand_name)
        print(self.pushButton_2.text())

    def browsedef(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        filterjs = "js(*.js)"

        current_Path = QFileDialog.getOpenFileNames(self, directory=self.path_dir, filter=filterjs)
        if current_Path:
            current_Path = current_Path[0]
            print(current_Path[0])
            print(len(current_Path))
            for i in range(len(current_Path)):
                current_Path[i] = os.path.basename(current_Path[i])
            self.current_Path = current_Path[0]

        self.treeWidget.setHeaderHidden(True)
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0, "MyProject")
        for i in range(len(current_Path)):
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, current_Path[i])
            child.setCheckState(0, Qt.Unchecked)
        self.runButton.setEnabled(True)
        self.selectBtn.setEnabled(True)
        self.unselectBtn.setEnabled(True)
        self.browse.setEnabled(False)

    def runTest(self):
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        print(iterator)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0):
                self.checked.append(item.text(0))
                print(item.text(0))
            iterator += 1
        print(self.checked)
        self.runButton.setEnabled(False)
        self.unselectBtn.setEnabled(False)
        self.selectBtn.setEnabled(False)
        self.treeWidget.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.logsBtn.setEnabled(True)

        x = threading.Thread(target=self.runProcess)
        x.start()

    def runProcess(self):
        for test in self.checked:
            self.process = Popen(['node', self.path_dir + test],shell=True)
            self.process.communicate()

        self.treeWidget.setEnabled(True)
        self.browse.setEnabled(True)
        self.logsBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)




    def logTest(self):
        filtertxt = "txt(*.log)"
        today = date.today()
        newToday = today.strftime("%d.%m.%Y")
        newToday = newToday.replace(" ", "")
        path_log = "C:/Users/inbar/code/bootcamp/allTheTests/" + newToday+"/TestResults.log"
        print(path_log)
        path_log=path_log.replace(" ","")
        print(path_log)
        the_file = open(path_log)
        logtext = the_file.read()
        print(logtext)
        self.textBrowser.append(logtext)

    def unSelectAll(self):
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        iterator += 1
        while iterator.value():
            item = iterator.value()
            if item.checkState(0):
                item.setCheckState(0, Qt.Unchecked)
            iterator += 1

    def selectAll(self):
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        iterator += 1
        while iterator.value():
            item = iterator.value()
            item.setCheckState(0, Qt.Checked)
            iterator += 1

    def stop(self):
        process = psutil.Process(self.process.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()





app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
layout = QtWidgets.QVBoxLayout(window)
window.show()
sys.exit(app.exec_())
