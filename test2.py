class A:
    x = 1

    def f(self):
        pass

    def __init__(self) -> None:
        self.y = 2


print(A.x)
A.x.__setattr__ = None
A.x = 10
print(A.x)
