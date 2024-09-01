class Symbol:
    def __init__(self, name, memory_start, memory_end=None):
        self.name = name
        self.memory_start = memory_start
        self.memory_end = memory_end or memory_start

class stackPointer(Symbol):
    def __init__(self):
        super().__init__('sp',0)

class Local(Symbol):
    def __init__(self):
        super().__init__('LOCAL',1)

class Argument(Symbol):
    def __init__(self):
        super().__init__('argument', 2)

class This(Symbol):
    def __init__(self):
        super().__init__('this',3)

class That(Symbol):
    def __init__(self):
        super().__init__('that',4)

class Temp(Symbol):
    def __init__(self):
        super().__init__('temp',5,12)

class General(Symbol):
    def __init__(self):
        super().__init__('general',13,15)

class Static(Symbol):
    def __init__(self):
        super().__init__('static', 16, 255)

class Stack(Symbol):
    def __init__(self):
        super().__init__('constant',256,2047)

class pointer0(Symbol):
    def __init__(self):
        super().__init__("pointer0")

class pointer1(Symbol):
    def __init__(self):
        super().__init__("pointer1")