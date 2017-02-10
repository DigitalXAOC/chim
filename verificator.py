#4. Vcrificator, тип: verificator. Пользовательский интерфейс и алгоритмы обработки данных
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Программно-аппаратный комплекс "Автоматизация проведения поверочных процедур метрологического оборудования"
# (с) НПО "Химавтоматика", 2009 - 2011
# Пользовательский интерфейс и алгоритмы обработки данных

from __future__ import division
import sys, os, platform, re, datetime, random, codecs, localmath
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
import ui_main
import ui_total
from elixir import *
from generate import *
from localmath import Jail, sanitize

accelerator = False
demo = True
release = False

theos=platform.system()
fsenc=sys.getfilesystemencoding()
frost=hasattr(sys, 'frozen')

if frost:
    filepath = os.path.dirname(unicode(sys.executable,fsenc))
    fileformat = u'скомпонованный'
elif __file__:
    filepath = os.path.dirname(__file__)
    fileformat = u'обычный'

datapath = os.path.join(filepath, 'verificator.db')

if theos == 'Windows':
    import win32api
    datapath=win32api.GetShortPathName(datapath)

dataconnstr = "sqlite:///"+datapath.encode(fsenc)

metadata.bind = dataconnstr

internal=Jail()

def doParam(param, data):
    result=re.sub(r'\b%s\b' % param, '%s' % param, data)
    return result

def doParams(paramlist, data):
    result = data
    for param in paramlist:
        result = doParam(param, result)
    return result

def doIndexParam(param, data):
    result=re.sub(r'\b%s\b' % param, '%s[i]' % param, data)
    return result

def doIndexParams(paramlist, data):
    result = data
    for param in paramlist:
        result = doParam(param, result)

def doParamValue(param, data, valuestr):
    result=re.sub(r'{\b%s\b}' % param, valuestr, data)
    return result

def deleteLayout(layout):
    clearLayout(layout)
    QCoreApplication.sendPostedEvents(layout, QEvent.DeferredDelete)

def clearLayout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
    if isinstance(item.layout(), QLayout):
        clearLayout(item.layout())
        item.layout().deleteLater()
    elif isinstance(item.widget(), QWidget):
        item.widget().deleteLater()
    layout.deleteLater()

def getlntervalAsText(interval):
    if interval == 0:
        text = u'не определен.'
    elif interval == 6:
        text = u'6 месяцев.'
    elif interval == 12:
        text = u'1 год.'
    elif interval == 24:
        text = u'2 года.'
    else:
        text = u'%u мес.' % interval
    return text

class iterdataelement(object):
    def __init__(self):
        self.results=[]

class CheckProc(object):
    def __init__(self):
        self.protocolNum = u''
        self.checkDate = u''
        self.serialNum = u''
        self.inventoryNum = u''
        self.user = u''
        self.productionDate = u''
        self.verifier = u''
        self.device_type_id = 0
        self.device_info = u''

def Validate(self):
    if (self.protocolNum == u'' or self.checkDate == u'' or self.serialNum == u'' or self.inventoryNum == u'' or self.user == u'' or self.productionDate == u'' or self.verifier == u'' or self.device_type_id == 0):
        return False
    else:
        return True

