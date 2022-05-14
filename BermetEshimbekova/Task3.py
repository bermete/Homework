# Task 4.3
from csv import reader, writer
from operator import itemgetter


def sort_students_by_key(file_path, k):
    with open(file_path) as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        header = next(csv_reader)
        students = [row for row in csv_reader]
    students = sorted(students, key=itemgetter(header.index(k)), reverse=True)
    return header, students


def get_top_performers(file_path, number_of_top_students=5):
    header, students = sort_students_by_key("../data/students.csv", 'average mark')
    return [i[0] for i in students[:number_of_top_students]]


def sort_students_by_age(source, destination):
    header, students = sort_students_by_key("../data/students.csv", 'age')
    with open(destination, 'w', newline='') as csv_file:
        csv_writer = writer(csv_file, delimiter=',')
        csv_writer.writerow(header)
        csv_writer.writerows(students)


print(get_top_performers("../data/students.csv"))
sort_students_by_age("../data/students.csv", "../data/sorted_students.csv")