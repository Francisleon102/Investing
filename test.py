import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

app = pg.mkQApp("3D Surface")

# 3D view
view = gl.GLViewWidget()
view.setWindowTitle("Surface Plot")
view.setCameraPosition(distance=20, elevation=20, azimuth=30)
view.show()

# Grid (optional but helpful)
grid = gl.GLGridItem()
grid.scale(1, 1, 1)
view.addItem(grid)

# Create surface data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

Z = np.sin(X) * np.cos(Y)   # any function z = f(x, y)

# Surface plot
surface = gl.GLSurfacePlotItem(
    x=x,
    y=y,
    z=Z,
    shader='shaded',        # try: 'heightColor', 'normalColor'
    smooth=True
)

view.addItem(surface)

pg.exec()
