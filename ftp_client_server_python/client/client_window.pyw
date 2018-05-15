#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
import logging
import threading
import time
import ftplib
import enum
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from client import MyFTPClient
from utils import fileProperty
import os

class StatusOfLoading(enum.Enum):
    PROCESS = "Обмен"
    PAUSED = "Приостановлено"

class ConnectWindow(QWidget):
    def __init__(self, parent_window = None, callbacks = None):
        super().__init__()
        self.callbacks = callbacks
        self.setWindowTitle("Введите данные для подключения")
        self.resize(350, 240)
        self.setFont(QFont('SansSerif', 10))
        self.parent = parent_window
        self.parent.setEnabled(False)
        # центрируем относительно родительского окна
        self.move(int(self.parent.x() + (self.parent.width() - self.width())/2), int(self.parent.y() + (self.parent.height() - self.height())/2))
        

        self.host_addr_lbl = QLabel(self)
        self.host_addr_lbl.setText("Адрес хоста:")
        self.host_addr_lbl.move(10, 10)

        self.host_addr_line = QLineEdit(self)
        self.host_addr_line.resize(220, 20)
        self.host_addr_line.move(110, 10)
        self.host_addr_line.setText("ftp://127.0.0.1")


        self.port_addr_lbl = QLabel(self)
        self.port_addr_lbl.setText("Порт хоста:")
        self.port_addr_lbl.move(19, 45)

        self.port_addr_line = QLineEdit(self)
        self.port_addr_line.resize(220, 20)
        self.port_addr_line.move(110, 45)
        self.port_addr_line.setText("3100")


        self.login_lbl = QLabel(self)
        self.login_lbl.setText("Логин:")
        self.login_lbl.move(53, 80)

        self.login_line = QLineEdit(self)
        self.login_line.resize(220, 20)
        self.login_line.move(110, 80)
        self.login_line.setText("user1")


        self.password_lbl = QLabel(self)
        self.password_lbl.setText("Пароль:")
        self.password_lbl.move(45, 115)

        self.password_line = QLineEdit(self)
        self.password_line.resize(220, 20)
        self.password_line.move(110, 115)
        self.password_line.setText("qwerty")


        self.connect_btn = QPushButton(self)
        self.connect_btn.setText("Подключиться")
        self.connect_btn.resize(QSize(160, 30))
        self.connect_btn.move(100, 160)
        self.connect_btn.clicked.connect(self.connect_to_server)

        self.message_lbl = QLabel(self)
        self.message_lbl.setText("")
        self.message_lbl.resize(330, 20)
        self.message_lbl.move(10, 200)
        self.message_lbl.setWordWrap(True)
        self.message_lbl.setFont(QFont('SansSerif', 8))

    def connect_to_server(self):
        self.message_lbl.setText("")
        try:
            self.parent.ftp_client = MyFTPClient(self.host_addr_line.text(), self.login_line.text(), self.password_line.text(), int(str(self.port_addr_line.text())), os.path.curdir, self.callbacks)
            self.parent.ftp_client.start_control()
            self.parent.connect_btn.setEnabled(False)
            self.close()
            self.parent.connected_to_server = True
            self.parent.renew_history_btn.setEnabled(True)
            self.parent.setEnabled(True)
        except:
            self.message_lbl.setText("Не удалось подключиться к серверу. Проверьте данные и повторите попытку.")
            pass

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        event.accept()

class NewFolderWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.setWindowTitle("Введите имя папки")
        self.resize(350, 220)
        self.setFont(QFont('SansSerif', 12))
        self.parent = parent_window
        self.parent.setEnabled(False)
        # центрируем относительно родительского окна
        self.move(int(self.parent.x() + (self.parent.width() - self.width())/2), int(self.parent.y() + (self.parent.height() - self.height())/2))

        self.new_folder_name_lbl = QLabel(self)
        self.new_folder_name_lbl.setText("Имя новой папки:")
        self.new_folder_name_lbl.move(10, 50)

        self.new_folder_name_line = QLineEdit(self)
        self.new_folder_name_line.resize(160, 20)
        self.new_folder_name_line.move(170, 48)
        self.new_folder_name_line.setText("")

        self.message_lbl = QLabel(self)
        self.message_lbl.setText("")
        self.message_lbl.move(10, 115)
        self.message_lbl.resize(330, 100)
        self.message_lbl.setWordWrap(True)
        self.message_lbl.setFont(QFont('SansSerif', 8))

        self.create_new_folder_btn = QPushButton(self)
        self.create_new_folder_btn.setText("Задать приоритет")
        self.create_new_folder_btn.resize(QSize(160, 30))
        self.create_new_folder_btn.move(100, 90)
        self.create_new_folder_btn.clicked.connect(lambda: self.create_new_folder())
        pass

    def create_new_folder(self):
        try:
            self.message_lbl.setText("")
            new_folder = self.new_folder_name_line.text()
            result = self.parent.ftp_client.make_remote_directory(new_folder)
            self.parent.setEnabled(True)
        except:
            self.message_lbl.setText("Ошибка! Возможные причины: \n-папка с таким именем уже существует; \n-у Вас недостаточно прав; \n-нет соединения с сервером; \n-задано неправильное имя;")
        pass

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        event.accept()

