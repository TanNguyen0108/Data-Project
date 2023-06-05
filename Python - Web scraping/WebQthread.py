import sys
# import win32com.client as win32
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QListWidget, QCheckBox, QApplication, QProgressBar, QLabel, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QTimer
import threading

class Ui(QtWidgets.QMainWindow):
    
    e = threading.Event()
    
    def btnfunc(self):
        self.e.set()
    
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI//Web_W.ui', self) # Load the .ui file
        self.show()
        self.setFixedSize(self.size())
        self.setWindowTitle("Data Mining")
        
        # self.plainTextEdit.setPlainText("asdasd")
        
        self.pushButton_3.clicked.connect(self.start_thread)
        self.pushButton_2.clicked.connect(self.btnfunc)
            
    def start_thread(self):
        self.t = threading.Thread(target=self.Reset_to_ID1, args=( ))
        self.t.start()
        
    def Reset_to_ID1(self):
        
        # self.plainTextEdit.clear()
        
        url = self.lineEdit.text()
		#headers will have the user agent name to avoid being blocked as bot
        headers = {"User-Agent": '###########################################################################'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        mydivs = soup.find("div", { "id" : "cases" })
        sort_html = ""
        for div in mydivs:
            sort_html += str(div)
        
        soup2 = BeautifulSoup(sort_html, 'html.parser')
        
        count_item = 0
        
        #test 1
        for item in soup2.find_all(attrs={"data-id": True}) :
            # self.plainTextEdit.setPlainText(" ")
            project_id = item['data-id']
            self.label_4.setText(str(project_id))
            
            project_name = item.find('strong').string
            self.label_5.setText(project_name)
            
            self.find_href = "https://woodforgood.com/" + item.find('a', href=True)['href']
            
            print(self.find_href)
            
            c_url = self.find_href
            c_page = requests.get(c_url, headers=headers)
            c_soup = BeautifulSoup(c_page.content, 'html.parser')
            c_table_data = str(c_soup.find(class_='widget case-study-details shaded').text)
            
            self.plainTextEdit.setPlainText(self.find_href)
            
            
            c_mydivs = c_soup.find("div", { "class" : "widget case-study-details shaded" })
            c_sort_html = ""
            # print(c_mydivs)
            for div in c_mydivs:
                  c_sort_html += str(div)
                
            c_soup2 = BeautifulSoup(c_sort_html, 'html.parser')
    
            for c_item in c_soup2.findAll(class_='detail'):
                  s = str(c_item.text).split("\n")
                  for i in range(0,7):
                      if self.tableWidget.verticalHeaderItem(i).text() == s[0]:
                          self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(s[1]))
                          
            print("1")

            
            self.e.clear()
            self.e.wait()
            
            for c_item in c_soup2.findAll(class_='detail'):
                  s = str(c_item.text).split("\n")
                  for i in range(0,7):
                         self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(""))
            
            # break
                
            count_item = count_item + 1
                
        print(count_item)
        
    def myfunc(self):
        self.e.wait()
                    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_() 

      
        