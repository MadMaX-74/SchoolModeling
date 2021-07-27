# -*- coding: utf-8 -*-
import os
import jsonpickle

jsonpickle.set_encoder_options('json', indent=4, separators=(',', ': '), ensure_ascii=False)
file_name = 'schools.json'

class FileProvider:
    def get(self, path):
        file = open(path, 'r')
        data = file.read()
        file.close()
        return data

    def append(self, path, data):
        file = open(path, 'a')
        data = file.write(data)
        file.close()

    def writelines(self, path, data):
        file = open(path, 'w')
        data = file.write(data)
        file.close()

    def exists(self, path):
        return os.path.exists(path)

    def clear(self, path):
        file = open(path, 'w')
        file.write("")
        file.close()




class School:
    def __init__(self, name, adress):
        self.name = name
        self.adress = adress
        self.students = []


class Storage:
    def __init__(self, path):
        self.file_path = path

    def get_all(self):
        if not file_provider.exists(self.file_path):
            schools = []
            self.safe_data(schools)

        data = file_provider.get(self.file_path)
        schools = jsonpickle.decode(data)
        return schools

    def add_data(self, school):
        schools = self.get_all()
        schools.append(school)
        self.safe_data(schools)

    def safe_data(self, schools):
        json_data = jsonpickle.encode(schools)
        file_provider.writelines(self.file_path, json_data)

    def edit_data(self, schools_list):
        schools = self.get_all()
        schools = schools_list
        self.safe_data(schools)

class Student:
    def __init__(self, name, age, class_number):
        self.name = name
        self.age = age
        self.class_number = class_number


file_provider = FileProvider()
storage = Storage(file_name)

def choose_school():
    school_list = storage.get_all()
    for i in range(len(school_list)):
        print(f'{i + 1}.{school_list[i].name:15}')
    while True:
        user_input = input('\n')
        if not user_input.isdigit() or user_input == '' or user_input == ' ':
            print('Вы ввели не число')
            continue
        if int(user_input) > len(school_list):
            print('Вы ввели число не соответсвующее колличеству школ')
            print('Введите ещё раз:')
            continue
        break

    index = int(user_input) - 1
    return index

while True:
    print('Выберите что вы хотите сделать:')
    print("1. Добавить данные о новой школе:")
    print("2. Получение полной информации о школе:")
    print("3. Изменение информации о школе")
    print("4. Просмотр учеников школы в виде таблицы")
    print("5. Добавление нового ученика школы")
    print("6. Удаление имеющегося ученика школы")
    print("0. выйти из программы")
    cmd = input("Выберите пункт: ")

    if cmd == "1":
        print('Давайте введем информацио о школе')
        while True:
            name = input('Введите название школы \n')
            if name == '':
                print('Вы ввели пустую строку')
                continue
            else:
                break
        while True:
            adress = input('Введите адресс школы \n')
            if adress == '':
                print('Вы ввели пустую строку')
                continue
            else:
                break
        school = School(name, adress)
        storage.add_data(school)
    elif cmd == "2":
        print('Выберите школу о которой хотите получить информацию:')
        school_list = storage.get_all()
        index = choose_school()
        name = 'Название школы'
        adress = 'Адресс школы'
        students_amount = 'Кол-во учеников'
        print(f'{name:15}{adress:15}{students_amount:10}')
        counter = len(school_list[index].students)
        print(f'{school_list[index].name:15}{school_list[index].adress:15}{counter:10}')

    elif cmd == "3":
        print('Выберите школу которую хотите изменить')
        school_list = storage.get_all()
        index = choose_school()
        while True:
            school_list[index].name = input('Введите новое название \n')
            if school_list[index].name == '' or school_list[index].adress == ' ':
                print('Вы ввели пустую строку')
                continue
            break
        while True:
            school_list[index].adress = input('Введите новый адресс \n')
            if school_list[index].adress == '' or school_list[index].adress == ' ':
                print('Вы ввели пустую строку')
                continue
            break
        storage.edit_data(school_list)
    elif cmd == "4":
        print('Выберите школу в которой хотите посмотреть учеников')
        school_list = storage.get_all()
        index = choose_school()
        name = 'Имя ученика'
        age = 'Возраст'
        class_number = 'Номер класса'
        print(f'{name:30}{age:10}{class_number:10}')
        students = school_list[index].students
        for i in range(len(students)):
            print(f'{i + 1}.{students[i].name:30}{students[i].age:10}{students[i].class_number:10}')
    elif cmd == "5":
        while True:
            student_name = input('Введите ФИО ученика \n')
            if student_name == '' or student_name == ' ':
                print('Вы ввели пустую строку')
                continue
            break
        while True:
            student_age = input('Введите возраст ученика \n')
            if student_age == '' or student_age == ' ' or not student_age.isdigit():
                print('Вы ввели некоректные данные')
                continue
            if int(student_age) > 20:
                print('Некорректный возраст ученика. Введите ещё раз:')
                continue
            break
        while True:
            class_number = input('Введите номер класса \n')
            if class_number == '' or class_number == ' ' or not class_number.isdigit():
                print('Вы ввели некоректные данные')
                continue
            if int(class_number) > 12:
                print('Некорректный класс ученика, в школе всего 12 классов. Введите ещё раз:')
                continue
            break
        new_student = Student(student_name, student_age, class_number)
        print('Выберите школу в которую хотите добавить ученика')
        school_list = storage.get_all()
        index = choose_school()
        school_list[index].students.append(new_student)
        for i in range(len(school_list)):
            storage.edit_data(school_list)
    elif cmd == "6":
        print('Выберите школу в которой хотите удалить ученика')
        school_list = storage.get_all()
        index = choose_school()
        select_item = school_list[index]
        name = 'Имя ученика'
        age = 'Возраст'
        class_number = 'Номер класса'
        print(f'{name:15}{age:10}{class_number:10}')
        students = select_item.students
        for i in range(len(students)):
            print(f'{i + 1}.{students[i].name:15}{students[i].age:10}{students[i].class_number:10}')
        print('Выберите ученика')
        while True:
            user_select = input('\n')
            if not user_select.isdigit():
                print('Вы ввели не число')
                continue
            if int(user_select) > len(students):
                print('В данной школе такого студента нет. Введите номер студента ещё раз:')
                continue
            break
        select = int(user_select) - 1
        students.pop(select)
        for i in range(len(school_list)):
            storage.edit_data(school_list)
    elif cmd == "0":
        break
    else:
        print("Вы ввели не правильное значение")
    continue_programm = input('Повторим? 1/0 ')
    if (continue_programm.lower() == '1'):
        continue
    else:
        break
