from random import randint


def q_gen_simple_add(q_count, ans_field):
    for r in range(q_count):
        yield "{} + {} = {} ;".format(randint(1, 9), randint(1, 9), ans_field)


def q_gen_simple_sub_positive(q_count, ans_field):
    for r in range(q_count):
        num1 = randint(1, 9)
        num2 = randint(1, num1)
        yield "{} - {} = {} ;".format(num1, num2, ans_field)


def write_exercise(file_name, q_generator, q_count, q_per_line=5, q_padding="    ", ans_field="____"):
    nl_remainder = q_per_line - 1

    with open(file_name, "w") as f:
        for i, q in enumerate(q_generator(q_count, ans_field)):
            f.write(q)
            if i % q_per_line == nl_remainder:
                f.write("\n\n")
            else:
                f.write(q_padding)


if __name__ == '__main__':
    generators = {
        "simple_add": q_gen_simple_add,
        "simple_sub": q_gen_simple_sub_positive
    }

    write_exercise("simple_add.txt", generators["simple_add"], 100)
    write_exercise("simple_sub.txt", generators["simple_sub"], 100)
