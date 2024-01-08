import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import seaborn as sns
from matplotlib import cm as cm

csv_path = glob(r"C:\Users\o.abdulmalik\Documents\testing_gui\csv_data\server\csv_data\Lebensdauertest_231219.csv")
df = pd.read_csv(csv_path[0], parse_dates=["times"], index_col=["times"])
def get_lower_tri_heatmap(df, output="cooc_matrix.png"):
    mask = np.zeros_like(df)
    mask[np.triu_indices_from(mask)] = True

    # Want diagonal elements as well

    # Set up the matplotlib figure
    f, ax = plt.subplots()

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns_plot = sns.heatmap(df, mask=mask, cmap=cmap,
             annot=True,fmt=".2f")
    # save to file
    fig = sns_plot.get_figure()


hm = df.corr(min_periods=3).dropna(how="all",axis=1)
hm = hm.dropna(how="all", axis=0)
corr_mat = np.array(hm)
get_lower_tri_heatmap(hm)

#df["torque_percentage"] = (((df["torque_percentage"]) * 400 ) -200) *7
#
#df["torque_t1"] = np.abs(df["torque_t1"].rolling(3).mean() * 110)
#df["torque_percentage"] = np.abs(df["torque_percentage"].rolling(3).mean())
#
#ax = df.plot( y=["torque_t1","torque_percentage"], xlabel="time", ylabel="Torque [Nm]", figsize=(13, 5))
#df.plot( y=["northSensorAngle_t1"], ylabel="Angle [°]", secondary_y=True, ax=ax)




plt.show()
