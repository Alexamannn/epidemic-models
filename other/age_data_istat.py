# -*- coding: utf-8 -*-
"""age_data_istat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-5bh6RCgMdLj60HH07byzkPSt583HJWj
"""

import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/My Drive/Colab Notebooks/covid/DCIS_POPRES1_25052020170201288.csv")

df = data.loc[(data.SEXISTAT1 == 9) &
                (data.STATCIV2 == 99) &
                (data.ITTER107.str.len() >= 5) &
                (data.ETA1 != "TOTAL")][["Territorio", "ETA1", "Value"]]

df.ETA1 = df.ETA1.str.replace("Y","")
df.ETA1 = df.ETA1.str.replace("_GE","")
df.Territorio = df.Territorio.str.replace("Valle d'Aosta / Vallée d'Aoste",
                                                "Valle d'Aosta")
df.Territorio = df.Territorio.str.replace("Bolzano / Bozen", "Bolzano")
df = df.astype({"ETA1": int})

df_final = pd.DataFrame()

# Three groups: 0-25, 25-75, 75+
for provincia in df.Territorio.unique():
  df1 = df.loc[df["Territorio"] == provincia]

  a = df1[df1["ETA1"] <= 25].groupby(["Territorio"]).agg({"Value" : sum})
  b = df1[(df1["ETA1"] > 25) & (df1["ETA1"] <= 75)].groupby(["Territorio"]).agg({"Value" : sum})
  c = df1[df1["ETA1"] > 75].groupby(["Territorio"]).agg({"Value" : sum})

  tmp = pd.concat([a, b, c])
  tmp.reset_index(level=0, inplace=True)
  tmp = tmp.append(pd.DataFrame([{"Territorio" : provincia, "Value" : tmp.Value.sum()}]), ignore_index=True)
  tmp["Eta"] = ["0-25", "25-75", "75-100", "Total"]
  tmp["Percentage"] = tmp.Value.apply(lambda x: x / tmp.Value.values[-1])

  df_final = pd.concat([df_final, tmp])

df_final.to_csv("/content/drive/My Drive/Colab Notebooks/covid/pop_prov_age_3_groups.csv", index=False)

df_final = pd.DataFrame()

# Four groups: 0-25, 25-50, 50-75, 75+
for provincia in df.Territorio.unique():
  df1 = df.loc[df["Territorio"] == provincia]

  a = df1[df1["ETA1"] <= 25].groupby(["Territorio"]).agg({"Value" : sum})
  b = df1[(df1["ETA1"] > 25) & (df1["ETA1"] <= 50)].groupby(["Territorio"]).agg({"Value" : sum})
  c = df1[(df1["ETA1"] > 50) & (df1["ETA1"] <= 75)].groupby(["Territorio"]).agg({"Value" : sum})
  d = df1[df1["ETA1"] > 75].groupby(["Territorio"]).agg({"Value" : sum})

  tmp = pd.concat([a, b, c, d])
  tmp.reset_index(level=0, inplace=True)
  tmp = tmp.append(pd.DataFrame([{"Territorio" : provincia, "Value" : tmp.Value.sum()}]), ignore_index=True)
  tmp["Eta"] = ["0-25", "25-50", "50-75", "75-100", "Total"]
  tmp["Percentage"] = tmp.Value.apply(lambda x: x / tmp.Value.values[-1])

  df_final = pd.concat([df_final, tmp])

df_final.to_csv("/content/drive/My Drive/Colab Notebooks/covid/pop_prov_age_4_groups.csv", index=False)