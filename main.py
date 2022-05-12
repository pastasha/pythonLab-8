
import psycopg2,sys

from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout, QTableWidget, QGroupBox, QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox,QCheckBox,QStyledItemDelegate)

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return
    
class MainWindow (QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Program")
        self.vbox = QVBoxLayout(self)
        self.tabs=QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn=psycopg2.connect(database="service_db",
                      user="postgres",
                      password="12345",
                      host="localhost",
                      port="5432")
        self.conn.autocommit = True
        self.cursor=self.conn.cursor()

    def _create_shedule_tab(self):
        self.list_table=list()
        self.list_table_name=list()
        self.shedule_tab=QWidget()
        self.subject_tab=QWidget()
        self.teacher_tab=QWidget()
        self.tabs.addTab(self.shedule_tab,"График")
        self.tabs.addTab(self.subject_tab,"Предметы")
        self.tabs.addTab(self.teacher_tab,"Преподаватели")

        self.monday_gbox=QGroupBox("Понедельник")
        self.tuesday_gbox=QGroupBox("Вторник")
        self.wednesday_gbox=QGroupBox("Среда")
        self.thursday_gbox=QGroupBox("Четверг")
        self.friday_gbox=QGroupBox("Пятница")

        self.svbox=QVBoxLayout()
        self.shbox1=QHBoxLayout()
        self.shbox2=QHBoxLayout()
        self.shbox3=QHBoxLayout()
        self.shbox4=QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        
        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox2.addWidget(self.wednesday_gbox)
        self.shbox2.addWidget(self.thursday_gbox)
        self.shbox3.addWidget(self.friday_gbox)
        
        self._create___table("Понедельник")
        self.list_table_name.append("Понедельник")
        self._create___table("Вторник")
        self.list_table_name.append("Вторник")
        self._create___table("Среда")
        self.list_table_name.append("Среда")
        self._create___table("Четверг")
        self.list_table_name.append("Четверг")
        self._create___table("Пятница")
        self.list_table_name.append("Пятница")
    
        self.update_shedule_button=QPushButton("Обновить")
        self.shbox4.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

        self.subject_gbox=QGroupBox("Предметы")
        self.subject_svbox=QVBoxLayout()
        self.subject_shbox1=QHBoxLayout()
        self.subject_shbox2=QHBoxLayout()
        self.subject_svbox.addLayout(self.subject_shbox1)
        self.subject_svbox.addLayout(self.subject_shbox2)
        self.subject_shbox1.addWidget(self.subject_gbox)
        self.update_subject_button=QPushButton("Обновить")
        self.subject_shbox2.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_shedule)
        
        self._create_subject_table()
        self.subject_tab.setLayout(self.subject_svbox)

        self.teacher_gbox=QGroupBox("Предметы")
        self.teacher_svbox=QVBoxLayout()
        self.teacher_shbox1=QHBoxLayout()
        self.teacher_shbox2=QHBoxLayout()
        self.teacher_svbox.addLayout(self.teacher_shbox1)
        self.teacher_svbox.addLayout(self.teacher_shbox2)
        self.teacher_shbox1.addWidget(self.teacher_gbox)
        self.update_teacher_button=QPushButton("Обновить")
        self.teacher_shbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_shedule)
        
        self._create_teacher_table()
        self.teacher_tab.setLayout(self.teacher_svbox)

    def _create___table(self,name):
        
        table=QTableWidget()
        self.list_table.append(table)
        table.setParent(None)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID","ID Предмета "," Номер комнаты ","Время ","Четная неделя? ","",""])
        self._update___table(table,name)
        mvbox=QVBoxLayout()
        mvbox.addWidget(table)
        if name=="Понедельник":
            self.monday_gbox.setLayout(mvbox)
        elif name=="Вторник":
            self.tuesday_gbox.setLayout(mvbox)
        elif name=="Среда":
            self.wednesday_gbox.setLayout(mvbox)
        elif name=="Четверг":
            self.thursday_gbox.setLayout(mvbox)
        else:
            self.friday_gbox.setLayout(mvbox)
                                                

        delegate = ReadOnlyDelegate(self)
        table.setItemDelegateForRow(1, delegate)
        table.setItemDelegateForColumn(0, delegate)

    def _create_subject_table(self):
        self.subject_table=QTableWidget()
        self.subject_table.setParent(None)
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["ID"," Название ","",""])
        self._update_subject_table()
        mvbox=QVBoxLayout()
        mvbox.addWidget( self.subject_table)
        self.subject_gbox.setLayout(mvbox)                                               
        delegate = ReadOnlyDelegate(self)
        self.subject_table.setItemDelegateForRow(1, delegate)
        self.subject_table.setItemDelegateForColumn(0, delegate)

    def _create_teacher_table(self):
        self.teacher_table=QTableWidget()
        self.teacher_table.setParent(None)
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["ID"," ФИО ","Id Предмета","",""])
        self._update_teacher_table()
        mvbox=QVBoxLayout()
        mvbox.addWidget( self.teacher_table)
        self.teacher_gbox.setLayout(mvbox)                                               
        delegate = ReadOnlyDelegate(self)
        self.teacher_table.setItemDelegateForRow(1, delegate)
        self.teacher_table.setItemDelegateForColumn(0, delegate)

    def _update___table(self,table,name):
       
        self.cursor.execute("select * from service.timetable where day='{}' order by  chet , start_time".format(name))
        records=list(self.cursor.fetchall())
        table.setRowCount(0)
        table.setRowCount(len(records)+1)
        for i,r in enumerate(records):
            r=list(r)
            joinButton=QPushButton("Изменить")
            removeButton=QPushButton("Удалить")
            checkBox=QCheckBox()
            if r[5]:
                checkBox.toggle()
            table.setItem(i,0,QTableWidgetItem(str(r[0])))
            table.setItem(i,1,QTableWidgetItem(str(r[1])))
            table.setItem(i,2,QTableWidgetItem(str(r[2])))
            table.setItem(i,3,QTableWidgetItem(str(r[3])))
            table.setCellWidget(i,4,checkBox)
            table.setCellWidget(i,5,joinButton)
            table.setCellWidget(i,6,removeButton)
            
            joinButton.clicked.connect(lambda ch, num=i: self._change_table(num,table))
            removeButton.clicked.connect(lambda ch, num=i: self._remove_from_table(num,table))
            
            table.resizeRowsToContents()
        else:
            insertButton=QPushButton("Добавить")
            checkBox=QCheckBox()
            table.setItem(len(records),0,QTableWidgetItem(""))
            table.setItem(len(records),1,QTableWidgetItem(""))
            table.setItem(len(records),2,QTableWidgetItem(""))
            table.setItem(len(records),3,QTableWidgetItem(""))
            table.setCellWidget(len(records),4,checkBox)
            table.setCellWidget(len(records),5,insertButton)
            table.setItem(len(records),6,QTableWidgetItem(""))
            insertButton.clicked.connect(lambda : self._insert_table(int(len(records)),name,table))

            table.resizeRowsToContents()

    
    def _update_subject_table(self):
       
        self.cursor.execute("select * from service.subject ".format())
        records=list(self.cursor.fetchall())
        self.subject_table.setRowCount(0)
        self.subject_table.setRowCount(len(records)+1)
        for i,r in enumerate(records):
            r=list(r)
            joinButton=QPushButton("Изменить")
            removeButton=QPushButton("Удалить")
  
            self.subject_table.setItem(i,0,QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i,1,QTableWidgetItem(str(r[1])))

            self.subject_table.setCellWidget(i,2,joinButton)
            self.subject_table.setCellWidget(i,3,removeButton)
            
            joinButton.clicked.connect(lambda ch, num=i: self._change_subject_table(num))
            removeButton.clicked.connect(lambda ch, num=i: self._remove_from_subject_table(num))
            
            self.subject_table.resizeRowsToContents()
        else:
            insertButton=QPushButton("Добавить")
            self.subject_table.setItem(len(records),0,QTableWidgetItem(""))
            self.subject_table.setItem(len(records),1,QTableWidgetItem(""))
            self.subject_table.setCellWidget(len(records),2,insertButton)
            self.subject_table.setItem(len(records),3,QTableWidgetItem(""))
            insertButton.clicked.connect(lambda : self._insert_subject_table(int(len(records))))

            self.subject_table.resizeRowsToContents()

    def _update_teacher_table(self):
       
        self.cursor.execute("select * from service.teacher ".format())
        records=list(self.cursor.fetchall())
        self.teacher_table.setRowCount(0)
        self.teacher_table.setRowCount(len(records)+1)
        for i,r in enumerate(records):
            r=list(r)
            joinButton=QPushButton("Изменить")
            removeButton=QPushButton("Удалить")
  
            self.teacher_table.setItem(i,0,QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i,1,QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i,2,QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i,3,joinButton)
            self.teacher_table.setCellWidget(i,4,removeButton)
            
            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_table(num))
            removeButton.clicked.connect(lambda ch, num=i: self._remove_from_teacher_table(num))
            
            self.teacher_table.resizeRowsToContents()
        else:
            insertButton=QPushButton("Добавить")
            self.teacher_table.setItem(len(records),0,QTableWidgetItem(""))
            self.teacher_table.setItem(len(records),1,QTableWidgetItem(""))
            self.teacher_table.setItem(len(records),2,QTableWidgetItem(""))
            self.teacher_table.setCellWidget(len(records),3,insertButton)
            self.teacher_table.setItem(len(records),4,QTableWidgetItem(""))
            insertButton.clicked.connect(lambda : self._insert_teacher_table(int(len(records))))

            self.teacher_table.resizeRowsToContents()
            
    def _change_table(self, rowNum,table):
        try:
            row=list()         
            row.append(table.item(rowNum,0).text())
            row.append(table.item(rowNum,1).text())
            row.append(table.item(rowNum,2).text())
            row.append(table.item(rowNum,3).text())
            row.append(table.cellWidget(rowNum, 4).isChecked())

        
            self.cursor.execute("UPDATE service.timetable SET subject_id='{}', room_numb='{}', start_time='{}', chet='{}' WHERE id = '{}'; ".format(row[1],row[2],row[3],row[4],row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _change_subject_table(self, rowNum):
        try:
            row=list()         
            row.append(self.subject_table.item(rowNum,0).text())
            row.append(self.subject_table.item(rowNum,1).text())

        
            self.cursor.execute("UPDATE service.subject SET name='{}' WHERE id = '{}'; ".format(row[1],row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _change_teacher_table(self, rowNum):
        try:
            row=list()         
            row.append(self.teacher_table.item(rowNum,0).text())
            row.append(self.teacher_table.item(rowNum,1).text())
            row.append(self.teacher_table.item(rowNum,2).text())
        
            self.cursor.execute("UPDATE service.teacher SET full_name='{}', subject_id='{}' WHERE id = '{}'; ".format(row[1],row[2],row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")
    
    def _remove_from_table(self, rowNum,table):
        try:
            row=list()         
            row.append(table.item(rowNum,0).text())

        
            self.cursor.execute("DELETE FROM service.timetable WHERE id = '{}'; ".format(row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _remove_from_subject_table(self, rowNum):
        try:
            row=list()         
            row.append(self.subject_table.item(rowNum,0).text())

        
            self.cursor.execute("DELETE FROM service.subject WHERE id = '{}'; ".format(row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _remove_from_teacher_table(self, rowNum):
        try:
            row=list()         
            row.append(self.teacher_table.item(rowNum,0).text())

        
            self.cursor.execute("DELETE FROM service.teacher WHERE id = '{}'; ".format(row[0]))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")
    
    def _insert_table(self, rowNum,day,table):
        try:
            row=list()         
            row.append("")
            row.append(table.item(rowNum,1).text())
            row.append(table.item(rowNum,2).text())
            row.append(table.item(rowNum,3).text())
            row.append(table.cellWidget(rowNum, 4).isChecked())
            
        
            self.cursor.execute("INSERT INTO service.timetable(subject_id, room_numb, start_time, day, chet)VALUES ( '{}', '{}', '{}' ,'{}', '{}')".format(row[1],row[2],row[3],day,row[4]))
            self.conn.commit()
            self._update_shedule()
        except :
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _insert_subject_table(self, rowNum):
        try:
            row=list()         
            row.append("")
            row.append(self.subject_table.item(rowNum,1).text())
            print(row)
            self.cursor.execute("INSERT INTO service.subject(name) VALUES ( '{}')".format(row[1]))
            self.conn.commit()
            self._update_shedule()
        except :
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")

    def _insert_teacher_table(self, rowNum):
        try:
            row=list()         
            row.append("")
            row.append(self.teacher_table.item(rowNum,1).text())
            row.append(self.teacher_table.item(rowNum,2).text())
            print(row)
            self.cursor.execute("INSERT INTO service.teacher(full_name,subject_id) VALUES ( '{}','{}')".format(row[1],row[2]))
            self.conn.commit()
            self._update_shedule()
        except :
            QMessageBox.about(self,"Ошибка","Введены некорректные данные")
            
    def _update_shedule(self):
        for i in range (len(self.list_table)):            
            self._update___table(self.list_table[i],self.list_table_name[i])
        self._update_subject_table()
        self._update_teacher_table()


def my_excepthook(type, value, tback):
    QtWidgets.QMessageBox.critical(
        window, "CRITICAL ERROR", str(value),
        QtWidgets.QMessageBox.Cancel
    )
 
    sys.__excepthook__(type, value, tback)
 
 
sys.excepthook = my_excepthook

app=QApplication(sys.argv)
win=MainWindow()
win.show()
sys.exit(app.exec_())
        
