import numpy as np

class Variable:
    def __init__(self, data):
        if data is not None:
            if not isinstance(data, np.ndarray):
                raise TypeError('{} is not supported'.format(type(data))) 

        self.data = data
        self.grad = None
        self.creator = None

    def set_creator(self, func):
        self.creator = func
    
    def backward(self):
        if self.grad is None:
            self.grad = np.ones_like(self.data)

        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            x, y = f.input, f.output
            x.grad = f.backward(y.grad)

            if x.creator is not None:
                funcs.append(x.creator)

def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x

# base Class
class Function:
    def __call__(self, input):
        x = input.data
        y = self.forward(x)
        output = Variable(as_array(y))
        output.set_creator(self)
        self.input = input
        self.output = output
        return output
    
    def forward(self, in_data):
        raise NotImplementedError()
    
    def backward(self, grad):
        raise NotImplementedError()

class Square(Function):
    def forward(self, input):
        return input ** 2
    
    def backward(self, gy):
        x = self.input.data
        return 2 * x * gy
    
def square(input):
    f = Square()
    return f(input)


class Exp(Function):
    def forward(self, input):
        return np.exp(input)
    
    def backward(self, gy):
        x = self.input.data
        return np.exp(x) * gy

def exp(input):
    f = Exp()
    return f(input)

# 中心差分近似
def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)
