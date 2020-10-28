from copy import copy, deepcopy


class LongNumber:
    def __init__(self, number, exp=None):
        """Конструктор"""
        self.plus = True
        self.exponent = 1

        if number[0] == '-':
            number = number[1:]
            self.plus = False

        self.digits = [*number]

        if exp is None:
            self.exponent = len(number)
            pos_point = number.find('.')
            if pos_point != -1:
                self.exponent = pos_point
                self.digits = [*number[0:pos_point]] + [*number[pos_point + 1:]]

        else:
            self.exponent = len(number)
            pos_point = number.find('.')
            if pos_point != -1:
                self.exponent = pos_point
                self.digits = [*number[0:pos_point]] + [*number[pos_point + 1:]]
            self.exponent = exp

        self.digits = list(map(int, self.digits))

    def __remote_zeros(self):
        """Удаление нулей справа и слева"""
        n = max(1, self.exponent)

        while len(self.digits) > n and self.digits[-1] == 0:
            self.digits.pop(-1)

        while len(self.digits) > 1 and self.digits[0] == 0:
            self.digits.pop(0)
            self.exponent -= 1

        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop(-1)

        if len(self.digits) == 1 and self.digits[0] == 0:
            self.exponent = 1
            self.plus = True

    def __str__(self):
        """Перегрузка печати"""
        print_str = ''
        len_digit = len(self.digits)

        if not self.plus:
            print_str += '-'

        if self.exponent > 0:
            count = 0

            while count < len_digit and count < self.exponent:
                print_str += str(self.digits[count])
                count += 1

            while count < self.exponent:
                print_str += '0'
                count += 1

            if count < len_digit:
                print_str += '.'
                while count < len_digit:
                    print_str += str(self.digits[count])
                    count += 1

        else:
            print_str += '0.'
            for i in range(-self.exponent):
                print_str += '0'
            for i in range(len_digit):
                print_str += str(self.digits[i])

        return print_str

    def __mul__(self, other):
        """Перегрузка умножения"""
        len_res = len(self.digits) + len(other.digits)

        res = LongNumber('0')
        res.plus = self.plus * other.plus
        res.digits = [0 for _ in range(len_res)]
        res.exponent = self.exponent + other.exponent

        # умножаем числа в столбик
        for i in range(len(self.digits)):
            for j in range(len(other.digits)):
                res.digits[i + j + 1] += self.digits[i] * other.digits[j]

        # переносы
        for i in range(len_res - 1, 0, -1):
            res.digits[i - 1] += res.digits[i] // 10
            res.digits[i] %= 10

        res.__remote_zeros()

        return res

    def __neg__(self):
        """Перегрузка унарного минуса"""
        res = LongNumber('0')
        res.plus = not self.plus
        res.exponent = self.exponent
        res.digits = self.digits
        return res

    def __gt__(self, other):
        """Перегрузка >"""

        if self.plus != other.plus:
            return self.plus > other.plus

        if self.exponent != other.exponent:
            return (self.exponent > other.exponent) ^ (self.plus is False)

        dig_1 = copy(self.digits)
        dig_2 = copy(other.digits)
        size = max(len(dig_1), len(dig_2))

        while len(dig_1) != size:
            dig_1.append(0)

        while len(dig_2) != size:
            dig_2.append(0)

        for i in range(size):
            if dig_1[i] != dig_2[i]:
                return (dig_1[i] > dig_2[i]) ^ (self.plus is False)

        return False

    def __eq__(self, other):
        """Перегрузка =="""
        if self.plus != other.plus: return False

        if self.exponent != other.exponent: return False

        if len(self.digits) != len(other.digits): return False

        for i in range(len(self.digits)):
            if self.digits[i] != other.digits[i]: return False

        return True

    def __ge__(self, other):
        """Перегрузка >="""
        return self > other or self == other

    def __add__(self, other):
        """Перегрузка сложения"""

        if self.plus == other.plus:
            exp_1 = self.exponent
            exp_2 = other.exponent
            exp = max(exp_1, exp_2)
            dig_1 = copy(self.digits)
            dig_2 = copy(other.digits)

            while exp_1 != exp:
                dig_1.insert(0, 0)
                exp_1 += 1

            while exp_2 != exp:
                dig_2.insert(0, 0)
                exp_2 += 1

            size = max(len(dig_1), len(dig_2))

            while len(dig_1) != size:
                dig_1.append(0)

            while len(dig_2) != size:
                dig_2.append(0)

            len_res = 1 + size

            res = LongNumber('0')
            res.plus = self.plus
            res.digits = [0 for _ in range(len_res)]

            for i in range(size):
                res.digits[i + 1] = dig_1[i] + dig_2[i]

            for i in range(len_res - 1, 0, -1):
                res.digits[i - 1] += res.digits[i] // 10
                res.digits[i] %= 10

            res.exponent = exp + 1
            res.__remote_zeros()
            return res

        if not self.plus:
            return other - (-self)

        return self - (-other)

    def __sub__(self, other):
        """Перегрузка вычитания"""

        if self.plus and other.plus:
            cmp = self > other
            exp_1 = self.exponent if cmp else other.exponent
            exp_2 = other.exponent if cmp else self.exponent
            exp = max(exp_1, exp_2)
            dig_1 = copy(self.digits if cmp else other.digits)
            dig_2 = copy(other.digits if cmp else self.digits)

            while exp_1 != exp:
                dig_1.insert(0, 0)
                exp_1 += 1

            while exp_2 != exp:
                dig_2.insert(0, 0)
                exp_2 += 1

            size = max(len(dig_1), len(dig_2))

            while len(dig_1) != size:
                dig_1.append(0)

            while len(dig_2) != size:
                dig_2.append(0)

            len_res = 1 + size

            res = LongNumber('0')
            res.plus = True if cmp else False
            res.digits = [0 for _ in range(len_res)]

            for i in range(size):
                res.digits[i + 1] = dig_1[i] - dig_2[i]

            for i in range(len_res - 1, 0, -1):
                if res.digits[i] < 0:
                    res.digits[i] += 10
                    res.digits[i - 1] -= 1

            res.exponent = exp + 1
            res.__remote_zeros()
            return res

        if (self.plus is False) and (other.plus is False):
            return (-other) - (-self)

        return self + (-other)

    def inverse(self):
        """Инверсия числа (1/x)"""
        div_digits = 1000

        if len(self.digits) and self.digits[0] == 0:
            raise ZeroDivisionError("Division by zero!")

        other = deepcopy(self)
        other.plus = True

        delit = LongNumber('1')

        res = LongNumber('0')
        res.plus = self.plus
        res.exponent = 1
        res.digits = []

        while LongNumber('1') > other:
            other.exponent += 1
            res.exponent += 1

        while other > delit:
            delit.exponent += 1

        res.exponent -= delit.exponent - 1

        numbers = 0
        total_numbers = div_digits + max(0, res.exponent)

        while True:
            div = 0

            while delit >= other:
                div += 1
                delit = delit - other

            delit.exponent += 1
            delit.__remote_zeros()
            res.digits.append(div)
            numbers += 1

            if delit == LongNumber('0') or numbers >= total_numbers:
                break

        return res

    def __truediv__(self, other):
        """Пергрузка деления"""
        res = self * other.inverse()

        i = len(res.digits) - 1 - max(0, self.exponent)
        n = max(0, res.exponent)

        if (i > n) and (res.digits[i] == 9):
            while (i > n) and (res.digits[i] == 9):
                i -= 1

            if res.digits[i] == 9:
                res.digits = res.digits[:n]
                if self.plus:
                    res += LongNumber('1')
                else:
                    res += LongNumber('-1')

            else:
                res.digits = res.digits[:(i + 1)]
                res.digits[i] += 1
        return res

    def __pow__(self, power, modulo=None):
        res = LongNumber("1")
        for i in range(abs(power)):
            res *= self
        if power >= 0:
            return res
        else:
            return LongNumber("1")/res
        return res