class TotalCheckDialog(QDialog, ui_total.Ui_TotalCheckDialog):
    def __init__(self, parent=None):
        self.parent=parent
        super(TotalCheckDialog, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        self.q_ids = []
        self.checkInfoLabel.setText(u'')
        self.checkStatusLabel.setText(u'Проверка запущена.')
        self.needMoreData=False
        self.needComputing=False
        self.connect(self.printPushButton, SIGNAL("clicked()"), self.printReport)
        self.connect(self.savePushButton, SIGNAL("clicked()"), self.saveReport)
        self.connect(self.takeAnswerPushButton, SIGNAL("clicked()"), self.decideQuestion)
        self.connect(self.toolsListWidget, SIGNAL("itemChanged(QListWidgetItem*)"), self.toolsItemChanged)
        self.reportHeader = (u'<table width=" 100%%"><tr><td align="left"><b>Протокол поверки №<u> %s </u></b>'
            u'<td align="right"<b>от %s</b></table>' % (self.parent.currentCheckProc.protocolNum, self.parent.currentCheckProc.checkDate))
        self.report = u''
        self.reportFooter = (u'</ol><br>Поверитель:<u> %s </u><br><br>'
            u'<font size="-1">МП</font><br><br>' % self.parent.currentCheckProc.verifier)
        self.reportFooter += (u'<font size="-3" соlоr="#7f7f7f">Процедура поверки автоматизирована'
            u'ПО "Verificator" &copy; 2008-2010 ОАО НПО "Химавтоматика"</font>'
            u'<a name="footer">')
        self.deviceTypeInfoLabel.setText(parent.currentCheckProc.device_info)
        #self.showMaximized()
        self.reportGroupBox.setEnabled(False)
        self.stopCheckPushButton.setVisible(True)
        self.endCheckPushButton.setVisible(False)
        self.checkPrepareGroupBox.setVisible(True)
        self.questionGroupBox.setVisible(False)
        self.checkFrame.setVisible(True)
        QTimer.singleShot(0, self.loadData)

def loadData(self):
    self.updateReport()
    dt_id = self.parent.currentCheckProc.device_type_id
    self.deviceType=DeviceType.get_by(id = dt_id)
    tools = self.deviceType.required_tools
    self.checkInfoLabel.setText(u'Для данного типа оборудования требуется единиц поверочного оборудования: %d' %len(tools))
    for tool in tools:
        item = QListWidgetItem(u'%s (%s %s)' % (tool.name, tool.parameters, tool.standarts))
        item.setData(Qt.UserRole, QVariant(long(tool.id)))
        item.setCheckState(Qt.Unchecked)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemlsUserCheckable | Qt.ItemlsEnabled)
        self.toolsListWidgetaddItem(item)
        self.report+=u'<br><center><b>%s</b></center><br>' % self.deviceType.model
        self.героrt+=u'Заводской №:<u> %s </u><br>' % self.parent.currentCheckProc.serialNum
        self.report+=u'Инвентарный №:<u> %s </u><br>' % self.parent.currentCheckProc.inventoryNum
        self.героrt+=u'Принадлежит: <u> %s </u><br>' % self.parent.currentCheckProc.user
        self.report+=u'Дата выпуска:<u> %s </u><br>' % self.parent.currentCheckProc.productionDate
        self.updateReport()

        self.dt_paramnum = len(self. deviceType.passport_parameters)
        self.dt_paramlist = [param.variable_name for param in self.deviceType.passport_parameters]
        self.dt_paramcomlist = [param.description for param in self.deviceType.passport__parameters]
        self.dt_paramnamelist = [param.readable_name for param in self.deviceType.passport_parameters]
        self.dt_paramhintlist = [param.hint for param in self.deviceType.passport_parameters]
        self.d_paramvallist = ['' for param in self.deviceType.passport_parameters]
        self.addInfoLabel.setText('')
        if self.dt_paramnum:
            addtext = u'Для данного типа оборудования требуется ввод паспортных значений следующих параметров:<br>'
        for i in range(self.dt_paramnum):
            addtext += '<b>' + self.dt_paramnamelist[i]+'</b> - <i>' + self.dt_paramcomlist[i] + '</i><br>'
            self.addlnfoLabel.setText(addtext)
            self.needMoreData=True

def updateInfo(self, gn, gc, qn, qc):
    infotext = u'Выполняется группа №%d: "%s", запрос №%d: "%s"' % (gn, gc, qn, qc)
    self.checklnfoLabel.setText(infotext)

def toolsItemChanged(self):
    QTimer.singleShot(0, self.maybePrepared)

def maybePrepared(self):
    prepared = False
    total = self.toolsListWidget.count()
    checked = 0
    for i in range(total):
        item = self.toolsListWidget.item(i)
    if (item.checkStateO == Qt.Checked):
        checked += 1
        prepared = (checked == total)
    if accelerator:
        prepared = True
    if prepared:
        self.checkStatusLabel.setText(u'Поверочное оборудование  подготовлено.')
        q_groups=self.deviceType.question_groups
    for group in q_groups:
        questions=group.questions
    for q in questions:
        self.q_ids.append(q.id)
        self.checkPrepareGroupBox.setVisible(False)
        self.questionGroupBox.setVisible(True)
        self.checkStatusLabel.setText('')
    if self.needMoreData:
        QTimer.singleShot(0, self.requestData)
    else:
        self.report+=u'<center><b>Результаты поверки</b></center><ol>'
        self.updateReport()
        QTimer.singleShot(0, self.processQuestion)

