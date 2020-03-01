import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий

from PyQt5 import QtWidgets
from report import Report
import windows  # Это наш конвертированный файл дизайна

class App(QtWidgets.QMainWindow, windows.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.report = Report()
        self.pushButton.clicked.connect(self.import_csv)
        self.pushButton_2.clicked.connect(self.export_scan)
        self.pushButton_3.clicked.connect(self.export_report)

        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)

        # self.btnBrowse.clicked.connect(self.browse_folder)  # Выполнить функцию browse_folder
                                                            # при нажатии кнопки

    def import_csv(self):
        self.listWidget.clear()
        file_paths = QtWidgets.QFileDialog.getOpenFileNames(self)
        print("FILE PATHS", file_paths)
        if file_paths[0]:
            for file_path in file_paths[0]:
                self.listWidget.addItem(os.path.relpath(file_path))
        self.report.import_scan_results(file_paths[0])
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
    
    def export_scan(self):
       save_path = QtWidgets.QFileDialog.getSaveFileName(self)
       if(save_path):
            print("PATH TO SAVE REPORT", save_path[0])
            self.report.csv_scan(save_path[0])
            QtWidgets.QMessageBox.information(self, "Сохранение сканировния", "Результаты сканирования успешно сохранены: "+ save_path[0])

    
    def export_report(self):
       save_path = QtWidgets.QFileDialog.getSaveFileName(self)
       if(save_path):
            print("PATH TO SAVE REPORT", save_path[0])
            self.report.csv_report(save_path[0])
            QtWidgets.QMessageBox.information(self, "Сохранение отчёта", "Результаты отчёта успешно сохранены: "+ save_path[0])
        

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()