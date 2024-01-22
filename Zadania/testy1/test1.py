def low_num(numbers):
    numbers = [int(num) for num in numbers.split()]  # Konwersja ciągu znaków na listę liczb całkowitych
    return min(numbers), max(numbers)

result = low_num("8 3 -5 42 -1 0 0 -9 4 7 4 -4")
print(result)

