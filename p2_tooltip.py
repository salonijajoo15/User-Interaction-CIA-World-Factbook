import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSlider, QToolTip
from PyQt6.QtCore import Qt

def parse_arguments():
    parser = argparse.ArgumentParser(description='Linked Brushing Bubble Charts Tool with Tooltips')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the CSV file containing data')
    return parser.parse_args()


def main():
    args = parse_arguments()
    csv_path = args.input
    df = pd.read_csv(csv_path)
    #separating numeric and categorical so it doesnt give errors in graph
    numeric_columns = df.select_dtypes(include=[float, int]).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=[float, int]).columns.tolist()

    # overall layout
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Linked Brushing Bubble Charts with Tooltips')
    window.setGeometry(100, 100, 1800, 900)
    figure1, ax1 = plt.subplots(figsize=(8, 6))
    canvas1 = FigureCanvas(figure1)
    figure2, ax2 = plt.subplots(figsize=(8, 6))
    canvas2 = FigureCanvas(figure2)
    widget = QWidget()
    layout = QVBoxLayout()
    charts_layout = QHBoxLayout()
    charts_layout.addWidget(canvas1)
    charts_layout.addWidget(canvas2)
    control_panel_layout = QHBoxLayout()
    chart1_layout = QVBoxLayout()
    x_select1 = QComboBox()
    x_select1.addItems(numeric_columns)
    y_select1 = QComboBox()
    y_select1.addItems(numeric_columns)
    color_select1 = QComboBox()
    color_select1.addItems(df.columns)
    size_select1 = QComboBox()
    size_select1.addItems(numeric_columns)
    scaling_slider1 = QSlider(Qt.Orientation.Horizontal)
    scaling_slider1.setMinimum(1)
    scaling_slider1.setMaximum(2000)
    scaling_slider1.setValue(1000)

    #chart 1 layout
    chart1_layout.addWidget(QLabel('X-axis Chart 1:'))
    chart1_layout.addWidget(x_select1)
    chart1_layout.addWidget(QLabel('Y-axis Chart 1:'))
    chart1_layout.addWidget(y_select1)
    chart1_layout.addWidget(QLabel('Color Chart 1:'))
    chart1_layout.addWidget(color_select1)
    chart1_layout.addWidget(QLabel('Size Chart 1:'))
    chart1_layout.addWidget(size_select1)
    chart1_layout.addWidget(QLabel('Scaling factor'))
    chart1_layout.addWidget(scaling_slider1)

    #chart 2 layout
    chart2_layout = QVBoxLayout()
    x_select2 = QComboBox()
    x_select2.addItems(numeric_columns)
    y_select2 = QComboBox()
    y_select2.addItems(numeric_columns)
    color_select2 = QComboBox()
    color_select2.addItems(df.columns)
    size_select2 = QComboBox()
    size_select2.addItems(numeric_columns)
    scaling_slider2 = QSlider(Qt.Orientation.Horizontal)
    scaling_slider2.setMinimum(1)
    scaling_slider2.setMaximum(2000)
    scaling_slider2.setValue(1000)

    # Add Chart 2 widgets to layout
    chart2_layout.addWidget(QLabel('X-axis Chart 2:'))
    chart2_layout.addWidget(x_select2)
    chart2_layout.addWidget(QLabel('Y-axis Chart 2:'))
    chart2_layout.addWidget(y_select2)
    chart2_layout.addWidget(QLabel('Color Chart 2:'))
    chart2_layout.addWidget(color_select2)
    chart2_layout.addWidget(QLabel('Size Chart 2:'))
    chart2_layout.addWidget(size_select2)
    chart2_layout.addWidget(QLabel('Scaling factor'))
    chart2_layout.addWidget(scaling_slider2)
    control_panel_layout.addLayout(chart1_layout)
    control_panel_layout.addLayout(chart2_layout)
    layout.addLayout(charts_layout)
    layout.addLayout(control_panel_layout)
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    # globaladded everywhere as it helps to save it easily and update
    global colorbar1, colorbar2, scatter1, scatter2, selected_indices, tooltip1, tooltip2, highlight_circle1, highlight_circle2
    colorbar1 = colorbar2 = None
    scatter1 = scatter2 = None
    selected_indices = set()

    #initalizing tooltip for both the charts
    tooltip1 = QLabel(window)
    tooltip1.setStyleSheet("QLabel { background-color : lightcoral; border: 1px solid black; padding: 5px; }")
    tooltip1.hide()
    tooltip2 = QLabel(window)
    tooltip2.setStyleSheet("QLabel { background-color : lightcoral; border: 1px solid black; padding: 5px; }")
    tooltip2.hide()

    # initializing the circles that i use in both the charts to highlight it
    highlight_circle1 = highlight_circle2 = None

    def handle_categorical_column(column):
        if column in categorical_columns:
            return pd.Categorical(df[column]).codes
        return df[column]

    # i created a function to handle the hover
    def create_hover_tooltip(canvas, scatter, df, chart_name, tooltip, other_scatter, other_tooltip):
        def on_hover(event):
            global highlight_circle1, highlight_circle2
            if event.inaxes is None or scatter is None:
                #clear highlight when mouse isnt on bubble
                tooltip.hide()
                other_tooltip.hide()
                if highlight_circle1:
                    highlight_circle1.remove()
                    highlight_circle1 = None
                if highlight_circle2:
                    highlight_circle2.remove()
                    highlight_circle2 = None
                canvas.draw()
                if other_scatter:
                    other_scatter.figure.canvas.draw()
                return

            #check if there is a point being hovered over
            contains, index = scatter.contains(event)
            if contains:
                ind = index['ind'][0]
                data_info = df.iloc[ind]
                country_name = data_info.get('name', 'Unknown Country')
                tooltip_text = f"<b>{country_name}</b><br>"
                for col in df.columns:
                    tooltip_text += f"{col}: {data_info[col]}<br>"
                tooltip.setText(tooltip_text)
                tooltip.adjustSize()
                #move the tooltip to the mouse position
                window_x, window_y = canvas.mapToGlobal(canvas.pos()).x(), canvas.mapToGlobal(canvas.pos()).y()
                tooltip.move(window_x + event.x + 20, window_y + event.y + 20)
                tooltip.show()

                #highlight the point w black circle
                offsets = scatter.get_offsets()
                x, y = offsets[ind]
                if highlight_circle1:
                    highlight_circle1.remove()  #remove previous highlight
                highlight_circle1 = \
                ax1.plot(x, y, 'o', markerfacecolor='none', markeredgecolor='black', markersize=15, markeredgewidth=2)[
                    0]

                #highlight the corresponding point on the other plot as well
                if other_scatter:
                    other_x, other_y = other_scatter.get_offsets()[ind]
                    if highlight_circle2:
                        highlight_circle2.remove()  #remove previous highlight
                    highlight_circle2 = \
                    ax2.plot(other_x, other_y, 'o', markerfacecolor='none', markeredgecolor='black', markersize=15,
                             markeredgewidth=2)[0]
                    other_scatter.figure.canvas.draw()
                canvas.draw()

                #synchronize tooltips on the other chart
                other_tooltip.setText(tooltip_text)
                other_tooltip.adjustSize()
                other_window_x, other_window_y = other_scatter.figure.canvas.mapToGlobal(
                    other_scatter.figure.canvas.pos()).x(), other_scatter.figure.canvas.mapToGlobal(
                    other_scatter.figure.canvas.pos()).y()
                other_tooltip.move(other_window_x + event.x + 20, other_window_y + event.y + 20)
                other_tooltip.show()

            else:
                #hide tooltip and remove highlight if not hovering over a point
                tooltip.hide()
                other_tooltip.hide()
                if highlight_circle1:
                    highlight_circle1.remove()
                    highlight_circle1 = None
                if highlight_circle2:
                    highlight_circle2.remove()
                    highlight_circle2 = None
                canvas.draw()
                if other_scatter:
                    other_scatter.figure.canvas.draw()

        # connecting hover the way prof showed in brightspace
        canvas.mpl_connect('motion_notify_event', on_hover)

    # updating the plots
    def update_plots():
        global scatter1, scatter2, colorbar1, colorbar2, highlight_circle1, highlight_circle2
        x_attr1, y_attr1, color_attr1, size_attr1 = x_select1.currentText(), y_select1.currentText(), color_select1.currentText(), size_select1.currentText()
        x_attr2, y_attr2, color_attr2, size_attr2 = x_select2.currentText(), y_select2.currentText(), color_select2.currentText(), size_select2.currentText()
        scale_factor1 = scaling_slider1.value() / 1000
        scale_factor2 = scaling_slider2.value() / 1000

        #extract numeric data for plotiing
        def handle_numeric(attr, data):
            return pd.to_numeric(data[attr], errors='coerce').fillna(0)
        x1 = handle_numeric(x_attr1, df)
        y1 = handle_numeric(y_attr1, df)
        x2 = handle_numeric(x_attr2, df)
        y2 = handle_numeric(y_attr2, df)
        #normalizes bubble size
        size1 = pd.to_numeric(df[size_attr1], errors='coerce').fillna(1)
        size2 = pd.to_numeric(df[size_attr2], errors='coerce').fillna(1)
        size1_scaled = (size1 - size1.min()) / (size1.max() - size1.min()) * scale_factor1 * 1000
        size2_scaled = (size2 - size2.min()) / (size2.max() - size2.min()) * scale_factor2 * 1000

        #color attributes
        color1 = handle_categorical_column(color_attr1)
        color2 = handle_categorical_column(color_attr2)
        ax1.clear()
        scatter1 = ax1.scatter(x1, y1, s=size1_scaled, c=color1, cmap='viridis', alpha=1.0, edgecolors='w',
                               linewidth=0.5)
        ax1.set_xlabel(x_attr1)
        ax1.set_ylabel(y_attr1)
        ax1.set_title('Chart 1')
        ax2.clear()
        scatter2 = ax2.scatter(x2, y2, s=size2_scaled, c=color2, cmap='viridis', alpha=1.0, edgecolors='w',
                               linewidth=0.5)
        ax2.set_xlabel(x_attr2)
        ax2.set_ylabel(y_attr2)
        ax2.set_title('Chart 2')

        #legends for bubble size
        add_size_legend(ax1, size_attr1, scale_factor1, df)
        add_size_legend(ax2, size_attr2, scale_factor2, df)

        # kept giving error so made it dynamic
        if colorbar1 is None:
            colorbar1 = figure1.colorbar(scatter1, ax=ax1, label=color_attr1)
        else:
            colorbar1.set_label(color_attr1)
            colorbar1.update_normal(scatter1)

        if colorbar2 is None:
            colorbar2 = figure2.colorbar(scatter2, ax=ax2, label=color_attr2)
        else:
            colorbar2.set_label(color_attr2)
            colorbar2.update_normal(scatter2)
        canvas1.draw()
        canvas2.draw()

        #this reapplies the tooltipa after updating
        create_hover_tooltip(canvas1, scatter1, df, "Chart 1", tooltip1, scatter2, tooltip2)
        create_hover_tooltip(canvas2, scatter2, df, "Chart 2", tooltip2, scatter1, tooltip1)

        # Reset highlight circles after plot update
        highlight_circle1 = highlight_circle2 = None

        # Update highlight
        highlight_selected()

    # Function to highlight selected bubbles and keep non-selected transparent
    def highlight_selected():
        global scatter1, scatter2
        if selected_indices:
            alphas1 = [1.0 if i in selected_indices else 0.2 for i in range(len(df))]
            alphas2 = [1.0 if i in selected_indices else 0.2 for i in range(len(df))]
        else:
            # reserting to original color
            alphas1 = [1.0 for _ in range(len(df))]
            alphas2 = [1.0 for _ in range(len(df))]
        scatter1.set_alpha(alphas1)
        scatter2.set_alpha(alphas2)
        # redrawaing once its done
        canvas1.draw()
        canvas2.draw()

    #function to reset the selection and revert bubbles to the original state
    def reset_selection(event):
        global selected_indices
        selected_indices.clear()
        highlight_selected()

    def add_size_legend(ax, size_attr, scale_factor, df):
        size_values = pd.to_numeric(df[size_attr], errors='coerce').fillna(0)
        small = size_values.quantile(0.25) #used this as it was easier here with so much code
        medium = size_values.median()
        big = size_values.max()
        #normalizing bubbles as values were tooooo large
        min_bubble_size = (small / size_values.max()) * scale_factor * 1000
        median_bubble_size = (medium / size_values.max()) * scale_factor * 1000
        max_bubble_size = (big / size_values.max()) * scale_factor * 1000
        legend_sizes = [min_bubble_size, median_bubble_size, max_bubble_size]
        legend_labels = [f'{small:.1e}', f'{medium:.1e}', f'{big:.1e}']
        for size, label in zip(legend_sizes, legend_labels):
            ax.scatter([], [], s=size, color='gray', alpha=0.5, edgecolor='black', label=label)
        ax.legend(title=size_attr, title_fontsize='13', loc="upper right", frameon=True, fontsize='10', scatterpoints=1)

    def on_select(eclick, erelease, chart='left'):
        global selected_indices
        selected_indices.clear() #clear previous selections

        if chart == 'left':#checks which chart is being selected
            x_min, x_max = sorted([eclick.xdata, erelease.xdata])
            y_min, y_max = sorted([eclick.ydata, erelease.ydata])

            for i in range(len(df)):#itterate through all data points to see which ones fall within the selection rectangle
                x_value = df.iloc[i][x_select1.currentText()]
                y_value = df.iloc[i][y_select1.currentText()]
                if x_min <= x_value <= x_max and y_min <= y_value <= y_max:
                    selected_indices.add(i)
        elif chart == 'right': #same for right
            x_min, x_max = sorted([eclick.xdata, erelease.xdata])
            y_min, y_max = sorted([eclick.ydata, erelease.ydata])

            for i in range(len(df)):
                x_value = df.iloc[i][x_select2.currentText()]
                y_value = df.iloc[i][y_select2.currentText()]
                if x_min <= x_value <= x_max and y_min <= y_value <= y_max:
                    selected_indices.add(i)

        highlight_selected()#update the charts to reflect the selection by highlighting selected points

        # making the rectangle box disappear as soon as im done selectingrectangle box and make it disappear after selection
        rect_selector1.set_active(False)
        rect_selector2.set_active(False)
        rect_selector1.set_visible(False)
        rect_selector2.set_visible(False)
        canvas1.draw()  #its going to pullup the canvases again without the box
        canvas2.draw()
        #and this helps to select the rectangle box again
        rect_selector1.set_active(True)
        rect_selector2.set_active(True)

    #rectangle selector tool
    rect_selector1 = RectangleSelector(ax1, lambda eclick, erelease: on_select(eclick, erelease, 'left'), useblit=True, interactive=True)
    rect_selector2 = RectangleSelector(ax2, lambda eclick, erelease: on_select(eclick, erelease, 'right'), useblit=True, interactive=True)
    update_plots()
    # so when you click on the screen the graph resets to otiginal  colors.
    canvas1.mpl_connect('button_press_event', reset_selection)
    canvas2.mpl_connect('button_press_event', reset_selection)
    x_select1.currentIndexChanged.connect(update_plots)
    y_select1.currentIndexChanged.connect(update_plots)
    color_select1.currentIndexChanged.connect(update_plots)
    size_select1.currentIndexChanged.connect(update_plots)
    scaling_slider1.valueChanged.connect(update_plots)
    x_select2.currentIndexChanged.connect(update_plots)
    y_select2.currentIndexChanged.connect(update_plots)
    color_select2.currentIndexChanged.connect(update_plots)
    size_select2.currentIndexChanged.connect(update_plots)
    scaling_slider2.valueChanged.connect(update_plots)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
