import csv
from os.path import isfile, join, basename

class Report:
    def __init__(self, scan_result=[]):
       if(scan_result):
            self.scan_result = scan_result
            self.calculate_report()

    def import_scan_results(self, csv_sources):
        """Импорт результатов сканрирования из csv файлов
        
        Arguments:
            csv_sources {list} -- Список csv файлов для сканирования
        """        
        self.scan_result = []
        for csv_source in csv_sources:
            with open(csv_source) as source:
                readCSV = csv.reader(source, delimiter=';')

                for row in readCSV:
                    file_name = basename(source.name).split(".")[0]
                    user_row = row
                    user_row = {'UserID': file_name,
                                'ID': row[0], 'FileName': row[1], 'FileSize': row[2], 'IsVirus': row[3]}
                    self.scan_result.append(user_row)
        self.calculate_report()
            
    def csv_scan(self, scan_file ='scan.csv'):
        """Экспорт результатов сканирования в CSV
        
        Keyword Arguments:
            scan_file {str} -- [description] (default: {'scan.csv'})
        """        
        csv_cols = ['UserID', 'ID', 'FileName', 'FileSize', 'IsVirus']
        with open(scan_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=csv_cols)
            writer.writeheader()
            for data in self.scan_result:
                writer.writerow(data)

    def csv_report(self, report_file ='report.csv'):
        """Экспорт финального отчёта в CSV
        
        Keyword Arguments:
            report_file {str} -- [description] (default: {'report.csv'})
        """        
        csv_cols = ['ID', 'UserCount', 'FileCount',
                    'UserVirusCount', 'VirusCount']
        flatten_report = []
        for file_id, report in self.total_report.items():
            flatten_report.append({
                'ID': file_id,
                'UserCount': report['UserCount'],
                'FileCount': report['FileCount'],
                'UserVirusCount': report['UserVirusCount'],
                'VirusCount': report['VirusCount']
            })      
        with open(report_file, 'w', newline='') as csvfile: 
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=csv_cols)
            writer.writeheader()
            for data in flatten_report:
                writer.writerow(data)

    # def csv_report:

    def calculate_report(self):
        self.total_report = {}
        users_files = {}

        for scan in self.scan_result:
            if scan["UserID"] not in users_files:
                users_files[scan["UserID"]] = {}

            # Инициализация полей
            if scan["ID"] not in self.total_report:
                self.total_report[scan["ID"]] = {
                    'UserCount': 0,
                    'UserVirusCount': 0,
                    'FileCount': 0,
                    'VirusCount': 0,
                }

            if scan["ID"] not in users_files[scan["UserID"]]:
                users_files[scan["UserID"]][scan["ID"]] = {'infected': False }    
                self.total_report[scan["ID"]]["UserCount"] += 1
                if int(scan["IsVirus"]):
                    self.total_report[scan["ID"]]["UserVirusCount"] += 1
                    users_files[scan["UserID"]][scan["ID"]]['infected'] = True
                
            self.total_report[scan["ID"]]["FileCount"] += 1
            if int(scan["IsVirus"]):
                self.total_report[scan["ID"]]["VirusCount"] += 1
                if scan["ID"] in users_files[scan["UserID"]] and not users_files[scan["UserID"]][scan["ID"]]["infected"]:
                    users_files[scan["UserID"]][scan["ID"]] = {'infected': True}
                    self.total_report[scan["ID"]]["UserVirusCount"] += 1

    