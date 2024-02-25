from itertools import combinations  # комбинаторика
import sys  # выход по ошибке
from tabulate import tabulate

arr = ["avto", "zd", "mt"]  # массив первичных гипотез (переделать в ввод с клавиатуры)

mass = [0.00] * pow(2, len(arr))  # массив базовых вероятностей/масс гипотез


def combinations_to_matrix(arr):
    combinations_matrix = []
    n = len(arr)
    for r in range(1, n + 1):  # комбинации от 1 до n элементов
        combinations_matrix.extend(list(combinations(arr, r)))
    return combinations_matrix


def combinations_matrix_with_spaces(arr):
    combinations_matrix = combinations_to_matrix(arr)
    max_length = max(len(comb) for comb in combinations_matrix)
    combinations_matrix_with_spaces = []
    for combination in combinations_matrix:
        filled_combination = combination + (' ',) * (max_length - len(combination))
        combinations_matrix_with_spaces.append(filled_combination)
    return combinations_matrix_with_spaces

def check_intersection(list1, list2):

    set1=list1
    set2=list2
    if set1 & set2:
        return True
    else:
        return False


result = combinations_matrix_with_spaces(arr)

result.insert(0, "zero")  # нулевое событие

n = pow(2, len(arr))  # количесво всех комбинаций первичных гипотез

# #ввод масс
# print("Введите базовую вероятность/массу для гипотез:")
# for i in range(1, n):
#     print(result[i], ' = ')
#     element = float(input())  # запросите пользователя ввести элементы массива
#     mass[i] = element  # добавьте элемент в массив


mass = [0.0, 0.3, 0.2, 0.1, 0.4, 0.0, 0.0, 0.0]  # тестовые значений

# Проверка "Сумма базовых вероятностей/масс для всех подмножеств равна 1"
summ = 0.00
for i in mass:
    summ += i

if round(summ, 9) != 1.00:
    print("Ошибка!!! Сумма базовых вероятностей/масс не равна 1, а равнa =", summ)
    sys.exit(1)  # Выход из программы

# Вывод гипотез с базовыми вероятностями
print("Гипотезы с базовыми вероятностями/массами:")
for i in range(0, n):
    print(result[i], ' = ', mass[i])

# Рассчёт Bel()
bell = [0.00] * n  # массив значений функции доверия
for i in range(1, n):
    for j in range(1, len(arr)):
        if mass[i] != 0.0:
            if result[i][1] == ' ':
                bell[i] = mass[i]
                print("Bell(", result[i], ") = ", bell[i])
                break
            else:

                print("Bell(", result[i], ") = ", mass[i], end='')
                bell[i] += mass[i]

                for watch in range(0, len(arr)):
                    position = result[i][watch]

                    for y in range(1, n):
                        if result[y][0] == position and result[y][1] == " ":
                            bell[i] += mass[y]
                            print(" + ", mass[y], end='')
                bell = [round(num, 3) for num in bell]
                print(" = ", bell[i])
                break

# Переделываем list внутри listа в set для расчётов Pl() (в итоге получеим лист сэтов)
result_new = [""] * len(result)
result_new[0]=result[0]
for i in range(1, len(result)):
    buffer = set(result[i])
    buffer.discard(" ")
    result_new[i] = buffer


# Рассчёт Pl()
pl = [0.00] * pow(2, len(arr))  # массив значений функции доверия

for i in range(1,n) :
    pl[i] = 1.00
    if mass[i]!=0.0:
        list1=result_new[i] # Запоминаем гипотезу А с которой будет искать "что угодно, но не А"

        print("Pl(",result_new[i],") = 1",end="")
        for j in range(1,n):
            list2=result_new[j]
            if check_intersection(list1, list2):
                privet=0  #Заглушка
            else:
                print(" -",mass[j],end="")
                pl[i]-=mass[j]
        pl = [round(num, 7) for num in pl]
        print(" = ",pl[i])

#Проверка условия mass[A]<=Bel(A)<=Pl(A)

#Вывод результатов
print("Итоговые результаты (гипотеза, базовая вероятность, доверие, правдоподобие):")

table_data = [
    ["Гипотеза"] + result_new,
    ["Базовая вероятност"] + mass,
    ["Доверие"] + bell,
    ["Правдоподобие"] + pl
]

# Вывод таблицы
print(tabulate(table_data, tablefmt="fancy_grid"))