#Reference
#https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Matplotlib/09-LiveData/finished_code.py
 
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
plt.style.use('fivethirtyeight')
 
x_values = []
y_values = []
 
index = count()
 
def animate(i):
    df = pd.read_csv('trendiness_score.csv')
    x_values = df['Time'].values.tolist()
    y_values = df['Score'].values.tolist()
    plt.cla()
    plt.plot(x_values, y_values)
    plt.xlabel('Current Minute')
    plt.ylabel('Score')
    plt.title('Trendiness Score Trend')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
 
ani = FuncAnimation(plt.gcf(), animate, 5000)
 
plt.tight_layout()
plt.show()
