import pyqtgraph as pg
from PyQt6 import QtWidgets
import sys
import pandas as pd


def display_text_in_plot():
    app = QtWidgets.QApplication(sys.argv)
    
    # Create a PlotWidget
    plot_widget = pg.PlotWidget(title="Text on Plot Example")
    plot_widget.show()
    plot_widget.resize(500, 400)
    
    # Plot some data (optional, just for context)
    plot_widget.plot([1, 2, 3, 4, 5], [2, 4, 1, 3, 5])
    
    # Add a TextItem
    # Position (x, y) coordinates within the data space
    text_item = pg.TextItem("Hello, PyQtGraph!", anchor=(0.5, 0.5), color='r')
    text_item.setPos(3, 4) # Position at x=3, y=4 in data coordinates
    plot_widget.addItem(text_item)
    
    # You can update the text later
    # text_item.setText("New Text")
    
    # Example of a LabelItem (fixed position on canvas)
    label_item = pg.LabelItem("Status: OK", parent=plot_widget.graphicsItem)
    label_item.anchor(itemPos=(0.0, 0.0), parentPos=(0.0, 0.0), pixelOffset=(10, 10)) # Top-left with offset

    sys.exit(app.exec())

if __name__ == "__main__":
    display_text_in_plot()