class ChangePriorityWindow(QWidget):
    def __init__(self, parent_window, full_path_to_local_file, old_priority):
        super().__init__()
        self.setWindowTitle("Введите приоритет")
        self.resize(350, 200)
        self.setFont(QFont('SansSerif', 12))
        self.parent = parent_window
        self.parent.setEnabled(False)
        self.old_priority = old_priority
        self.full_path_to_local_file = full_path_to_local_file
        # центрируем относительно родительского окна
        self.move(int(self.parent.x() + (self.parent.width() - self.width())/2), int(self.parent.y() + (self.parent.height() - self.height())/2))
        

        self.filename_lbl = QLabel(self)
        self.filename_lbl.setText("Файл: " + os.path.split(full_path_to_local_file)[1])
        self.filename_lbl.move(10, 10)

        self.new_priority_lbl = QLabel(self)
        self.new_priority_lbl.setText("Новый приоритет:")
        self.new_priority_lbl.move(10, 50)

        self.new_priority_line = QLineEdit(self)
        self.new_priority_line.resize(160, 20)
        self.new_priority_line.move(170, 48)
        self.new_priority_line.setText(str(old_priority))

        self.message_lbl = QLabel(self)
        self.message_lbl.setText("")
        self.message_lbl.move(10, 105)
        self.message_lbl.resize(330, 90)
        self.message_lbl.setWordWrap(True)
        self.message_lbl.setFont(QFont('SansSerif', 8))

        self.set_priority_btn = QPushButton(self)
        self.set_priority_btn.setText("Задать приоритет")
        self.set_priority_btn.resize(QSize(160, 30))
        self.set_priority_btn.move(100, 90)
        self.set_priority_btn.clicked.connect(self.change_priority)
        pass

    def change_priority(self):
        self.message_lbl.setText("")
        new_pr = None
        try:
            new_pr = int(self.new_priority_line.text())
        except ValueError:
            self.message_lbl.setText("Ошибка! Введите число!")
            return
        if new_pr <= 0:
            self.message_lbl.setText("Ошибка! Приоритет должен быть >= 1 !")
            return

        if self.parent.ftp_client.set_priority_of_loading(self.full_path_to_local_file, new_pr):
            self.close()
            self.parent.setEnabled(True)
        else:
            self.message_lbl.setText("Ошибка! При смене приоритета загрузки\выгрузки произошла ошибка. Попробуйте ещё раз.")
            self.set_priority_btn.setEnabled(False)
        pass

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        event.accept()

