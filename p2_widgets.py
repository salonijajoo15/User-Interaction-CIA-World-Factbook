import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget
import argparse

# not hardcoding cli this time(made that mistake last time my bad)
def parse_args():
    parser = argparse.ArgumentParser(description="Interactive Bubble Chart using CIA Factbook Data")
    parser.add_argument('-i', '--input', type=str, default='/Users/salonijajoo/Downloads/CIA_world_factbook_2023.csv',
                        help='Path to the CSV file containing data')
    return parser.parse_args()
#global variable to manage the colorbar across updates
colorbar = None

# main
def main():
    global colorbar
    args = parse_args()
    df = pd.read_csv(args.input)
    numeric_columns = df.select_dtypes(include=[float, int]).columns.tolist() #separating numeric columns
    app = QApplication(sys.argv)
    #display
    window = QMainWindow()
    window.setWindowTitle('Interactive Bubble Chart')
    window.setGeometry(100, 100, 900, 700)
    figure, ax = plt.subplots(figsize=(8, 6))  # Set a fixed figure size
    canvas = FigureCanvas(figure)
    widget = QWidget()
    layout = QVBoxLayout()
    x_select = QComboBox()
    x_select.addItems(numeric_columns)
    y_select = QComboBox()
    y_select.addItems(numeric_columns)
    color_select = QComboBox()
    color_select.addItems(df.columns)
    size_select = QComboBox()
    size_select.addItems(numeric_columns)

    # adding the widgets for task 2
    layout.addWidget(QLabel('X-axis:'))
    layout.addWidget(x_select)
    layout.addWidget(QLabel('Y-axis:'))
    layout.addWidget(y_select)
    layout.addWidget(QLabel('Color:'))
    layout.addWidget(color_select)
    layout.addWidget(QLabel('Size:'))
    layout.addWidget(size_select)
    layout.addWidget(canvas)
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    # if column can be converted to numeric this function does it
    def is_numeric(column):
        return column in numeric_columns

    #legend
    def legend(ax, size_attr):
        sizes = pd.to_numeric(df[size_attr], errors='coerce')
        if sizes.isnull().all():
            return
        small = sizes.min()
        big = sizes.max()
        medium = (small + big) / 2
        fixed_sizes = [100, 400, 800]
        size_labels = [f'{int(small):,}', f'{int(medium):,}', f'{int(big):,}']
        legend_x = 0.85
        legend_y_start = 0.8
        space = 0.1

        for i, (fixed_size, label) in enumerate(zip(fixed_sizes, size_labels)): #Loop to plot the invisible legend bubbles and their corresponding labels
            ax.scatter(legend_x, legend_y_start - i * space, s=fixed_size, color='none', edgecolor='black',
                       transform=ax.transAxes, clip_on=False)
            ax.text(legend_x + 0.05, legend_y_start - i * space, f'{label}', transform=ax.transAxes,
                    verticalalignment='center', fontsize=10)

        ax.text(legend_x, legend_y_start + 0.05, size_attr, transform=ax.transAxes, fontweight='bold', fontsize=10)


    def update_plot():
        global colorbar  #global to allow modifications to the colorbar
        ax.clear()
        x_attr = x_select.currentText()
        y_attr = y_select.currentText()
        color_attr = color_select.currentText()
        size_attr = size_select.currentText()
        if not is_numeric(size_attr):
            raise ValueError(f"The selected size attribute '{size_attr}' contains non-numeric data.")

        # plots data
        x = df[x_attr]
        y = df[y_attr]
        color = df[color_attr]
        size = pd.to_numeric(df[size_attr])
        size_scaled = ((size - size.min()) / (size.max() - size.min())) * 1000
        if not is_numeric(color_attr):
            color_codes = pd.Categorical(df[color_attr]).codes
            scatter = ax.scatter(x, y, s=size_scaled, c=color_codes, cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5)
        else:
            scatter = ax.scatter(x, y, s=size_scaled, c=color, cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5)

        ax.set_xlabel(x_attr)
        ax.set_ylabel(y_attr)
        ax.set_title('CIA Factbook 2023')

        #safely remove existing colorbar if it exists and is valid
        if colorbar is not None and hasattr(colorbar, 'ax'):
            try:
                colorbar.remove()
            except Exception as e:
                print(f"Error while removing colorbar: {e}")

        #sdds color bar if color attribute is numeric
        if is_numeric(color_attr):
            # the colorbar kept moving everytime i changed the color variable so i fixed it
            ax.set_position([0.1, 0.1, 0.65, 0.8])
            colorbar = figure.colorbar(scatter, ax=ax, label=color_attr, fraction=0.05, pad=0.04)
        legend(ax, size_attr)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        canvas.draw() #refreshes canvas
    update_plot()

    #connects signals
    x_select.currentIndexChanged.connect(update_plot)
    y_select.currentIndexChanged.connect(update_plot)
    color_select.currentIndexChanged.connect(update_plot)
    size_select.currentIndexChanged.connect(update_plot)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
