import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # 1️⃣ Read data
    df = pd.read_csv("epa-sea-level.csv")

    # 2️⃣ Scatter plot
    plt.figure(figsize=(10, 5))
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # 3️⃣ Line of best fit (all data)
    res_all = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    years_all = pd.Series(range(1880, 2051))
    plt.plot(
        years_all,
        res_all.intercept + res_all.slope * years_all,
        color="red"
    )

    # 4️⃣ Line of best fit (from year 2000)
    df_recent = df[df["Year"] >= 2000]
    res_recent = linregress(
        df_recent["Year"],
        df_recent["CSIRO Adjusted Sea Level"]
    )
    years_recent = pd.Series(range(2000, 2051))
    plt.plot(
        years_recent,
        res_recent.intercept + res_recent.slope * years_recent,
        color="green"
    )

    # 5️⃣ Labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")

    # 6️⃣ Save and return figure
    plt.savefig("sea_level_plot.png")
    return plt.gca()