class RenameRemoteFileWindow(QWidget):
    def __init__(self, parent_window, old_remote_filename):
        super().__init__()
        self.setWindowTitle("Введите новое имя")
        self.resize(350, 300)
        self.setFont(QFont('SansSerif', 12))
        self.parent = parent_window
        self.parent.setEnabled(False)
        self.old_remote_filename = old_remote_filename
        # центрируем относительно родительского окна
        self.move(int(self.parent.x() + (self.parent.width() - self.width())/2), int(self.parent.y() + (self.parent.height() - self.height())/2))
        

        self.filename_lbl = QLabel(self)
        self.filename_lbl.setText("Файл: " + old_remote_filename)
        self.filename_lbl.move(10, 10)

        self.new_priority_lbl = QLabel(self)
        self.new_priority_lbl.setText("Новое имя файла:")
        self.new_priority_lbl.move(10, 50)

        self.new_name_line = QLineEdit(self)
        self.new_name_line.resize(160, 20)
        self.new_name_line.move(180, 48)

        self.message_lbl = QLabel(self)
        self.message_lbl.setText("")
        self.message_lbl.move(10, 105)
        self.message_lbl.resize(330, 90)
        self.message_lbl.setWordWrap(True)
        self.message_lbl.setFont(QFont('SansSerif', 8))

        self.advanced_message_lbl = QLabel(self)
        self.advanced_message_lbl.setText("")
        self.advanced_message_lbl.move(10, 205)
        self.advanced_message_lbl.resize(330, 85)
        self.advanced_message_lbl.setWordWrap(True)
        self.advanced_message_lbl.setFont(QFont('SansSerif', 8))

        self.set_priority_btn = QPushButton(self)
        self.set_priority_btn.setText("Задать имя")
        self.set_priority_btn.resize(QSize(160, 30))
        self.set_priority_btn.move(100, 80)
        self.set_priority_btn.clicked.connect(self.change_name_of_file)
        pass

    def change_name_of_file(self):
        self.message_lbl.setText("")
        self.advanced_message_lbl.setText("")
        if self.new_name_line.text().startswith("/") or self.new_name_line.text().startswith("."):
            self.message_lbl.setText("Ошибка! Недопустимое имя файла.")
            return

        result = self.parent.ftp_client.rename_remote_file(self.old_remote_filename, self.new_name_line.text())
        print(result)
        if result == True:
            self.close()
            self.parent.setEnabled(True)
        else:
            self.message_lbl.setText("Ошибка! При смене имени файла произошла ошибка. Попробуйте ещё раз. Возможные причины: \n-файл сейчас участвует в обмене;\n-неверное имя файла;\n-файл с таким именем уже существует;\n-у Вас недостаточно прав доступа;")
            self.advanced_message_lbl.setText("Подробнее:" + str(result))
        pass

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.local_cwd = os.path.abspath(os.path.curdir)
        os.chdir(self.local_cwd)
        self.initUI()
        self.connect_window = None
        self.change_priority_window = None
        self.create_new_directory_window = None
        self.rename_remote_file_window = None
        self.ftp_client = None
        self.connected_to_server = False
        self.flag_of_refreshing_bars = True
        self.thread_for_refreshing_bars = threading.Thread()
        self.thread_for_refreshing_bars ._target = self.refresh_all_progress_bars
        self.args = ()
        self.thread_for_refreshing_bars.start()
        self.lock_for_refreshing_bars = threading.Lock()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.resize(1280, 600)
        self.center()
        self.setWindowTitle('Параллельный двунаправленный приоритетный FTP-клиент')
        self.file_icon = QIcon('file.png')
        self.folder_icon = QIcon('folder.png')

        # зададим шрифт подсказкам
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setFont(QFont('SansSerif', 13))

        # инициализируем кнопки "подключиться" и "отключиться" и "восстановить работу из истории"
        self.connect_btn = QPushButton(self)
        self.connect_btn.setText("Подключиться")
        self.connect_btn.resize(QSize(160, 30))
        self.connect_btn.move(10, 10)
        self.connect_btn.clicked.connect(self.init_connect_window)

        self.disconnect_btn = QPushButton(self)
        self.disconnect_btn.setText("Отключиться")
        self.disconnect_btn.resize(QSize(160, 30))
        self.disconnect_btn.move(180, 10)
        self.disconnect_btn.clicked.connect(self.disconnect_from_server)

        self.renew_history_btn = QPushButton(self)
        self.renew_history_btn.setText("Восстановить работу из истории")
        self.renew_history_btn.resize(QSize(340, 30))
        self.renew_history_btn.move(350, 10)
        self.renew_history_btn.clicked.connect(self.renew_history)
        self.renew_history_btn.setEnabled(False)
        

        # локальнная файловая система
        self.local_file_list_widget = QTreeWidget(self)
        self.local_file_list_widget.setHeaderLabels([' ', 'Имя', 'Размер'])
        self.local_file_list_widget.resize(250, 500)
        self.local_file_list_widget.move(10, 50)
        self.local_file_list_widget.setIconSize(QSize(20, 20))
        self.local_file_list_widget.setColumnWidth(0, 45)
        self.local_file_list_widget.itemDoubleClicked.connect(self.dbl_click_on_local_file_list)
        self.local_file_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.local_file_list_widget.customContextMenuRequested.connect(self.open_context_menu_for_local_file_list_widget)


        # удалённая файловая система
        self.remote_file_list_widget = QTreeWidget(self)
        self.remote_file_list_widget.setHeaderLabels([' ', 'Имя', 'Размер'])
        self.remote_file_list_widget.resize(250, 500)
        self.remote_file_list_widget.move(1020, 50)
        self.remote_file_list_widget.setIconSize(QSize(20, 20))
        self.remote_file_list_widget.setColumnWidth(0, 45)
        self.remote_file_list_widget.itemDoubleClicked.connect(self.dbl_click_on_remote_file_list)
        self.remote_file_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.remote_file_list_widget.customContextMenuRequested.connect(self.open_context_menu_for_remote_file_list_widget)

        # прогресс-бары по центру
        self.progress_widget = QTreeWidget(self)
        self.progress_widget.setHeaderLabels(['Имя', 'Прогресс', 'Размер', 'Направление', 'Статус', 'Приоритет', 'Полный локальный путь'])
        self.progress_widget.resize(740, 500)
        self.progress_widget.move(270, 50)
        self.progress_widget.setIconSize(QSize(20, 20))
        self.progress_widget.setColumnWidth(0, 120)
        self.progress_widget.setColumnWidth(1, 140)
        self.progress_widget.setColumnWidth(2, 80)
        self.progress_widget.setColumnWidth(3, 90)
        self.progress_widget.setColumnWidth(4, 80)
        self.progress_widget.setColumnWidth(5, 80)
        self.progress_widget.setColumnWidth(6, 90)
        self.progress_widget.setFont(QFont('SansSerif', 8))
        # self.remote_file_list_widget.itemDoubleClicked.connect(self.dbl_click_on_remote_file_list)
        self.progress_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.progress_widget.customContextMenuRequested.connect(self.open_context_menu_for_loading)
        self.progress_bars = {}

        self.refresh_local_file_list()

        self.show()
        pass

    def renew_history(self):
        if self.connected_to_server == False:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка восстановления.")
            msg.setInformativeText("Нельзя восстановить работу, так как отсутствует подключение к серверу!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return
        try:
            self.renew_history_btn.setEnabled(False)
            self.ftp_client.renew_all_loads_from_history()
            time.sleep(1) # нужно дождаться, пока контрольный цикл загрузок\выгрузок закончит текущий "цикл передачи" и дойдёт до синхронизации добавленных загрузок\выгрузок
            self.refresh_progress_widget_from_ftp_client()
            
        except:
            raise
        pass

    def refresh_progress_widget_from_ftp_client(self):
        if self.connected_to_server == False:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка восстановления.")
            msg.setInformativeText("Нельзя восстановить работу, так как отсутствует подключение к серверу!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return
        self.ftp_client.stop_control()

        self.progress_bars.clear()
        self.progress_widget.clear()

        # выгрузки
        for uploading_number in self.ftp_client.upload_files.items():
            uploading_progress_item = QTreeWidgetItem(self.progress_widget)
            uploading_progress_item.setText(0, self.ftp_client.upload_files[uploading_number[0]]['local_filename'])
            uploading_progress_item.setText(2, format(self.ftp_client.upload_files[uploading_number[0]]['local_file_size'] / 1024 / 1024, ".1f") + " MB")
            uploading_progress_item.setText(3, "Выгрузка")
            uploading_progress_item.setText(4, StatusOfLoading.PROCESS.value)
            uploading_progress_item.setText(5, str(self.ftp_client.upload_files[uploading_number[0]]['priority']))
            uploading_progress_item.setText(6, self.ftp_client.upload_files[uploading_number[0]]['full_path_to_local_file'])
            pb = QProgressBar(self.progress_widget)
            pb.setGeometry(0, 0, 100, 10)
            pb.setValue(0)
            self.progress_widget.setItemWidget(uploading_progress_item, 1, pb)
            self.progress_bars[self.ftp_client.upload_files[uploading_number[0]]['full_path_to_local_file'] + '_up'] = pb

        # загрузки
        for downloading_number in self.ftp_client.download_files.items():
            downloading_progress_item = QTreeWidgetItem(self.progress_widget)
            downloading_progress_item.setText(0, str(self.ftp_client.download_files[downloading_number[0]]['remote_filename']))
            downloading_progress_item.setText(2, format(self.ftp_client.download_files[downloading_number[0]]['remote_file_size'] / 1024 / 1024, ".1f") + " MB")
            downloading_progress_item.setText(3, "Загрузка")
            downloading_progress_item.setText(4, StatusOfLoading.PROCESS.value)
            downloading_progress_item.setText(5, str(self.ftp_client.download_files[downloading_number[0]]['priority']))
            downloading_progress_item.setText(6, self.ftp_client.download_files[downloading_number[0]]['full_path_to_local_file'])
            pb = QProgressBar(self.progress_widget)
            pb.setGeometry(0, 0, 100, 10)
            pb.setValue(0)
            self.progress_widget.setItemWidget(downloading_progress_item, 1, pb)
            self.progress_bars[self.ftp_client.download_files[downloading_number[0]]['full_path_to_local_file'] + '_down'] = pb
        self.ftp_client.start_control()
        pass

    def refresh_all_progress_bars(self):
        while self.flag_of_refreshing_bars:
            # print("yaeh")
            if not self.connected_to_server:
                time.sleep(1)
                continue
            try: # словарь может менять размер в процессе обработки, поэтому будет вылетать RuntimeError
                # print("-DOWNLOADINGS-")
                for down_file_number in self.ftp_client.download_files:
                    # print(self.ftp_client.download_files[down_file_number]['remote_filename'] + "  " + format(self.ftp_client.download_files[down_file_number]['local_file_size'] / self.ftp_client.download_files[down_file_number]['remote_file_size'] * 100, ".1f"))
                    try:
                        self.lock_for_refreshing_bars.acquire()
                        if str(self.ftp_client.download_files[down_file_number]['full_path_to_local_file'] + '_down') in self.progress_bars.keys():
                            self.progress_bars[self.ftp_client.download_files[down_file_number]['full_path_to_local_file'] + '_down'].setValue(int(self.ftp_client.download_files[down_file_number]['local_file_size'] / self.ftp_client.download_files[down_file_number]['remote_file_size'] * 100))
                        self.lock_for_refreshing_bars.release()
                    except KeyError:
                        # raise
                        pass
                    except RuntimeError:
                        pass
                # print("-UPLOADINGS-")
                for up_file_number in self.ftp_client.upload_files:
                    # print(self.ftp_client.upload_files[up_file_number]['local_filename'] + "  " + format(self.ftp_client.upload_files[up_file_number]['remote_file_size'] / self.ftp_client.upload_files[up_file_number]['local_file_size'] * 100, ".1f"))
                    try:
                        self.lock_for_refreshing_bars.acquire()
                        if str(self.ftp_client.upload_files[up_file_number]['full_path_to_local_file'] + '_up') in self.progress_bars.keys():
                            self.progress_bars[self.ftp_client.upload_files[up_file_number]['full_path_to_local_file'] + '_up'].setValue(int(self.ftp_client.upload_files[up_file_number]['remote_file_size'] / self.ftp_client.upload_files[up_file_number]['local_file_size'] * 100))
                        self.lock_for_refreshing_bars.release()
                    except KeyError:
                        # raise
                        pass
                    except RuntimeError:
                        pass
                time.sleep(1)
            except RuntimeError:
                time.sleep(0.5)
                pass
        pass

    def open_context_menu_for_loading(self, position):
        if self.progress_widget.itemAt(position) == None:
            return
        clicked_item = self.progress_widget.itemAt(position)
        menu = QMenu()
        change_pr_menu_action = QAction('Сменить приоритет', menu)
        change_pr_menu_action.triggered.connect(lambda: self.init_change_priority_window(os.path.abspath(clicked_item.text(6)), clicked_item.text(5)))
        menu.addAction(change_pr_menu_action)

        continue_loading_menu_action = QAction('Продолжить обмен', menu)
        continue_loading_menu_action.setEnabled(False)
        if clicked_item.text(4) == StatusOfLoading.PAUSED.value:
            continue_loading_menu_action.triggered.connect(lambda: self.continue_loading(clicked_item))
            continue_loading_menu_action.setEnabled(True)
        menu.addAction(continue_loading_menu_action)

        pause_loading_menu_action = QAction('Приостановить обмен', menu)
        pause_loading_menu_action.setEnabled(False)
        if clicked_item.text(4) == StatusOfLoading.PROCESS.value:
            pause_loading_menu_action.triggered.connect(lambda: self.pause_loading(clicked_item))
            pause_loading_menu_action.setEnabled(True)
        menu.addAction(pause_loading_menu_action)

        remove_loading_menu_action = QAction('Удалить обмен', menu)
        remove_loading_menu_action.triggered.connect(lambda: self.remove_loading(clicked_item))
        menu.addAction(remove_loading_menu_action)

        menu.exec_(self.progress_widget.viewport().mapToGlobal(position))
        pass

    def continue_loading(self, clicked_item):
        full_path_to_local_file = clicked_item.text(6)
        flag_continued_downloading = self.ftp_client.continue_downloading(full_path_to_local_file)
        flag_continued_uploading = False
        if flag_continued_downloading == False:
            flag_continued_uploading = self.ftp_client.continue_uploading(full_path_to_local_file)
        else:
            pass
        if flag_continued_downloading or flag_continued_uploading:
            items_found = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
            if len(items_found) != 0:
                items_found[0].setText(4, StatusOfLoading.PROCESS.value)
                return
                pass
            else:
                pass
        else:
            pass
        if flag_continued_downloading == False and flag_continued_uploading == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка продолжения загрузки/выгрузки.")
            msg.setInformativeText("Данную загрузку/выгрузку файла продолжить невозможно. Попробуйте снова.")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
        pass

    def pause_loading(self, clicked_item):
        full_path_to_local_file = clicked_item.text(6)
        flag_paused_downloading = self.ftp_client.pause_downloading(full_path_to_local_file)
        flag_paused_uploading = False
        if flag_paused_downloading == False:
            flag_paused_uploading = self.ftp_client.pause_uploading(full_path_to_local_file)
        else:
            pass
        if flag_paused_downloading or flag_paused_uploading:
            items_found = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
            if len(items_found) != 0:
                items_found[0].setText(4, StatusOfLoading.PAUSED.value)
                return
                pass
            else:
                pass
        else:
            pass
        if flag_paused_downloading == False and flag_paused_uploading == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка приостановки загрузки/выгрузки.")
            msg.setInformativeText("Данную загрузку/выгрузку файла приостановить невозможно. Попробуйте снова.")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
        pass

    def open_context_menu_for_local_file_list_widget(self, position):
        if self.local_file_list_widget.itemAt(position) == None:
            menu = QMenu()
            addDes = QAction('Обновить', menu)
            addDes.triggered.connect(lambda: self.refresh_local_file_list())
            menu.addAction(addDes)
            menu.exec_(self.local_file_list_widget.viewport().mapToGlobal(position))
            return
        flag_of_found_file = False
        for file_or_dir in os.listdir(self.local_cwd):
            pathname = os.path.join(self.local_cwd, file_or_dir) # pathname - полный путь к файлу с именем
            file_prop = fileProperty(pathname)
            if file_prop.Name == str(self.local_file_list_widget.itemAt(position).text(1)):
                if file_prop.Mode.startswith('d'):
                    # попытка вызвать контекстное меню на папке
                    pass
                else:
                    flag_of_found_file = True
                    pass
        if not flag_of_found_file:
            return
        menu = QMenu()
        upload_action = QAction('Закачать файл на сервер', menu)
        upload_action.triggered.connect(lambda: self.upload_file_on_server(os.path.abspath(self.local_file_list_widget.itemAt(position).text(1))))
        menu.addAction(upload_action)

        remove_action = QAction('Удалить файл', menu)
        remove_action.triggered.connect(lambda: self.remove_local_file(self.local_file_list_widget.itemAt(position)))
        menu.addAction(remove_action)

        menu.exec_(self.local_file_list_widget.viewport().mapToGlobal(position))
        pass

    def open_context_menu_for_remote_file_list_widget(self, position):
        if self.connected_to_server == False:
            return
        if self.remote_file_list_widget.itemAt(position) == None:
            menu = QMenu()
            refresh_menu_action = QAction('Обновить', menu)
            refresh_menu_action.triggered.connect(lambda: self.ftp_client.refresh_remote_file_list())
            menu.addAction(refresh_menu_action)

            new_folder_menu_action = QAction('Создать папку', menu)
            new_folder_menu_action.triggered.connect(lambda: self.new_folder_window_init())
            menu.addAction(new_folder_menu_action)

            menu.exec_(self.remote_file_list_widget.viewport().mapToGlobal(position))
            return
        flag_of_found_file = False
        for file_or_dir in self.ftp_client.remoteFileList:
            if file_or_dir['filename'] == str(self.remote_file_list_widget.itemAt(position).text(1)):
                if file_or_dir['mode'].startswith('d'):
                    # попытка вызвать контекстное меню на папке
                    pass
                else:
                    flag_of_found_file = True
                    pass
        if not flag_of_found_file:
            return
        menu = QMenu()
        download_action = QAction('Скачать файл с сервера', menu)
        download_action.triggered.connect(lambda: self.download_file_from_server(self.remote_file_list_widget.itemAt(position).text(1)))
        menu.addAction(download_action)

        rename_action = QAction('Переименовать файл', menu)
        rename_action.triggered.connect(lambda: self.rename_remote_file_window_init(self.remote_file_list_widget.itemAt(position).text(1)))
        menu.addAction(rename_action)

        remove_action = QAction('Удалить файл', menu)
        remove_action.triggered.connect(lambda: self.remove_remote_file(self.remote_file_list_widget.itemAt(position)))
        menu.addAction(remove_action)

        menu.exec_(self.remote_file_list_widget.viewport().mapToGlobal(position))
        pass



    def remove_loading(self, clicked_item):
        full_path_to_local_file = clicked_item.text(6)
        flag_removed_downloading = self.ftp_client.stop_downloading(full_path_to_local_file)
        flag_removed_uploading = False
        if flag_removed_downloading == False:
            flag_removed_uploading = self.ftp_client.stop_uploading(full_path_to_local_file)
        else:
            pass
        if flag_removed_downloading or flag_removed_uploading:
            items_to_delete = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
            if len(items_to_delete) != 0:
                # self.progress_widget.removeChild(items_to_delete[0])
                self.progress_widget.takeTopLevelItem(self.progress_widget.indexOfTopLevelItem(items_to_delete[0]))
                return
                pass
            else:
                pass
        else:
            pass
        if flag_removed_downloading == False and flag_removed_uploading == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка удаления загрузки/выгрузки.")
            msg.setInformativeText("Данную загрузку/выгрузку файла удалить (остановить) невозможно. Попробуйте снова.")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
        pass

    def remove_local_file(self, clicked_item):
        absolute_path = os.path.abspath(clicked_item.text(1))
        items_with_this_path_in_progress = self.progress_widget.findItems(absolute_path, Qt.MatchCaseSensitive, 6)
        if len(items_with_this_path_in_progress) != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка удаления файла.")
            msg.setInformativeText("Файл нельзя удалить, так как он участвует в обмене!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return
            # self.progress_widget.takeTopLevelItem(self.progress_widget.indexOfTopLevelItem(items_to_delete[0]))
        os.remove(absolute_path)
        self.refresh_local_file_list()
        pass

    def remove_remote_file(self, clicked_item):
        try:
            result = self.ftp_client.remove_remote_file(clicked_item.text(1))
            print(result)
        except ftplib.Error:
            # вывести сообщение о том, что файл участвует в обмене и его нельзя удалить
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка удаления файла.")
            msg.setInformativeText("Файл нельзя удалить, так как он участвует в обмене! Так же возможны другие причины..")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
        pass

    def upload_file_on_server(self, local_path):
        # print("Upload: " + local_path)
        if self.connected_to_server == False:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка выгрузки файла.")
            msg.setInformativeText("Файл нельзя выгрузить, так как отсутствует подключение к серверу!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return

        items_alredy_in_loadings = self.progress_widget.findItems(local_path, Qt.MatchCaseSensitive, 6)
        if len(items_alredy_in_loadings) != 0:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка выгрузки файла.")
            msg.setInformativeText("Файл нельзя выгрузить, так как он уже участвует в обмене!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return
            pass
        else:
            pass

        uploading = self.ftp_client.upload(local_path, 1)
        if uploading != None:
            uploading_progress_item = QTreeWidgetItem(self.progress_widget)
            uploading_progress_item.setText(0, uploading['local_filename'])
            uploading_progress_item.setText(2, format(uploading['local_file_size'] / 1024 / 1024, ".1f") + " MB")
            uploading_progress_item.setText(3, "Выгрузка")
            uploading_progress_item.setText(4, StatusOfLoading.PROCESS.value)
            uploading_progress_item.setText(5, '1')
            uploading_progress_item.setText(6, uploading['full_path_to_local_file'])
            pb = QProgressBar(self.progress_widget)
            pb.setGeometry(0, 0, 100, 10)
            pb.setValue(0)
            self.progress_widget.setItemWidget(uploading_progress_item, 1, pb)
            self.progress_bars[uploading['full_path_to_local_file'] + '_up'] = pb
        pass

    def download_file_from_server(self, remote_filename):
        # print("Download: " + remote_filename)
        if self.connected_to_server == False:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка загрузки файла.")
            msg.setInformativeText("Файл нельзя загрузить, так как отсутствует подключение к серверу!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return

        items_alredy_in_loadings = self.progress_widget.findItems(remote_filename, Qt.MatchCaseSensitive, 0)
        if len(items_alredy_in_loadings) != 0:
            # вывести сообщение о том, что неободимо сначала подключиться к серверу
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            # msg.setIconPixmap(pixmap)  # Своя картинка
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка загрузки файла.")
            msg.setInformativeText("Файл нельзя загрузить, так как он уже участвует в обмене!")
            okButton = msg.addButton('ОК', QMessageBox.AcceptRole)
            # msg.addButton('Отмена', QMessageBox.RejectRole)
            msg.exec()
            return
            pass
        else:
            pass

        downloading = self.ftp_client.download(remote_filename, "", 1)
        if downloading != None:
            downloading_progress_item = QTreeWidgetItem(self.progress_widget)
            downloading_progress_item.setText(0, remote_filename)
            downloading_progress_item.setText(2, format(downloading['remote_file_size'] / 1024 / 1024, ".1f") + " MB")
            downloading_progress_item.setText(3, "Загрузка")
            downloading_progress_item.setText(4, StatusOfLoading.PROCESS.value)
            downloading_progress_item.setText(5, '1')
            downloading_progress_item.setText(6, downloading['full_path_to_local_file'])
            pb = QProgressBar(self.progress_widget)
            pb.setGeometry(0, 0, 100, 10)
            pb.setValue(0)
            self.progress_widget.setItemWidget(downloading_progress_item, 1, pb)
            self.progress_bars[downloading['full_path_to_local_file'] + '_down'] = pb
        pass


    def refresh_local_file_list(self):
        self.local_file_list_widget.clear()
        parent_dir_item = QTreeWidgetItem(self.local_file_list_widget)
        parent_dir_item.setText(1, '.')
        parent_dir_item.setText(2, '')
        parent_dir_item.setIcon(0, self.folder_icon)
        for f in os.listdir(self.local_cwd): # f - имя файла
            pathname = os.path.join(self.local_cwd, f) # pathname - полный путь к файлу с именем
            file_prop = fileProperty(pathname)
            item = QTreeWidgetItem(self.local_file_list_widget)
            item.setText(1, file_prop.Name)
            item.setText(2, file_prop.Size)
            if file_prop.Mode.startswith('d'):
                icon = self.folder_icon
            else:
                icon = self.file_icon
            item.setIcon(0, icon)  
        pass

    def refresh_remote_file_list(self, remote_file_list):
        self.remote_file_list_widget.clear()
        parent_dir_item = QTreeWidgetItem(self.remote_file_list_widget)
        parent_dir_item.setText(1, '.')
        parent_dir_item.setText(2, '')
        parent_dir_item.setIcon(0, self.folder_icon)
        for file in remote_file_list:
            item = QTreeWidgetItem(self.remote_file_list_widget)
            item.setText(1, file['filename'])
            item.setText(2, file['size'])
            if file['mode'].startswith('d'):
                icon = self.folder_icon
            else:
                icon = self.file_icon
            item.setIcon(0, icon)


    def init_connect_window(self):
        self.callback_methods_for_client = {'refresh_file_list' : self.refresh_remote_file_list,
        'file_uploaded' : self.file_uploaded,
        'file_downloaded' : self.file_downloaded,
        'priority_changed' : self.priority_of_loading_changed }
        self.connect_window = ConnectWindow(self, self.callback_methods_for_client)
        self.connect_window.show()
        pass

    def init_change_priority_window(self, full_path_to_local_file, old_priority):
        self.change_priority_window = ChangePriorityWindow(self, full_path_to_local_file, old_priority)
        self.change_priority_window.show()
        pass

    def new_folder_window_init(self):
        self.create_new_directory_window = NewFolderWindow(self)
        self.create_new_directory_window.show()
        pass

    def rename_remote_file_window_init(self, remote_filename):
        self.rename_remote_file_window = RenameRemoteFileWindow(self, remote_filename)
        self.rename_remote_file_window.show()
        pass


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dbl_click_on_local_file_list(self, item, column_no):
        if item.text(1) == '.':
            # print("Нажал на корневую директорию")
            try:
                self.local_cwd = os.path.split(self.local_cwd)[0]
                os.chdir(self.local_cwd)
                self.refresh_local_file_list()
            except:
                raise
        elif os.path.isdir(os.path.join(self.local_cwd, item.text(1))):
            # нажал на папку
            try:
                self.local_cwd = os.path.join(self.local_cwd, item.text(1))
                os.chdir(self.local_cwd)
                self.refresh_local_file_list()
            except:
                raise
        else:
            # print("Нажал на файл")
            pass

    def dbl_click_on_remote_file_list(self, item, column_no):
        text_of_item = str(item.text(1))
        if text_of_item == '.':
            # print("Нажал на корневую директорию")
            try:
                self.ftp_client.cd_to_remote_parent_directory()
            except:
                raise
        else:
            flag_of_found_file_or_directory = False
            for file_or_dir in self.ftp_client.remoteFileList:
                if file_or_dir['filename'] == text_of_item:
                    flag_of_found_file_or_directory = True
                    if file_or_dir['mode'].startswith('d'):
                        self.ftp_client.cd_to_remote_directory(text_of_item)
                    else:
                        # дважды кликнули по файлу, а не по папке
                        pass
            if not flag_of_found_file_or_directory:
                # вывести сообщение о том, что такой файл или папка на сервере не найдены
                pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтвердите действие', 'Вы уверены в том, что хотите выйти?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # закрыть и сохранить все загрузки и выгрузки, а так же все подключения перед выходом
            # self.disconnect_from_server()
            if self.connected_to_server:
                self.ftp_client.stop_and_save_loads_before_exiting()
                self.connected_to_server = False
            self.flag_of_refreshing_bars = False
            if self.connect_window != None:
                self.connect_window.close()
                self.connect_window = None
            if self.change_priority_window != None:
                self.change_priority_window.close()
                self.change_priority_window = None
            if self.create_new_directory_window != None:
                self.create_new_directory_window.close()
                self.create_new_directory_window = None
            if self.rename_remote_file_window != None:
                self.rename_remote_file_window.close()
                self.rename_remote_file_window = None
            event.accept()
        else:
            event.ignore()

    def disconnect_from_server(self):
        if self.connected_to_server:
            self.ftp_client.stop_and_save_loads_before_exiting()
            self.connected_to_server = False
            self.renew_history_btn.setEnabled(False)
        self.remote_file_list_widget.clear()


        self.progress_widget.clear()
        self.progress_bars.clear()


        self.connect_btn.setEnabled(True)
        self.refresh_local_file_list()
        pass

    def file_uploaded(self, full_path_to_local_file):
        # print("File " + full_path_to_local_file + " has been uploaded on server!")


        self.progress_bars.pop(full_path_to_local_file + "_up")


        items_to_delete = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
        if len(items_to_delete) != 0:
            # self.progress_widget.removeChild(items_to_delete[0])
            self.progress_widget.takeTopLevelItem(self.progress_widget.indexOfTopLevelItem(items_to_delete[0]))
        pass

    def file_downloaded(self, full_path_to_local_file):
        # print("File " + full_path_to_local_file + " has been downloaded from server!")

        self.lock_for_refreshing_bars.acquire()
        self.progress_bars.pop(full_path_to_local_file + "_down")


        items_to_delete = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
        if len(items_to_delete) != 0:
            # self.progress_widget.removeChild(items_to_delete[0])
            self.progress_widget.takeTopLevelItem(self.progress_widget.indexOfTopLevelItem(items_to_delete[0]))
        self.lock_for_refreshing_bars.release()
        self.refresh_local_file_list()
        pass

    def priority_of_loading_changed(self, full_path_to_local_file, new_priority):
        items_found = self.progress_widget.findItems(full_path_to_local_file, Qt.MatchCaseSensitive, 6)
        if len(items_found) != 0:
            items_found[0].setText(5, str(new_priority))
        pass

    def test_print(self):
        print("Test print!")
        
if __name__ == '__main__':
    logging.basicConfig(filename = os.path.curdir + "/ftp_client.log", level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
    logging.info("\n\n\n===START===")
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
    
    
