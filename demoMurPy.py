from MurPy import Environment
from _interfaceobjects import VAR, SET, ADD


def main():
    VAR("ciao", 5)
    VAR("ciao2", 2)
    VAR("ciao3", 1)
    SET("ciao", 3)
    SET("ciao3", ADD("ciao", "ciao2"))
    VAR("ciao4", 2)
    # 3 2 5 2

if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
    print(env.BFCode)
