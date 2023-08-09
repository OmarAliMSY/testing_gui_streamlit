import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"csv_data\omarstest.csv")
df = df.drop(columns=["statusNumber","errorCode"])

df.plot()

plt.show()