import pandas as pd
import matplotlib.pyplot as plt
import argparse


def load_data(file_path):
    return pd.read_csv(file_path)


def plot_bubble_chart(df):
    x = df['GDP_per_capita']  #columns give in the image
    y = df['military_expenditures']
    color_attr = df['life_expectancy']
    size = ((df['population'] - df['population'].min()) / (df['population'].max() - df['population'].min())) * 1000 #normalizing
    plt.figure(figsize=(12, 8))
    plt.scatter(x, y, s=size, c=color_attr, cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5),\
    plt.colorbar(label='Life Expectancy'),\
    plt.title('GDP per Capita, Military Expenditures, Population, and Life Expectancy'),\
    plt.xlabel('GDP per Capita (in USD)'), plt.ylabel('Military Expenditures (in USD)')

    sizes = [1e5, 1e7, 1e9]  # Example sizes to display in the legend
    handles = [
        plt.scatter(
            [], [],
            s=((sz - df['population'].min()) / (df['population'].max() - df['population'].min())) * 1000,
            alpha=0.5,
            edgecolor='black',
            linewidth=0.5,
            label=f'{int(sz):,}'
        ) for sz in sizes
    ]
#legend
    plt.legend(
        handles=handles, title='Population',
        loc='upper right', bbox_to_anchor=(1, 1), frameon=True  # Adjusted higher with bbox_to_anchor
    )
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Bubble Chart for Global Statistics (GDP per capita, Military Expenditures, Life Expectancy, Population)")
    parser.add_argument('-i', '--input', type=str, required=True, help="Path to the CSV file containing data")
    args = parser.parse_args()
    df = load_data(args.input)
    plot_bubble_chart(df)


if __name__ == '__main__':
    main()
