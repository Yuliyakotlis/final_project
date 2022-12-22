import random


def rand_letter(x, y):
    return chr(random.randint(ord(x), ord(y)))


def generate_letters_ru(size: int):
    return ''.join(random.choice(rand_letter('а', 'я')) for i in range(size))


def generate_numbers(size: int):
    return ''.join(random.choice(rand_letter('0', '9')) for i in range(size))


def generate_letters_en(size: int):
    return ''.join(random.choice(rand_letter('a', 'z')) for i in range(size))

