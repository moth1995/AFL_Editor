import csv

class CSVFile:
    encoding = "utf-8"

    def __init__(self, file_location:str):
        self.__file_location = file_location

    @property
    def file_location(self):
        return self.__file_location

    @file_location.setter
    def file_location(self, valor:str):
        if valor != "":
            self.__file_location = valor
        else:
            raise ValueError("CSV file location can't be empty")

    def make(self,headers):
        """
        Creates the csv into the disk
        """
        with open(self.file_location, 'w', newline='', encoding=self.encoding) as csv_file:
            writer = csv.writer(csv_file, delimiter=',')            
            writer.writerow(headers)

    def to_file(self, rows:list, headers:list):
        """
        Receives a list, creates the csv using the method "make" and then writes the data
        """
        self.make(headers)
        with open(self.file_location, 'a', newline='', encoding=self.encoding) as csv_file:
            writer=csv.writer(csv_file, delimiter=',')
            for i in range(len(rows)):
                writer.writerow([i,rows[i]])
    def load(self):
        with open(self.file_location, 'r', encoding='utf-8') as csvf:
            # list to store the names of columns
            csv_reader = csv.reader(csvf, delimiter = ',')
            list_of_column_names = []
            for row in csv_reader:
                list_of_column_names = row
                break
            return [row for row in csv_reader if row != list_of_column_names]