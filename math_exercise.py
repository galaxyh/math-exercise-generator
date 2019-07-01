from random import randint, randrange
from math import log10, floor


def get_align_padding(num_max):
    return floor(log10(num_max)) + 1


def q_gen_simple_add(q_count, ans_field, num_min, num_max):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        yield "{num1: >{width}} + {num2: >{width}} = {ans_field} ;".format(
            num1=randint(num_min, num_max),
            num2=randint(num_min, num_max),
            ans_field=ans_field,
            width=padding_width
        )


def q_gen_simple_sub_positive(q_count, ans_field, num_min, num_max):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        num1 = randint(num_min, num_max)
        num2 = randint(num_min, num1)
        yield "{num1: >{width}} - {num2: >{width}} = {ans_field} ;".format(
            num1=num1,
            num2=num2,
            ans_field=ans_field,
            width=padding_width
        )


def q_gen_3_add_sub_positive(q_count, ans_field, num_min, num_max):
    padding_width = get_align_padding(num_max)
    for r in range(q_count):
        ops = [[-1, 1][randrange(2)], [-1, 1][randrange(2)]]
        while True:
            num1 = randint(num_min, num_max)
            if ops[0] == 1:
                num2 = randint(num_min, num_max)
            elif num1 >= num_min:
                num2 = randint(num_min, num1)
            else:
                continue

            tmp = num1 + ops[0] * num2

            if ops[1] == 1:
                num3 = randint(num_min, num_max)
            elif tmp >= num_min:
                num3 = randint(num_min, tmp)
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


def write_exercise(file_name, q_generator, q_count, num_min, num_max, line_height=1, q_per_line=5, q_padding=4,
                   ans_field=4):
    q_padding_str = "{x: >{width}}".format(x="", width=q_padding)
    ans_field_str = "{x:_>{width}}".format(x="", width=ans_field)

    nl_remainder = q_per_line - 1

    with open(file_name, "w") as f:
        for i, q in enumerate(q_generator(q_count, ans_field_str, num_min, num_max)):
            f.write(q)
            if i % q_per_line == nl_remainder:
                for j in range(0, line_height + 1):
                    f.write("\n")
            else:
                f.write(q_padding_str)


if __name__ == '__main__':
    generators = {
        "simple_add": q_gen_simple_add,
        "simple_sub_positive": q_gen_simple_sub_positive,
        "triple_add_sub_positive": q_gen_3_add_sub_positive
    }

    write_exercise("simple_add.txt", generators["simple_add"], 100, 1, 10)
    write_exercise("simple_sub.txt", generators["simple_sub_positive"], 100, 1, 20)
    write_exercise("triple_add_sub_positive.txt", generators["triple_add_sub_positive"], 2000, 1, 33,
                   line_height=7,
                   q_per_line=2,
                   q_padding=8,
                   ans_field=7)
