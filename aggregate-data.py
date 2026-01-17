import pandas as pd


def main():
    df = pd.read_csv("data/raw_github_data.csv")

    df_avg = (
        df
        .groupby(["language", "period"])
        .mean()
        .reset_index()
    )

    df_avg.to_csv("data/language_average.csv", index=False)
    print("Saved: data/language_average.csv")


if __name__ == "__main__":
    main()
