import matplotlib.pyplot as plt

from long_number import LongNumber


def get_vector_x(alpha):
    return [LongNumber("10") ** alpha, LongNumber("1223"), LongNumber("10") ** (alpha - 1),
            LongNumber("10") ** (alpha - 2), LongNumber("3"), LongNumber("-10") ** (alpha - 5)]


def get_vector_y(beta):
    return [LongNumber("10") ** beta, LongNumber("2"), LongNumber("-10") ** (beta + 1), LongNumber("10") ** beta,
            LongNumber("2111"), LongNumber("10") ** (beta + 3)]


def get_eps_long():
    e = LongNumber("0.1")
    while True:
        if LongNumber("42") + LongNumber(e) > LongNumber("42"):
            prev_e = e
            e /= LongNumber("2")
        else:
            return prev_e


def get_eps_double():
    e = float(0.1)
    while True:
        if float(42) + float(e) > float(42):
            prev_e = e
            e /= float(2)
        else:
            return prev_e


def f(a, b, c, x):
    return a * x * x + b * x + c


def test():
    arr_index = []
    arr = []
    x = get_vector_x(-10)
    for beta in range(-10, 20):
        y = get_vector_y(beta)
        res = LongNumber("0")
        for k in range(6):
            res += x[k] * y[k]
        res -= LongNumber("8779")
        arr_index.append(beta)
        arr.append(float(str(res)))
        print(str(beta) + "," + str(res))
    return arr_index, arr


if __name__ == '__main__':

    x, f = test()
    for i in range(len(x)):
        print(str(x[i]), " ", str(f[i]))
    plt.plot(x, f)
    plt.scatter(x, f)

    plt.xlabel("parameter")
    plt.ylabel("Error")
    plt.grid()
    plt.show()
