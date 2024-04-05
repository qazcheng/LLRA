import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
list_3=[]
list_4=[]
repeat=[]
# 读取CSV文件为DataFrame
df = pd.read_csv('output_numbers.csv')
print(df.shape[1])
print(df.shape[0])
list_2=df["Extracted Numbers"]
list_2=list(list_2)
list_1=df["Time (seconds)"]
list_1=list(list_1)
new_list_1=[]
print(len(list_2))
for i in range(len(list_2)):
    y=list_2[i].split(",")
    suffer=0.0
    for j in y:
            j = j.replace(' ', '')
            try:
                number = float(j)
                if 1.0 < number < 3.0 and suffer == 0.0:
                    if str(number).startswith("1.1"):
                        number = float(str(number).replace("1.1", "1.7"))
                    suffer = number
                    continue
                if 1.0 < number < 3.0 and suffer != 0.0:
                    if str(number).startswith("1.1"):
                        number = float(str(number).replace("1.1", "1.7"))
                    list_3.append(suffer)
                    list_4.append(number)
                    new_list_1.append(list_1[i])
                    break

            except ValueError:
                continue
print(len(new_list_1))
for i in range(len(new_list_1)):
    new_list_1[i]=round(new_list_1[i]/1000,5)
print(len(list_3))
print(len(list_4))
df_grade = pd.DataFrame(new_list_1, columns=['time'])
df_grade = pd.concat([df_grade, pd.DataFrame(list_3,columns=['103'])],axis=1)
df_grade = pd.concat([df_grade, pd.DataFrame(list_4,columns=['100'])],axis=1)
print(df_grade)
import pandas as pd
# 创建一个ExcelWriter对象，指定文件名
with pd.ExcelWriter('data.xlsx', engine='openpyxl', mode='a') as writer:
    # 将DataFrame写入新的工作表
    df_grade.to_excel(writer, sheet_name='IOT', index=False)

# df_grade.to_excel('data.xlsx',sheet_name='LRAKEP34')