def requestData(self):
    self.questionTextBrowser.setHtml(u'<p>Укажите актуальные для поверяемого в настоящий момент оборудования'
        u'паспортные значения указанных параметров.')
    if self.answerGroupBox.layout():
        deleteLayout(self.answerGroupBox.layout())
        self.layout=QVBoxLayout()
        self.param_edits=[]
        self.param_labels=[]
        self.param_names=[]
        self.param_layouts_in=[]
        self.param_layouts=[]
    for i in range(self.dt_paramnum):
        self.param_labels.append(QLabel(self.dt_paramcomlist[i]+':'))
    if demo or release:
        hint='='
    else:
        hint='=<font color=red>'+self.dt_paramhintlist[i]+'</font>'
        self.param_names.append(QLabel(self.dt_paramnamelist[i]+hint))
        self.param_edits.append(QLineEdit())
        self.param_layouts_in.append(QHBoxLayout())
        self.param_layouts_in[i].addWidget(self.param_names[i])
        self.param_layouts_in[i].addWidget(self.param_edits[i])
        self.connect(self.param_edits[i], SIGNAL("textChanged(QString)"),
        lambda value=self.param_edits[i].text(), num=i: self.dt_setres(value,num))
    if accelerator or demo:
        self.param_edits[i].setText(self.dt_paramhintlist[i])
        self.param_layouts.append(QVBoxLayout())
        self.param_layouts[i].addWidget(self.param_labels[i])
        self.param_layouts[i].addLayout(self.param_layouts_in[i])
        self.layout.addLayout(self.param_layouts[i])
        self.answerGroupBox.setLayout(self.layout)

def dt_setres(self,value,num): self.d_paramvallist[num]=unicode(sanitize(value))

