a,b= 100,200
print('hello')
print('{0}+{1}={2}'.format(a,b,a+b))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
a = list(np.arange(1,10,0.1))
b = [math.sin(x) for x in a]
plt.plot(a,b,label = 'sin(x)')
plt.show()