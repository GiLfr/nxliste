import pandas as pd

# df1 = pd.DataFrame({'A': ['AA', 'BB','DD'], 'B': [1, 2, 999], 'C': ['XXX', 'YYY', 'ZZZ']}); 
# df2 = pd.DataFrame({'A': ['BB', 'AA', 'CC'], 'B': [9, 2, 0]}); 

df1 = pd.DataFrame({'City': ['New York', 'Chicago', 'Tokyo', 'Paris','New Delhi'],
                     'Temp': [59, 29, 73, 56,48],
                     'Meteo': ['Beau','Beau','Pluvieux','Beau','Nuageux']})

df2 = pd.DataFrame({'City': ['London', 'New York', 'Tokyo', 'New Delhi','Paris'],
                     'Temp': [55, 55, 73, 85,56]})
print(df1)
print(df2)

# print(pandas.merge(dfi, dfn,how = 'right'))

print(df1.merge(df2, how = 'inner' ,indicator=False))

# df = pd.concat([df1, df2])
# df = df.reset_index(drop=True)
# df_gpby = df.groupby(list(df.columns))
# idx = [x[0] for x in df_gpby.groups.values() if len(x) != 1]
# print(df.reindex(idx))

print(df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only'])
