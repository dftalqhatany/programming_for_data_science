import matplotlib.pyplot as plt


def missing_chart(df):

    missing = df.isna().sum()

    fig, ax = plt.subplots()

    missing.plot(kind="bar", ax=ax)

    ax.set_title("Missing Values per Column")

    return fig


def outlier_chart(outliers):

    fig, ax = plt.subplots()

    cols = list(outliers.keys())
    values = list(outliers.values())

    ax.bar(cols, values)

    ax.set_title("Outliers per Column")

    return fig
