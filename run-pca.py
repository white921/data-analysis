import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


FEATURES = ["stars", "forks", "issues", "commits"]


def run_pca_and_plot(df, period_label, title):
    """
    df: periodで絞り込んだDataFrame
    period_label: 'past' or 'recent'
    title: 図のタイトル
    """

    X = df[FEATURES]

    # 標準化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame(
        X_pca,
        columns=["PC1", "PC2"]
    )
    pca_df["language"] = df["language"]

    # 主成分負荷量（コンソール出力用）
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=["PC1", "PC2"],
        index=FEATURES
    )

    print(f"\n=== PCA Loadings ({period_label}) ===")
    print(loadings)

    print(f"\n=== Explained Variance Ratio ({period_label}) ===")
    print(pca.explained_variance_ratio_)

    # 可視化
    plt.figure(figsize=(8, 6))
    for _, row in pca_df.iterrows():
        plt.scatter(row["PC1"], row["PC2"])
        plt.text(row["PC1"], row["PC2"], row["language"])

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    df = pd.read_csv("data/language_average.csv")

    # --- past ---
    df_past = df[df["period"] == "past"].reset_index(drop=True)
    run_pca_and_plot(
        df_past,
        period_label="past",
        title="PCA of GitHub Language Features (Past: 3 Years Ago)"
    )

    # --- recent ---
    df_recent = df[df["period"] == "recent"].reset_index(drop=True)
    run_pca_and_plot(
        df_recent,
        period_label="recent",
        title="PCA of GitHub Language Features (Recent)"
    )


if __name__ == "__main__":
    main()