def decideQuestion(self):
    if self.needMoreData:
        self.needMoreData = False
        for i in range(self.dt_paramnum):
            statement='%s=%s' % (self.dt_paramlist[i], self.d_paramvallist[i])
            exec(statement,vars(localmath),vars(internal))
            addtext = u''
            self.report += u'<br>Характеристики и паспортные значения:<br>'
        for i in range(self.dt_paramnum):
            self.report += self.dt_paramcomlist[i] + ':' + self.dt_paramnamelist[i]+'='+self.d_paramvallist[i]+'<br>'
            self.addInfoLabel.setText(addtext)
            self.report+=u'<center><b>Результаты поверки</b></center><ol>'
            self.updateReport()
            QTimer.singleShot(0, self.processQuestion)
    elif self.needComputing:
        self.needComputing = False
        statetext=u''
        for i in range(self.paramnum):
            statetext+=u'%s%s=%s ' % (self.paramlist[i], self.subscript(self.iter), self.iterdata[self.iter].results[i])
        if self.q.iterations:
            statement=u'%s[%d]=%s' % (self.paramlist[i], self.iter, self.iterdata[self.iter].results[i])
        else:
            statement=u'%s=%s' % (self.paramlist[i], self.iterdata[self.iter].results[i])
            exec(statement,vars(localmath),vars(internal))

        if not self.q.iterations:
            calc=self.q.calculation
            exec(calc,vars(localmath),vars(internal))
            cond=self.q.condition
            self.res=eval(cond,vars(localmath),vars(internal))
        else:
            condstat=self.q.condition
        for a in range(len(self.paramlist)):
            condstat=doIndexParam(self.paramlist[a], condstat)
            internal.i=self.iter
            exec(condstat,vars(localmath),vars(internal))

        self.iter += 1
        if self.q.iterations:
            if self.iter == self.q.iterations:
                itercalc=self.q.itercalc
                exec(itercalc,vars(localmath),vars(internal))
                itercond=self.q.itercond
        for a in range(len(self.paramlist)):
            itercond=doIndexParam(self.paramlist[a], itercond)
            self.res=eval(itercond,vars(localmath),vars(internal))
        if self.q.reportstring != None:
            self.reportstring=self.q.reportstring
        for a in range(len(self.iterparamlist)):
            value = '%.2f' % round(eval(self.iterparamlist[a],vars(localmath),vars(internal)),2)
            self.reportstring=doParamValue(self.iterparamlist[a], self.reportstring, value)
            self.report += self.reportstring
            self.updateReport()
        if self.res:
            if self.q.conclusion_success != None:
                self.reportstring=self.q.conclusion_success
                self.report += self.reportstring
                self.updateReport()
                QTimer.singleShot(0, self.processQuestion)
            else:
                if self.q.conclusion_failure != None:
                    self.reportstring=self.q.conclusion_failure
                    self.report += self.reportstring
                    self.updateReport()
                    QTimer.singleShot(0, self.finalize)
                else:
                    QTimer.singleShot(0, self.drawIteration)
        else:
            if self.q.reportstring != None:
                self.reportstring=self.q.reportstring
                for a in range(len(self.paramlist)):
                    value = '%.2f' % round(eval(self.paramlist[a],vars(localmath),vars(internal)),2)
                    self.reportstring=doParamValue(self.paramlist[a], self.reportstring, value)
                    self.report+= self.reportstring
                    self.updateReport()
            if self.res:
                if self.q.conclusion_success != None:
                    self.reportstring=self.q.conclusion_success
                    self.report += self.reportstring
                    self.updateReport()
                    QTimer.singleShot(0, self.processQuestion)
            else:
                if self.q.conclusion_failure != None:
                    self.reportstring=self.q.conclusion_failure
                    self.report += self.reportstring
                    self.updateReport()
                    QTimer.singleShot(0, self.finalize)

                else:
                    self.iter=0
                    self.iterdata=[]
                    self.reportstring=u''
                    for i in range(self.q.iterations):
                        self.iterdata.append(iterdataelement())
                    if self.q.iterations == 0:
                        self.iterdata.append(iterdataelement())
                    if not self.q.iterations:
                        for image in self.q.images:
                            self.questionTextBrowser.document().addResource(QTextDocument.ImageResource,QUrl(image.name),QVariant(
                            QByteArray(image.data)))
                            self.questionTextBrowser.setHtml(self.q .text)
                            self.paramIist=self.q.params.split('$')
                    if self.paramlist == ['']:
                        self.paramlist = []
                        self.paramnum=len(self.paramlist)
                    for i in range(self.paramnum):
                        self.paramlist[i]=self.paramlist[i].strip()
                    if self.q.iterations:
                        for i in range(self.paramnum):
                            statement='%s=[0 for i in range(%d)]' % (self.paramlist[i], self.q.iterations)
                            exec(statement,vars(localmath),vars(internal))
                            self.iterparamlist=self.q.iterparams.split('$')
                        if self.iterparamlist == ['']:
                            self.iterparamlist = []
                            self.iterparamnum=len(self.iterparamlist)
                            for i in range(self.iterparamnum):
                                self.iterparamlist[i]=self.iterparamlist[i].strip()

    self.paramcomlist=self.q.param_comments.split('$')
    if self.paramcomlist == ['']:
        self.paramcomlist = []
        self.paramnum=len(self.paramcomlist)
    for i in range(self.paramnum):
        self.paramcomlist[i]=self.paramcomlist[i].strip()

    if self.q.question_type_id == 1:
        self.paramnamelist=self.q.param_names.split('$')
    if self.paramnamelist == ['']:
        self.paramnamelist = []
    for i in range(self.paramnum):
        self.paramnamelist[i]=self.paramnamelist[i] .strip()
        self.paramhintlist=self.q.param_hints.split('$')
    if self.paramhintlist == ['']:
        self.paramhintlist = []
    for i in range(self.paramnum):
        self.paramhintlist[i]=self.paramhintlist[i].strip()

    if self.q.question_type_id == 1:
        for i in range(self.paramnum):
            for j in range(self.dt_paramnum):
                self.paramhintlist[i]=doParam(self.dt_paramlist[j], self.paramhintlist[i])
    if self.q.iterations:
        for i in range(self.paramnum):
            for j in range(len(self.iterparamlist)):
                self.paramhintlist[i]=doParam(self.iterparamlist[j], self.paramhintlist[i])
    for i in range(self.paramnum):
        self.paramhintlist[i]='%.2f' %round(eval(self.paramhintlist[i],vars(localmath),vars(internal)),2)
        QTimer.singleShot(0,self.drawIteration)

