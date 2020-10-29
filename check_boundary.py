# а)

# Деление на 0 всегда приводит к ошибке в соответствии со стандартом IEEE-754
try:
    print(float('inf')//0)
except ZeroDivisionError:
    print("Dicision by zero error")

# Деление 0 всегда дает 0 в соответствии с IEEE-754
print(0//float('inf'))

# Неопределенность
print(float('inf')//float('inf'))

# б)

# В соответствии с IEEE-754 "-" - это дополнительный бит, поэтому 0.0 и -0.0 отличаются.
# Чтобы это обойти в Python используется сигнатура ==
print(0.0 is -0.0)
print(0.0 == -0.0)

# В соответствии со стандартом IEEE-754 любое число, включая +inf , выше, чем -inf
print(float('inf') == float('-inf'))