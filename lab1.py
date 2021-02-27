# Вхідні данні
hours = 1102     # для знаходження ймовірності безвідмовної роботи
lamd_hours = 5420  # для знаходження інтенсивності відмов
y = 0.86

# Вхідна вибірка наробітків до відмови(у годинах)
t_i = [912, 2981, 2048, 1268, 1879, 381, 1855,
        460, 4, 376, 364, 1961, 707, 673, 193, 1617,
        679, 319, 1155, 29, 2208, 107, 663, 769,
        187, 222, 38, 628, 2310, 375, 414, 2598,
        509, 275, 468, 918, 60, 646, 618, 560, 1484,
        446, 1755, 1140, 192, 1101, 103, 2853,
        5771, 104, 1163, 55, 72, 491, 253, 898,
        1280, 85, 318, 121, 692, 948, 515, 622,
        1420, 252, 1487, 1885, 765, 966, 241, 79,
        722, 378, 444, 661, 1532, 2505, 455, 394,
        960, 1288, 1074, 109, 88, 430, 1672, 2224,
        427, 277, 1175, 863, 672, 1426, 199, 603,
        1337, 258, 818, 138]


# Сортована вибірка
sorted_t_i = sorted(t_i)

# Кількість об'єктів вибірки

N = len(sorted_t_i)

# Середній наробіток T_cp

T_cp = sum(t_i)/N
print("Середній наробіток: T_cp = " + str(T_cp))

# Розмах вибірки h

max_t_i = max(t_i)

h = max_t_i / 10

count =[[] for i in range(10)]
interval = [round(i*h, 1) for i in range(11)]

# Поділ на інтервали
try:
    for i in range(len(interval)):
        for j in sorted_t_i:
            if interval[i] <= j <= interval[i+1]:
                count[i].append(j)
except IndexError:
     pass

# Кількість значень вибірки, що потрапили в даний інтервал N_i
N_i = [len(i) for i in count]

# Густина відносних частот f_i
try:
    f_i = [round( (j / (N * h) ), 6) for j in N_i ]
except ZeroDivisionError:
    print("Division by zero.")

def recsum(num_list):
    if len(num_list) == 0:
        return 0
    return num_list[0] + recsum(num_list[1:])

# Значення ймовірності безвідмовної роботи пристрою на час правої границі
# для кожного інтервалу P_t
S_i = [recsum(f_i[:(i+1)])*h for i in range(len(f_i))]
P_t0 = 1
P_t = [round((1 - i), 6) for i in S_i]
P_t.insert(0, P_t0)

# γ-відсотковий наробіток на відмову T_y
def d_for_interval(P_t_i_1, P_t_i):
    try:
        d = round((P_t_i_1 - y)/(P_t_i_1 - P_t_i), 2)
        return d
    except ZeroDivisionError:
        print("Division by zero.")
print(P_t)
# Для нульового інтервалу 
d = d_for_interval(P_t[0], P_t[1])

T_y = round(h * d, 2)
print("γ-відсотковий наробіток на відмову: T_y = " + str(T_y) + " при γ = " + str(y))
# Ймовірність безвідмовної роботи на заданий час годин p_t
def find_interval(hours, interval_list):
    all = []
    try:
        for i in range(len(interval)):
            if hours <= interval[i]:
                all.append(i)
        return (all[0] - 1)

    except IndexError:
        pass


def find_p_t(hours):
    f_inter = find_interval(hours, interval)
    s_t = recsum(f_i[:f_inter])*h + (hours - interval[f_inter]) * f_i[f_inter]
    p_t = 1 - s_t
    return round(p_t, 6)
print("Ймовірність безвідмовної роботи на заданий час " + str(hours) + "годин: P(" + str(hours) + ") = " + str(find_p_t(hours)))

# Інтенсивність відмов на заданий час годин lamb
def find_lamd(lamb_hours):
    f_inter = find_interval(lamb_hours, interval)
    fi = f_i[f_inter]
    p_t = find_p_t(lamb_hours)
    try:
        lamb = fi / p_t
    except ZeroDivisionError:
        print("Division by zero.")
    return round(lamb,6)
print("Інтенсивність відмов на заданий час " + str(lamd_hours) + "годин: lamb(" + str(lamd_hours) + ") = " + str(find_lamd(lamd_hours)))
