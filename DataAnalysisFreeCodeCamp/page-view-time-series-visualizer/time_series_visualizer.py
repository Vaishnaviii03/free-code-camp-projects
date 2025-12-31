import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1️⃣ Import data and set index
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# 2️⃣ Clean data (remove top & bottom 2.5%)
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


# ======================
# LINE PLOT
# ======================
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df.index, df["value"], color="red")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


# ======================
# BAR PLOT
# ======================
def draw_bar_plot():
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Correct month order
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    df_bar["month"] = pd.Categorical(
        df_bar["month"],
        categories=months,
        ordered=True
    )

    df_bar = (
        df_bar
        .groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    fig = df_bar.plot(kind="bar", figsize=(15, 7)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig



# ======================
# BOX PLOT
# ======================
def draw_box_plot():
    df_box = df.copy().reset_index()

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month

    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        ax=axes[1]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
