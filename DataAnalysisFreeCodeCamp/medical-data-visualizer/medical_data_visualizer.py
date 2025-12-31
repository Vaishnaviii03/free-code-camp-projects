import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 1️⃣ Import the data
df = pd.read_csv("medical_examination.csv")
df.rename(columns={"gender": "sex"}, inplace=True)



# 2️⃣ Add overweight column
# BMI = weight / (height in meters)^2
df["overweight"] = (
    df["weight"] / ((df["height"] / 100) ** 2) > 25
).astype(int)


# 3️⃣ Normalize cholesterol and glucose
# 1 → 0 (good), >1 → 1 (bad)
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)


# =======================
# CATEGORICAL PLOT
# =======================
def draw_cat_plot():

    # 4️⃣ Convert data to long format
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    # 5️⃣ Group and count
    df_cat = (
        df_cat
        .groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )

    # 6️⃣ Draw categorical plot
    fig = sns.catplot(
        data=df_cat,
        kind="bar",
        x="variable",
        y="total",
        hue="value",
        col="cardio"
    ).fig

    # Do not modify the next two lines
    fig.savefig("catplot.png")
    return fig


# =======================
# HEAT MAP
# =======================
def draw_heat_map():

    # 7️⃣ Clean incorrect data
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # 8️⃣ Correlation matrix
    corr = df_heat.corr()

    # 9️⃣ Mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 🔟 Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # Do not modify the next two lines
    fig.savefig("heatmap.png")
    return fig
