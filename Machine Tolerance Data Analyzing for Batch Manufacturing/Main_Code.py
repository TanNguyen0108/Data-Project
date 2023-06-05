from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QApplication, QPushButton, QTableWidget,QTableWidgetItem,QHBoxLayout,QLabel, QMessageBox)
import os
import statistics
import pandas as pd
import numpy as np
import math

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import tempfile
from fpdf import FPDF

from io import BytesIO


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('UI//UI_WIA2.ui', self) # Load the .ui file
        
        self.setFixedSize(self.size())
        self.setWindowTitle("Measurement Tolerances Analysis")
        self.pushButton_2.clicked.connect(self.importing)
        self.pushButton_5.clicked.connect(self.Histogram)
        self.pushButton_7.clicked.connect(self.Moving_Average)
        self.pushButton_9.clicked.connect(self.Control_Chart)
        self.pushButton_4.clicked.connect(self.Pareto)
        self.pushButton_6.clicked.connect(self.PDF_Export)
        
        self.show()
        
    def importing(self):
        
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        self.label_4.setText(response[0])
    
        option = self.comboBox.currentText()
        if option == "CSV":
            self.importing_csv()
        elif option == "XML":
            self.importing_xml()
        # elif option == 2:
        #     response = self.getDirectory()
        else:
            print('Got Nothing')
            
        self.Review_data()  
        
    def importing_xml(self):
        self.re_df = pd.read_excel(self.label_4.text())
        
    def importing_csv(self):
        self.re_df = pd.read_csv(self.label_4.text())
        
    def Review_data(self):
        self.setDisabled(True)
        
        self.new_widget = QtWidgets.QWidget()
        self.new_widget.setGeometry(500, 300, 300, 250)
        # self.new_widget.setCentralWidget(self.new_widget)
        self.new_widget.setFixedSize(self.new_widget.size())
        self.layout = QVBoxLayout(self.new_widget)
        
        self.table_inputindex = QTableWidget(self.new_widget)
        self.table_inputindex.setRowCount(2)
        self.table_inputindex.setColumnCount(1)
        self.table_inputindex.setVerticalHeaderLabels(["Start Column","Start Row"])
        self.table_inputindex.setHorizontalHeaderLabels(["Input"])
        self.layout.addWidget(self.table_inputindex)
        
        self.label_title_button = QtWidgets.QLabel('Choose Control Limit Method',self.new_widget)
        self.layout.addWidget(self.label_title_button)
        
        self.button_layout = QHBoxLayout()
        
        self.button_custom = QtWidgets.QPushButton('Custom',self.new_widget)
        self.button_layout.addWidget(self.button_custom)
        self.button_auto = QtWidgets.QPushButton('LSL - USL',self.new_widget)
        self.button_layout.addWidget(self.button_auto)
        self.layout.addLayout(self.button_layout)
        
        self.label_status = QtWidgets.QLabel('Using control limit by:',self.new_widget)
        self.layout.addWidget(self.label_status)
        
        self.button_apply = QtWidgets.QPushButton('Apply',self.new_widget)
        self.layout.addWidget(self.button_apply)
        self.button_apply.hide()
        
        self.new_widget.show()
        
        self.button_custom.clicked.connect(self.click_at_subwidget_custom)
        self.button_auto.clicked.connect(self.click_at_subwidget_auto)
        self.button_apply.clicked.connect(self.enable_main_window)
        
    def click_at_subwidget_custom(self):
        self.button_apply.show()
        self.label_status.setText('Using control limit by: {}'.format(self.button_custom.text()))
        self.label_status.setStyleSheet("font-family: Arial; font-size: 12pt; font-weight: bold;")
    def click_at_subwidget_auto(self):
        self.button_apply.show()
        self.label_status.setText('Using control limit by: {}'.format(self.button_auto.text()))
        self.label_status.setStyleSheet("font-family: Arial; font-size: 12pt; font-weight: bold;")
        
    def enable_main_window(self):
        start_col = int(self.table_inputindex.item(0,0).text())
        start_row = int(self.table_inputindex.item(1,0).text())
        self.df = self.re_df.iloc[start_row:, start_col:]
        
        self.list_column = self.df.columns.values.tolist()
        
        self.new_widget.setEnabled(False)
        self.setEnabled(True)
        self.new_widget.close()
        
        self.create_button()
        self.Create_table_limit()
        self.Failure_rate()
        
    def create_button(self):
        kj = 600
        ki = 25
        bt_order = 0
        
        dict={}
        
        self.count = len(self.df.columns)
        print(self.count)
        
        row = self.count / 5
        
        for i in range(1,int(math.ceil(row)) + 1):
            for j in range(1,6):
                name_bt = self.list_column[bt_order]
                
                key = str("x"+str(bt_order))
                dict[key] = QPushButton('New Button{}'.format(bt_order),self)
                dict[key].setText(str(name_bt))
                dict[key].move(kj, ki)
                dict[key].setMinimumSize(10,10)
                kj= kj+100
                dict[key].show()
                
                bt_order = bt_order + 1
                if bt_order == self.count:
                    break
            ki= ki + 30
            kj = 600
        
        values = dict.values()
        values_list = list(values)    
        
        for button in values_list:
            button.clicked.connect(lambda checked, button=button: self.Button_Col_Method(button))
            
    def Button_Col_Method(self,button):
        self.column_index = button.text()
        self.groupBox_3.setTitle("Chart Subject: {}".format(button.text()))
        self.groupBox_3.setStyleSheet("font-family: Arial; font-size: 14pt; font-weight: bold;")
        
        #clear chart
        self.clear_plot()
        
    def Create_table_limit(self):
        # data = self.df
        self.list_col = self.df.columns.values.tolist()

        # Initialize the table widget
        self.tableWidget = QTableWidget(self)

        # Set the row and column count based on the input data
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(len(self.list_col))
        
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels([str(i_list) for i_list in self.list_col])
        self.tableWidget.setVerticalHeaderLabels(["Mean", "Upper Limit", "Lower Limit","Fail Numbers"])

        # Add the data_mean to the table widget
        j=0
        for i in self.list_col:
            try:
                x = pd.Series(self.df[i].values)
                #Skip NaN value
                non_nan_numbers = [num for num in x if not (num != num)]
                # print(statistics.mean(non_nan_numbers))
                self.tableWidget.setItem(0,j,QtWidgets.QTableWidgetItem(str(round(statistics.mean(non_nan_numbers),3))))   
            except:
                print("column pass")
            j += 1
            
        # re-data only:    
        self.Manual_Failure_rate()
        self.tableWidget.setGeometry(15, 120, 565, 140)
        self.tableWidget.show()
        
    def Histogram(self):
        self.clear_plot()
        self.canvas = FigureCanvas(Figure())
        self.MplWidget.canvas.axes.hist(self.df[self.column_index], bins=80)
        self.MplWidget.canvas.axes.set_xlabel('Ft^2')
        self.MplWidget.canvas.axes.set_title("Histogram of {}".format(self.column_index))
        self.MplWidget.canvas.draw()
        
    def Control_Chart(self):
        self.clear_plot()
        x = pd.Series(self.df[self.column_index].values)
        # Define list variable for moving ranges
        MR = [np.nan]
        # Get and append moving ranges
        i = 1
        for data in range(1, len(x)):
            MR.append(abs(x[i] - x[i-1]))
            i += 1
        # Convert list to pandas Series objects    
        MR = pd.Series(MR)
        # Concatenate mR Series with and rename columns
        data = pd.concat([x,MR], axis=1).rename(columns={0:"x", 1:"mR"})
        # Plot x and mR charts
        fig, axs = plt.subplots(2, figsize=(15,15), sharex=True)
        # x chart
        self.canvas = FigureCanvas(Figure())
        self.canvas.figure.add_subplot(212)
        self.MplWidget.canvas.axes.plot(data['x'], linestyle='-',color='black')
        self.MplWidget.canvas.axes.axhline(statistics.mean(data['x']), color='blue')
        self.MplWidget.canvas.axes.axhline(statistics.mean(data['x'])+3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128, color = 'red', linestyle = 'dashed')
        self.MplWidget.canvas.axes.axhline(statistics.mean(data['x'])-3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128, color = 'red', linestyle = 'dashed')
        self.MplWidget.canvas.axes.set_title('Individual Chart')
        self.MplWidget.canvas.axes.set(xlabel='Unit', ylabel='Value')
        self.MplWidget.canvas.draw()
        # mR chart
        self.canvas.figure.add_subplot(212)
        self.MplWidget_2.canvas.axes.plot(data['mR'], linestyle='-', color='black')
        self.MplWidget_2.canvas.axes.axhline(statistics.mean(data['mR'][1:len(data['mR'])]), color='blue')
        self.MplWidget_2.canvas.axes.axhline(statistics.mean(data['mR'][1:len(data['mR'])])+3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525, color='red', linestyle ='dashed')
        self.MplWidget_2.canvas.axes.axhline(statistics.mean(data['mR'][1:len(data['mR'])])-3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525, color='red', linestyle ='dashed')
        self.MplWidget_2.canvas.axes.set_ylim(bottom=0)
        self.MplWidget_2.canvas.axes.set_title('mR Chart')
        self.MplWidget_2.canvas.axes.set(xlabel='Unit', ylabel='Range')
        self.MplWidget_2.canvas.draw()
        # # Validate points out of control limits for x chart
        # i = 0
        # control = True
        # for unit in data['x']:
        #     if unit > statistics.mean(data['x'])+3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128 or unit < statistics.mean(data['x'])-3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128:
        #         print('Unit', i, 'out of cotrol limits!')
        #         control = False
        #     i += 1
        # if control == True:
        #     print('All points within control limits.')
            
        # # Validate points out of control limits for mR chart
        # i = 0
        # control = True
        # for unit in data['mR']:
        #     if unit > statistics.mean(data['mR'][1:len(data['mR'])])+3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525 or unit < statistics.mean(data['mR'][1:len(data['mR'])])-3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525:
        #         print('Unit', i, 'out of control limits!')
        #         control = False
        #     i += 1
        # if control == True:
        #     print('All points within control limits.')
        
    def Moving_Average(self):
        self.clear_plot()
        data = pd.Series(self.df[self.column_index].values)
        #setlimit
        index_colconv = self.df.columns.get_loc(self.column_index)
        limit_low = float(self.tableWidget.item(2,index_colconv).text())
        limit_high = float(self.tableWidget.item(1,index_colconv).text())
        defect_items = np.where((data < limit_low) | (data > limit_high))[0]
        # Define list variable for moving ranges
        # Calculate moving averages for two different window sizes
        ma_25 = data.rolling(window=25).mean()
        ma_50 = data.rolling(window=50).mean()
        ma_100 = data.rolling(window=100).mean()
        
        # Create a plot with the original data and both moving averages
        self.canvas = FigureCanvas(Figure())
        self.canvas.figure.add_subplot(211)
        self.MplWidget.canvas.axes.plot(data, label='Data with Defect Items')
        self.MplWidget.canvas.axes.scatter(defect_items, data[defect_items], color='r')
        self.MplWidget.canvas.axes.axhline(limit_low, linestyle='--', color='r')
        self.MplWidget.canvas.axes.axhline(limit_high, linestyle='--', color='r')
        # Set labels and legend
        self.MplWidget.canvas.axes.set_xlabel('Time')
        self.MplWidget.canvas.axes.set_ylabel('Your Column')
        self.MplWidget.canvas.axes.set_title('Moving Average Plot')
        self.MplWidget.canvas.axes.legend()
        # Show the plot
        self.canvas.figure.add_subplot(212)
        self.MplWidget_2.canvas.axes.plot(ma_25, label='MA (25)')
        self.MplWidget_2.canvas.axes.plot(ma_50, label='MA (50)')
        self.MplWidget_2.canvas.axes.plot(ma_100, label='MA (100)')
        self.MplWidget_2.canvas.axes.legend()
        self.MplWidget_2.canvas.axes.set_title('Moving Average')
        self.MplWidget.canvas.draw()
        self.MplWidget_2.canvas.draw()
        
    def Pareto(self):
        self.clear_plot()
        self.subject = list(self.list_col)
        self.failure_number = []
        for i in range(self.count):
            try:
                self.failure_number.append(int(self.tableWidget.item(3,i).text()))
            except:
                self.failure_number.append(0)
        
        data_pareto = {'Subject': self.subject,
                'Defects': self.failure_number}

        df_Pareto = pd.DataFrame(data_pareto)
        # sort data in descending order of defects
        df_Pareto = df_Pareto.sort_values(by=['Defects'], ascending=False)
        # calculate percentage of total defects
        df_Pareto['Percent'] = df_Pareto['Defects'].apply(lambda x: round((x/df_Pareto['Defects'].sum())*100,2))
        # calculate cumulative percentage
        df_Pareto['CumulativePercent'] = df_Pareto['Percent'].cumsum()
        # create Pareto chart
        self.canvas = FigureCanvas(Figure())
        self.canvas.figure.add_subplot(212)
        self.MplWidget.canvas.axes.bar(df_Pareto['Subject'], df_Pareto['Defects'], color='tab:red')
        tick_locations = np.arange(len(df_Pareto['Subject']))
        self.MplWidget.canvas.axes.set_xticks(tick_locations)
        self.MplWidget.canvas.axes.set_xticklabels(df_Pareto['Subject'].iloc[tick_locations], rotation=70, ha='right')
        self.MplWidget.canvas.axes.set_ylabel('Defects', color='tab:red')
        self.MplWidget.canvas.axes.tick_params(axis='y', labelcolor='tab:red')
        self.ax2 = self.MplWidget.canvas.axes.twinx()
        self.ax2.plot(df_Pareto['Subject'], df_Pareto['CumulativePercent'], color='tab:blue', marker='D', ms=7)
        self.ax2.set_ylabel('Cumulative %', color='tab:blue')
        self.ax2.tick_params(axis='y', labelcolor='tab:blue')
        self.MplWidget.canvas.draw()
        
    def Failure_rate(self):
        j=0
        try:
            for i in self.list_col:
                low = sum(1 for j_list in pd.Series(self.df[i].values) if float(j_list) > float(self.tableWidget.item(1,j).text()) )
                high = sum(1 for j_list in pd.Series(self.df[i].values) if float(j_list) < float(self.tableWidget.item(2,j).text()) )
                sum_failure = low + high
                self.tableWidget.setItem(3,j,QtWidgets.QTableWidgetItem(str(sum_failure)))
                j=j+1
        except:
            pass
    
    def Manual_Failure_rate(self):
        print(self.count)
        l_error = []
        for i_col in range(self.count):
            try:
                col_index_name = self.list_column[i_col]
                x = pd.Series(self.df[col_index_name].values)
                MR = [np.nan]
                i = 1
                for data in range(1, len(x)):
                    MR.append(abs(x[i] - x[i-1]))
                    i += 1
                MR = pd.Series(MR)
                data = pd.concat([x,MR], axis=1).rename(columns={0:"x", 1:"mR"})
                
                up_limit = round(statistics.mean(data['x'])+3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128,3)
                low_limit = round(statistics.mean(data['x'])-3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128,3)
                #assgin up limit
                self.tableWidget.setItem(1,i_col,QtWidgets.QTableWidgetItem(str(up_limit)))
                #assign low_limit
                self.tableWidget.setItem(2,i_col,QtWidgets.QTableWidgetItem(str(low_limit)))
                
                if math.isnan(up_limit):
                    l_error.append(col_index_name)
                    
            except:
                l_error.append(col_index_name)
                
        if len(l_error) == 0:
            pass
        else:
            out_warning = ', '.join(l_error)
            QMessageBox.warning(self, "Limit Warning", 
                                "Have {number} column/s with unexpected out-range value\n\nPlease check: {list_name}"
                                .format(number=len(l_error),list_name=out_warning))
            
            self.label_5.setText("Have {number} column/s with unexpected out-range value"
                                .format(number=len(l_error)))
    
    def WSWH_limit_value(self):
        #MT:
            #max:
        self.tableWidget.setItem(1,0,QtWidgets.QTableWidgetItem(str(3.530)))
        self.tableWidget.setItem(1,1,QtWidgets.QTableWidgetItem(str(3.530)))
        self.tableWidget.setItem(1,1,QtWidgets.QTableWidgetItem(str(3.530)))
        self.tableWidget.setItem(1,1,QtWidgets.QTableWidgetItem(str(3.530)))
            #min:
        self.tableWidget.setItem(2,0,QtWidgets.QTableWidgetItem(str(3.330)))
        self.tableWidget.setItem(2,1,QtWidgets.QTableWidgetItem(str(3.330)))
        self.tableWidget.setItem(2,1,QtWidgets.QTableWidgetItem(str(3.330)))
        self.tableWidget.setItem(2,1,QtWidgets.QTableWidgetItem(str(3.330)))
        #WT
            #max
        self.tableWidget.setItem(1,2,QtWidgets.QTableWidgetItem(str(7.6875)))
        self.tableWidget.setItem(1,6,QtWidgets.QTableWidgetItem(str(7.6875)))
            #min:
        self.tableWidget.setItem(2,2,QtWidgets.QTableWidgetItem(str(7.5625)))
        self.tableWidget.setItem(2,6,QtWidgets.QTableWidgetItem(str(7.5625)))
        #WB
            ##max:
        self.tableWidget.setItem(1,3,QtWidgets.QTableWidgetItem(str(3.6875)))
        self.tableWidget.setItem(1,7,QtWidgets.QTableWidgetItem(str(3.6875)))
            #min:
        self.tableWidget.setItem(2,3,QtWidgets.QTableWidgetItem(str(3.5625)))
        self.tableWidget.setItem(2,7,QtWidgets.QTableWidgetItem(str(3.5625)))
        #E1
            #max
        self.tableWidget.setItem(1,4,QtWidgets.QTableWidgetItem(str(0.75)))
        self.tableWidget.setItem(1,8,QtWidgets.QTableWidgetItem(str(0.75)))
            #min
        self.tableWidget.setItem(2,4,QtWidgets.QTableWidgetItem(str(0.625)))
        self.tableWidget.setItem(2,8,QtWidgets.QTableWidgetItem(str(0.625)))    
        #E2
            #max
        self.tableWidget.setItem(1,5,QtWidgets.QTableWidgetItem(str(3.875)))
        self.tableWidget.setItem(1,9,QtWidgets.QTableWidgetItem(str(3.875)))
            #min
        self.tableWidget.setItem(2,5,QtWidgets.QTableWidgetItem(str(3.75)))
        self.tableWidget.setItem(2,9,QtWidgets.QTableWidgetItem(str(3.75)))
        #TR
        
        #BR
        #D
        #BC
        #EC
        #CC
        #TS
        #BS
        #ST
        #w
        
    def clear_plot(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget_2.canvas.axes.clear()
        try:
            self.ax2.remove()
        except:
            pass
        self.MplWidget.canvas.draw()
        self.MplWidget_2.canvas.draw()
        
    def PDF_Export(self):
        WIDTH = 215.9
        # Create a new PDF document with "letter" size
        pdf = FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, "My PDF Document with Plot and Comment", ln=0.85, align="C")
        pdf.image("./resources/pdf_template.png", 0, 0, WIDTH)
        
        #Parato
        buffer_Pa = BytesIO()
        self.Pareto()
        self.MplWidget.canvas.axes.figure.savefig(buffer_Pa, format='png')
        buffer_Pa.seek(0)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f_Pa:
            buffer_Pa.seek(0)
            f_Pa.write(buffer_Pa.read())
        pdf.image(f_Pa.name, x=20, y=35, w=175, h=150)
        
        # Add a comment to the PDF document
        max_number_defect = max(self.failure_number)
        max_subject_deject = self.subject[self.failure_number.index(max_number_defect)]
        comment = "Based on the above pareto chart, it is shown that the size with the highest error rate is {name} with {number} defective products. However, this requires determining what defect rate level is acceptable for samples. This will depend on various factors such as the type of tight dimension, engineering require, and the industry standards.".format(name= max_subject_deject,number=max_number_defect)
        pdf.set_xy(10, 190)
        pdf.set_font("Arial", size=12)

        # Split the comment into chunks to fit in multiple lines
        lines = comment.split('\n')
        for line in lines:
            pdf.multi_cell(0, 5, line)
        
        #Chart for each dimension
        i = 0
        for self.column_index in self.list_col:
            
            pdf.add_page()
            pdf.image("./resources/pdf_template.png", 0, 0, WIDTH)
            
            pdf.set_font("Arial",'B', size=14)
            pdf.text(10, 35,"Inspection Chart for {} dimension:".format(self.column_index))
            ## import Histogram
            self.Histogram()
            buffer1 = BytesIO()
            self.MplWidget.canvas.axes.figure.savefig(buffer1, format='png')
            buffer1.seek(0)
            
            ## import Moving_Average
            self.Moving_Average()
            buffer2 = BytesIO()
            buffer3 = BytesIO()
            self.MplWidget.canvas.axes.figure.savefig(buffer2, format='png')
            buffer2.seek(0)
            self.MplWidget_2.canvas.axes.figure.savefig(buffer3, format='png')
            buffer3.seek(0)
            
            ## import Control_Chart
            self.Control_Chart()
            buffer4 = BytesIO()
            self.MplWidget_2.canvas.axes.figure.savefig(buffer4, format='png')
            buffer4.seek(0)
            
            # Save the plot images to temporary PNG files
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f1, \
                 tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f2, \
                 tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f3, \
                 tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f4:
                buffer1.seek(0)
                f1.write(buffer1.read())
                buffer2.seek(0)
                f2.write(buffer2.read())
                buffer3.seek(0)
                f3.write(buffer3.read())
                buffer4.seek(0)
                f4.write(buffer4.read())
                
            pdf.image(f1.name, x=6, y=38, w=93, h=80)
            pdf.image(f2.name, x=105, y=38, w=93,h=80)
            pdf.image(f3.name, x=6, y=115, w=93,h=80)
            pdf.image(f4.name, x=105, y=115, w=93,h=80)
            
            pdf.set_xy(10, 190)
            pdf.set_font("Arial", size=12)
            total_inspect = 800
            
            # number_failure = float(self.tableWidget.item(1,i).text()) + float(self.tableWidget.item(2,i).text())
            pdf.text(12, 195,"The mean is: {}".format(str(self.tableWidget.item(0,i).text())))
            pdf.text(12, 200,"The upper control limit is: {}".format(str(self.tableWidget.item(1,i).text())))
            pdf.text(12, 205,"The lower control limit is: {}".format(str(self.tableWidget.item(2,i).text())))
            pdf.text(12, 210,"Total {defect} items out of controll limit in {total} inspected items".format(defect = str(self.tableWidget.item(3,i).text()),total = total_inspect))
            pdf.text(12, 215,"The defect rate is {defect}/{total} = {percent}%."
                     .format(
                         defect=str(self.tableWidget.item(3,i).text()),total=total_inspect,percent = round(float(self.tableWidget.item(3,i).text())*100/float(total_inspect),3)
                     ))
            
            i= i+1
            self.close_plot()
            #break  
        
        # Save the PDF document to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            pdf.output(f.name)
        # Open the PDF file using the default application for PDF files
        os.startfile(f.name)
        
    def close_plot(self):
        plt.close('all')
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_() 
        
