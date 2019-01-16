from pylab import *

imsize = 512
grid_ref = linspace(-1, 1, imsize)
Y, X = meshgrid(grid_ref, grid_ref, indexing='ij')

ANG = arctan2(Y,X)
VX = sin(ANG)
VY = -cos(ANG)

figure()
quiver(VX[276:476:8, 20:220:8], VY[276:476:8, 20:220:8], scale=35.0)
tight_layout()
axis('scaled')
frame = gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
show()