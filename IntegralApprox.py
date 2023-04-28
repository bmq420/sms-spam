# complete the following functions
def getPartition(a, b, n):
    h = (b - a) / n
    x = [a + i*h for i in range(n+1)]
    return h, x

def getValues(x, f):
    y = [f(i) for i in x]
    return y

def integralApprox(y, h):
    I = 0
    for i in range(len(y)-1):
        I += (y[i] + y[i+1]) * h / 2
    return I

if __name__ == "__main__":
    f = lambda x: 3*x*x + 4*x - 5
    F = lambda x: x*x*x + 2*x*x - 5*x
    a, b = 1, 3
    n = 10
    h, x = getPartition(a, b, n)
    print("h = ", h, "x = ", x)
    y = getValues(x, f)
    print("y = ", y)
    I = integralApprox(y, h)
    print("I = ", I)
    print("Gold I = ", (F(3) - F(1)))