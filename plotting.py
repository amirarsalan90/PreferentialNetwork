import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import collections
import matplotlib.lines as mlines


# data = pd.read_csv("results-nodes.csv")
# df = data.groupby(['p-value']).mean()
# print(df)
# x1 = np.arange(10000,60000,10000)
#
# x = np.arange(10000,50000,0.5)
# def y1(x):
#     return 0.2*x
# def y2(x):
#     return 0.5*x
# def y3(x):
#     return 0.8*x
#
# plt.figure(figsize=(15,12))
# plt.plot(x,y1(x), "b-",linewidth=1)
# plt.plot(x,y2(x), "b-",linewidth=1)
# plt.plot(x,y3(x), "b-",linewidth=1)
#
# plt.plot(x1,df.iloc[0,:-1], "rD", label='p=0.6')
# plt.plot(x1,df.iloc[1,:-1], "rs", label='p=0.75')
# plt.plot(x1,df.iloc[2,:-1], "r^", label='p=0.9')
#
# plt.ylabel("$E[n_{t}]$", fontsize=25)
# plt.xlabel("t", fontsize=25)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
#
# plt.legend(loc=2, prop={'size': 20})
# plt.savefig("plot1.png")
# plt.show()


data = pd.read_csv("results-edges.csv")
df = data.groupby(['p-value']).mean()
print(df)
x1 = np.arange(10000,60000,10000)

x = np.arange(10000,50000,0.5)
def y1(x):
    return 0.12*x
def y2(x):
    return 0.375*x
def y3(x):
    return 0.72*x

plt.figure(figsize=(15,12))
plt.plot(x,y1(x), "b-",linewidth=1)
plt.plot(x,y2(x), "b-",linewidth=1)
plt.plot(x,y3(x), "b-",linewidth=1)

plt.plot(x1,df.iloc[0,:-1], "rD", label='p=0.6')
plt.plot(x1,df.iloc[1,:-1], "rs", label='p=0.75')
plt.plot(x1,df.iloc[2,:-1], "r^", label='p=0.9')

plt.ylabel("$E[m_{t}]$", fontsize=25)
plt.xlabel("t", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.legend(loc=2, prop={'size': 20})
plt.savefig("plot2.png")

plt.show()






# #plotting the neighbors (Figure 4)
# with open("neighbors.csv", "r") as file:
#     reader = csv.reader(file)
#     data = list(reader)
#
# data_2 = data[1:]
# data_3 = [item[:-1] for item in data_2]
#
# final_list = []
# for sublist in data_3:
#     for item in sublist:
#         final_list.append(item)
#
# print(final_list)
# final_list = [int(t) for t in final_list]
# final_list = [t for t in final_list if t < 50]
# print(final_list)
# dataCount = collections.Counter(final_list)
# dataCount2 = sorted(dataCount.items())
# print(dataCount2)
# deg, cnt = zip(*dataCount2)
# cnt_norm = [t/sum(cnt) for t in cnt]
#
# plt.figure(figsize=(15,12))
# plt.plot(deg,cnt_norm,"rs")
# plt.ylabel("$E[x_{k,t}^{(1)}]$", fontsize=25)
# plt.xlabel("k", fontsize=25)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.savefig("plot3.png")
# plt.show()

