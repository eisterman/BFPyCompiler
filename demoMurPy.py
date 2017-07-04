from _environment import Environment
from _interfaceobjects import VAR, SET, ADD, SUB


def main():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", 1)
    SET("A", 3)
    SET("C", ADD("A", "B"))
    VAR("D", 2)
    VAR("E", 5)
    SET("D", SUB("C", "B"))
    SET("E", SUB("B", "C"))
    # 3 2 5 3 253

if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    with open('out.bf', 'w') as file:
        file.write(env.BFCode)