def processQuestion(self):
    if len(self.q_ids) > 0:
        q_id = self.q_ids.pop(0)
        self.q = Question.get_by(id = q_id)
        g_id = self.q.question_group.id
        g = QuestionGroup.get_by(id = g_id)
        self.updateInfo(g.num, g.caption, self.q.num, self.q.caption)
        if (self.q.num == 1) and (g.report_caption):
            self.report += '<br><li> <b>%s</b><br>' % g.caption
            self.updateReport()
            QTimer.singleShot(0, self.decideQuestion)
    else:
        QTimer.singleShot(0, self.finalize)

def drawlteration(self):
    self.needComputing = True;
    if self.q.iterations:
        self.checkStatusLabel.setText(u'Выполняется итерация %d из %d' % (self.iter+1, self.q.iterations))
    else:
        self.checkStatusLabel.clear()

    if self.q.iterations:
        self.questionTextBrowser.setHtml(self.q.text.replace('&INDEX',self.subscript(self.iter+1)))

    for i in range(self.paramnum):
        self.iterdata[self.iter] .results.append(None)

    if self.answerGroupBox.layout():
        deleteLayout(self.answerGroupBox.layout())
        self.layout=QVBoxLayout()
    if self.q.question_type_id == 1:
        self.edits=[]
        self.labels=[]
        self.layouts=[]
    for i in range(self.paramnum):
        if demo or release:
            hint='='
        else:
            hint='=<font color=red>'+self.paramhintlist[i]+'<font>'
    if self.q.iterations:



        self.labels.append(QLabel(self.paramcomlist[i].replace('&INDEX',self.subscript(self.iter+1))+'; '+
        self.paramnamelist[i].replace('&INDEX',self.subscript(self.iter+1))+hint))
    else:
        self.labels.append(QLabel(self.paramcomlist[i]+'; '+self.paramnamelist[i]+hint))
        self.edits.append(QLineEdit())
        self.layouts.append(QHBoxLayout())
        self.layouts[i].addWidget(self.labels[i])
        self.layouts[i].addWidget(self.edits[i])
        self.connect(self.edits[i], SIGNAL("textChanged(QString)"),
        lambda value=self.edits[i].text(), num=i: self.setres(value,num))
    if accelerator or demo:
        self.edits[i].setText(self.paramhintlist[i])
        self.layout.addLayout(self.layouts[i])
    elif self.q.question_type_id == 2:
        self.buttons=[]
        for i in range(self.paramnum):
            self.buttons.append(QRadioButton(self.paramcomlist[i]))
            self.connect(self.buttons[i], SIGNAL("toggled(bool)"),
            lambda value=self.buttons[i].isChecked(), num=i: self.setres(value,num))
            self.layout.addWidget(self.buttons[i])
            self.buttons[0].setChecked(True)
    elif self.q.question_type_id == 3:
        self.buttons=[]
        for i in range(self.paramnum):
            self.buttons.append(QCheckBox(self.paramcomlist[i]))
            self.connect(self.buttons[i], SIGNAL("toggled(bool)"),
            lambda value=self.buttons[i].isChecked(), num=i: self.setres(value,num))
            self.layout.addWidget(self.buttons[i])
            self.buttons[i].setChecked(False)
        if accelerator or demo:
            self.buttons[i].setChecked(True)
            self.answerGroupBox.setLayout(self.layout)

def setres(self,value,num):
    self.iterdata[self.iter].results[num]=unicode(sanitize( value))

def subscript(self, i):
    if self.q.iterations:
        return '<sub>%d</sub>' % i
    else:
        return ''

def fmalize(self):
    self.checkStatusLabel.setText(u'Поверка завершена.')
    self.stopCheckPushButton.setVisible(False)
    self.endCheckPushButton.setVisible(True)
    self.reportGroupBox.setEnabled(True)
    self.checkFrame.setVisible(False)

