import pandas as pd

"""Вариант 6"""
EPS = 10 ** (-6)


def f_tasks12(x):
    return (1/13) * abs(-3-x) * ((1/2) * abs(x-1) + 1) * (3 * abs((1/4)*x + 3) + 1)


# первая производная от f_tasks12(x)
def f1_tasks12(x):
    return ((3*abs(x/4 + 3) + 1) * (((x-1)*abs(x+3))/(2*abs(x-1)) + ((abs(x-1)/2 + 1) * (x+3))/abs(x+3)))/13 + \
           (3 * (abs(x-1)/2 + 1) * (x/4 + 3) * abs(x+3))/(52 * abs(x/4 + 3))


def f_task3(x):
    return (pow(x+3, 2) + 2) * (pow(x+2, 2) + 4)


def f1_task3(x):
    return 2*(x+2) * (pow(x+3, 2) + 2) + (x+3)*(pow(x+2, 2) + 4)


def f2_task3(x):
    return pow(x+2, 2) + 2*pow(x+3, 2) + (x+3)*(2*x+4) + (2*x+4)*(2*x+6) + 8


def delta(xk, fi_min):
    return 1/(2*L) * (f_tasks12(xk) - fi_min)


"""Задание 1
    Поиск константы Липшица"""
a12 = -20
b12 = 10

L = max(abs(f1_tasks12(a12)), abs(f1_tasks12(b12)))
print("L = ", L, "\n")


"""Задание 2
    Метод ломанных"""

data2 = {'n': [], 'xn_s': [], 'pn_s': [], '2Ldelta': [], 'xn_1': [], 'xn_2': [], 'pn': []}
mas = [[], []]  # храним включенные пары
iter_counter = 0

n = 1
xn_s = 1 / (2 * L) * (f_tasks12(a12) - f_tasks12(b12) + L * (a12 + b12))
pn_s = 1 / 2 * (f_tasks12(a12) + f_tasks12(b12) + L * (a12 - b12))
delta_n = delta(xn_s, pn_s)
L_deltaN = 2 * L * delta_n

xn_1 = xn_s - delta_n
xn_2 = xn_s + delta_n
pn = 1/2 * (f_tasks12(xn_s) + pn_s)

mas[0].append(pn)
mas[1].append(sorted([xn_1, xn_2]))

while L_deltaN >= EPS:
    if iter_counter % 10 == 0:
        data2['n'].append(n)
        data2['xn_s'].append(xn_s)
        data2['pn_s'].append(pn_s)
        data2['2Ldelta'].append(L_deltaN)
        data2['xn_1'].append(xn_1)
        data2['xn_2'].append(xn_2)
        data2['pn'].append(pn)
    iter_counter += 1

    n += 1
    min_pn_ind = mas[0].index(min(mas[0]))  # индекс pn который надо исключить
    pn_s = mas[0][min_pn_ind]  # значение pn которое надо исключить
    xn_s = mas[1][min_pn_ind][0]  # значение xn которое надо исключить

    mas[1][min_pn_ind].pop(0)
    if mas[1][min_pn_ind] == []:
        mas[0].pop(min_pn_ind)
        mas[1].pop(min_pn_ind)

    delta_n = delta(xn_s, pn_s)
    L_deltaN = 2 * L * delta_n
    xn_1 = xn_s - delta_n
    xn_2 = xn_s + delta_n
    pn = 1 / 2 * (f_tasks12(xn_s) + pn_s)

    mas[0].append(pn)
    mas[1].append(sorted([xn_1, xn_2]))

task2 = pd.DataFrame(data2)
task2.to_excel('task2.xlsx', index=False)

"""Задание 3
    Метод Ньютона-Рафсона"""

data3 = {'n': [], 'xn': [], 'f1(xn)': [], 'f2(xn)': [], 'an': []}
x = -10
n = 0

while abs(f1_task3(x)) > EPS:
    delta = abs(f1_task3(x)) * f2_task3(x)**(-1 / 2)
    if delta > 1/4:
        alpha = 1 / (1 + delta)
    else:
        alpha = 1

    if n % 5 == 0:
        data3['n'].append(n)
        data3['xn'].append(x)
        data3['f1(xn)'].append(f1_task3(x))
        data3['f2(xn)'].append(f2_task3(x))
        data3['an'].append(alpha)

    x -= alpha * f1_task3(x) / f2_task3(x)
    n += 1

task3 = pd.DataFrame(data3)
task3.to_excel('task3.xlsx', index=False)
