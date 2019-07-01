from random import randint, randrange
from math import log10, floor, inf


def get_align_padding(num_max):
    return floor(log10(num_max)) + 1


def q_gen_2_add(q_count, ans_field, num_min, num_max, ans_lb=-inf, ans_ub=inf):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        num1 = randint(num_min, num_max)
        num2 = randint(num_min, min(num_max, ans_ub - num1))

        yield "{num1: >{width}} + {num2: >{width}} = {ans_field} ;".format(
            num1=num1,
            num2=num2,
            ans_field=ans_field,
            width=padding_width
        )


def q_gen_2_sub(q_count, ans_field, num_min, num_max, ans_lb=-inf, ans_ub=inf):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        while True:
            num1 = randint(num_min, num_max)
            num2 = randint(num_min, num_max)
            ans = num1 - num2
            if ans < ans_lb:
                continue

            yield "{num1: >{width}} - {num2: >{width}} = {ans_field} ;".format(
                num1=num1,
                num2=num2,
                ans_field=ans_field,
                width=padding_width
            )
            break


def q_gen_3_add_sub_strict_positive(q_count, ans_field, num_min, num_max, ans_lb=-inf, ans_ub=inf):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        ops = [[-1, 1][randrange(2)], [-1, 1][randrange(2)]]
        while True:
            num1 = randint(num_min, num_max)
            if ops[0] == 1:
                if ans_ub - num1 == 0:
                    continue
                num2 = randint(num_min, min(num_max, ans_ub - num1))
            elif num1 >= num_min:
                num2 = randint(num_min, num1)
            else:
                continue

            ans = num1 + ops[0] * num2

            if ops[1] == 1:
                if ans_ub - ans == 0:
                    continue
                num3 = randint(num_min, min(num_max, ans_ub - ans))
            elif ans >= num_min:
                num3 = randint(num_min, ans)
            else:
                continue

            yield "{num1: >{width}} {op1} {num2: >{width}} {op2} {num3: >{width}} = {ans_field} ;".format(
                num1=num1,
                op1=("+" if ops[0] > 0 else "-"),
                num2=num2,
                op2=("+" if ops[1] > 0 else "-"),
                num3=num3,
                ans_field=ans_field,
                width=padding_width
            )
            break


def write_exercise(file_name, q_generator, q_count, num_min, num_max, ans_lb=-inf, ans_ub=inf,
                   line_height=1, q_per_line=5, q_padding=4, ans_field=4):
    q_padding_str = "{x: >{width}}".format(x="", width=q_padding)
    ans_field_str = "{x:_>{width}}".format(x="", width=ans_field)

    nl_remainder = q_per_line - 1

    with open(file_name, "w") as f:
        for i, q in enumerate(q_generator(q_count, ans_field_str, num_min, num_max, ans_lb=ans_lb, ans_ub=ans_ub)):
            f.write(q)
            if i % q_per_line == nl_remainder:
                for j in range(0, line_height + 1):
                    f.write("\n")
            else:
                f.write(q_padding_str)


if __name__ == '__main__':
    generators = {
        "2_add": q_gen_2_add,
        "2_sub": q_gen_2_sub,
        "3_add_sub_strict_positive": q_gen_3_add_sub_strict_positive
    }

    write_exercise("2_add.txt", generators["2_add"], 100, 1, 10)
    write_exercise("2_sub_positive.txt", generators["2_sub"], 100, 1, 20, ans_lb=0)
    write_exercise("3_add_sub_positive.txt", generators["3_add_sub_strict_positive"], 2000, 1, 99,
                   ans_ub=99,
                   line_height=7,
                   q_per_line=2,
                   q_padding=8,
                   ans_field=7)