def updateReport(self):
    self.reportTextBrowser.setHtml(self.reportHeader + self.report + self.reportFooter)
    self.reportGroupBox.setEnabled(True)
    self.reportTextBrowser.scrollToAnchor('footer')
    self.reportGroupBox.setEnabled(False)

def printReport(self):
    global printer
    printer.setOutputFileName(u'')
    printer.setOutputFormat(QPrinter.NativeFormat)
    dialog = QPrintDialog(printer, self)
    if dialog.exec_():
        document = QTextDocument()
        document.setHtml(self.reportHeader + self.report + self.reportFooter)
        document.print_(printer)

def saveReport(self):
    global printer
    filename=unicode(QFileDialog.getSaveFileName(self, u'Сохранить отчет', u'report_%s.pdf'
    % self.parent.currentCheckProc.protocolNum, u'PDF (*.pdf)'))
    if filename:
        printer.setOutputFileName(filename)
        printer.setOutputFormat(QPrinter.PdfFormat)
        document = QTextDocument()
        document.setHtml(self.reportHeader + self.report + self.reportFooter)
        document.print_(printer)

class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def	init	(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        if demo or release:
            self.sysinfoLabel.clear()
        else:
            self.sysinfoLabel.setText(u'Формат исполнения: %s;\nВызвано из: %s\nOC: %s;'
            u' Кодировка ФС: %s\nПуть к БД: %s' % (fileformat, filepath, theos, fsenc, datapath))
            settings = QSettings()
            size = settings.value('MainWindow/Size').toSize()
        if size:
            self.resize(size)
            position = settings.value('MainWindow/Position', QVariant(QPoint(0, 0))).toPoint()
            self.move(position)
            self.restoreState(settings.value('MainWindow/State').toByteArray())
            self.checkDateEdit.calendarWidget().setFirstDayOfWeek(Qt.Monday)
            self.productionDateEdit.calendarWidget().setFirstDayOfWeek(Qt.Monday)
            self.currentCheckProc = CheckProc()
            self.connect(self.beginPushButton, SIGNAL('clicked()'), self.startCheck)
            self.connect(self. pushButton, SIGNAL("clicked()"), self.fillData)
            self.connect(self.deviceTypeListWidget, SIGNAL('currentItemChanged(QListWidgetItem*,QListWidgetItem*)'), self.selectDeviceType)
            self.connect(self.deviceTypeListWidget, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.startCheck)
            self.connect(self. protocolNumLineEdit, SIGNAL('textChanged(const QString&)'), self.setProtocolNum)
            self.connect(self.checkDateEdit, SIGNAL('dateChanged(const QDate&)'), self.setCheckDate)
            self.connect(self. serialNumLineEdit, SIGNAL('textChanged(const QString&)'), self.setSerialNum)
            self.connect(self. inventoryNumLineEdit, SIGNAL('textChanged(const QString&)'), self.setlnventoryNum)
            self.connect(self.userLineEdit, SIGNAL('textChanged(const QString&)'), self.setUser)
            self.connect(self.productionDateEdit, SIGNAL('dateChanged(const QDate&)'), self.setProductionDate)
            self.connect(self.verifierLineEdit, SIGNAL('textChanged(const QString&)'), self.setVerifier)
            self.checkDateEdit.setDate(QDate.currentDate())
            QTimer.singleShot(0, self.initData)

def initData(self):
    self.deviceTypeListWidget.clear()
    deviceTypes = DeviceType.query.all()
    i = 1
    for deviceType in deviceTypes:
        item = QListWidgetItem(u'%u) %s: %s' % (i, deviceType.type, deviceType.model))
        item.setData(Qt.UserRole, QVariant(long(deviceType.id)))
        self.deviceTypeListWidget.addltem(item)
        i += 1

def fillData(self):
    if accelerator or demo:
        numbers=['1','2','3','4','5','6','7','8','9']
        serial=''.join([random.choice(numbers) for x in range(6)])
        invent=''.join([random.choice(numbers) for x in range(4)])
        self.serialNumLineEdit.setText(unicode(serial))
        self.inventoryNumLineEdit.setText(unicode(invent))
        self.userLineEdit.setText(u'Воинская часть 35 в/ч')
        self.productionDateEdit.setDate(QDate.addDays(QDate.currentDate(),random.randrange(-3650,-365)))
        self.verifierLineEdit.setText(u'Килиманджаров Р.Я.')
        self.deviceTypeListWidget.setCurrentRow(random.randrange(self.deviceTypeListWidget.count()))
        self.protocolNumLineEdit.setText(unicode(self.deviceTypeListWidget.currentRow()+1))

def setProtocolNum(self):
    self.currentCheckProc.protocolNum = self.protocolNumLineEdit.text()
    self.protocolNumLabel.setStyleSheet('')

def setCheckDate(self):
    months=[u'января',u'февраля',u'марта',u'апреля',u'мая',u'июня',u'июля',u'августа',u'сентября',u'октября',u'ноября',u'декабря']
    self.currentCheckProc.checkDate = u'&laquo;<u>&nbsp;%02u&nbsp;</u>&raquo;<u>&nbsp; %s&nbsp;</u>&nbsp;20<u>%02u</u>' % (
    self.checkDateEdit.date().day(), months[self.checkDateEdit.date().month()-1],
        (self.checkDateEdit.date().year() % 100))
    self.checkDateLabel.setStyleSheet('')

def setSerialNum(self):
    self.currentCheckProc.serialNum = self.serialNumLineEdit.text()
    self.serialNumLabel.setStyleSheet('')

def setInventoryNum(self):
    self.currentCheckProc.inventoryNum = self.inventoryNumLineEdit.text()
    self.inventoryNumLabel.setStyleSheet('')

def setUser(self):
    self.currentCheckProc.user = self.userLineEdit.text()
    self.userLabel.setStyleSheet('')

def setProductionDate(self):
    self.currentCheckProc.productionDate = self.productionDateEdit.date().toString(Qt.DefaultLocaleShortDate)
    self.productionDateLabel.setStyleSheet('')

def setVerifier(self):
    self.currentCheckProc.verifier = self.verifierLineEdit.text()
    self.verifierLabel.setStyleSheet('')

def selectDeviceType(self, item, item2):
    self.currentCheckProc.device_type_id = item.data(Qt.UserRole).toInt()[0]
    if accelerator or demo:
        self.protocolNumLineEdit.setText(unicode(self.deviceTypeListWidget.currentRow()+1))
        deviceType = DeviceType.query.filter_by(id = self.currentCheckProc.device_type_id).one()
        device_type_model = deviceType.model
        device_type_description = deviceType.description
        device_type_check_interval = deviceType.check_interval
        device_type_documents = deviceType.documents
        self.currentCheckProc.device_info = (u'<i>Методика:</i> '
                                             u'%s<br><i>Оборудование:</i> '
                                             u'%s<br><i>Документация:</i>%s'
                                             u'<br><i>Межповерочный интервал:</i> %s' % (device_type_model,
                                            device_type_description, device_type_documents,
                                            getlntervalAsText(device_type_check_interval)))
    self.deviceTypeDescriptionLabel.setText(self.currentCheckProc.device_info)

def startCheck(self):
    if not self.currentCheckProc.device_type_id:
        QMessageBox.critical(self,u'Поверка невозможна',u'He была выбрана методика поверки.')
        return
    if not self.currentCheckProc.Validate():
        QMessageBox.critical(self,u'Поверка не может быть начата', u'He заполнены поля протокола поверки.')
        return
    total=TotalCheckDialog(self)
    if total.exec_():
        pass

def closeEvent(self, event):
    settings = QSettings()
    settings.setValue('MainWindow/Size', QVariant(self.size()))
    settings.setValue('MainWindow/Position', QVariant(self.pos()))
    settings.setValue('MainWmdow/State', QVariant(self.saveState()))

def main():
    global printer

    app = QApplication(sys.argv)
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)
    app.setOrganizalionName('Chimavtomatika')
    app.setOrganizationDomain('chimavtomatika.ru')
    app.setApplicationName('Metrology Equipment Verificator')
    form = MainWindow()
    form.show()
    app.exec_()
    session.commit()

    setup_all()
    main()__