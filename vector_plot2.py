from pylab import *

def interp2D2D(FX, FY, x, y):
    x0 = floor(x)
    y0 = floor(y)
    
    x1 = ceil(x)
    y1 = ceil(y)
    
    dx = x-x0
    print('temp3')
    dy = y-y0
    
    fx = ((1 - dx)*(1 - dy)*FX[x0, y0] +
          (dx)*(1 - dy)*FX[x, y0] + 
          (1 - dx)*(dy)*FX[x0, y] + 
          (dx)*(dy)*FX[x, y]) 

    fy = ((1 - dx)*(1 - dy)*FY[x0, y0] +
          (dx)*(1 - dy)*FY[x, y0] + 
          (1 - dx)*(dy)*FY[x0, y] + 
          (dx)*(dy)*FY[x, y]) 

    return (fx, fy)



imsize = (64, 64)

VX = zeros(imsize)
VY = zeros(imsize)

vessel_width = 10
vessel_range = arange(imsize[0]/2 - vessel_width, imsize[0]/2 + vessel_width)

VY[vessel_range, :] = 1

num_steps = 30

noise_scale = .3
VX = VX + noise_scale*randn(imsize[0], imsize[1])
VY = VY + noise_scale*randn(imsize[0], imsize[1])

out_range = setxor1d(arange(imsize[0]), vessel_range)
VX[out_range, :] = 0
VY[out_range, :] = 0

fig = figure()
quiver(VY, VX, color = '#A0A0A0')
# quiver(VY, VX)
for xi in vessel_range:
    X = zeros(num_steps)
    Y = zeros(num_steps)
    X[0] = xi
    Y[0] = 2

    for i in range(num_steps-1):
        (dx, dy) = interp2D2D(VX, VY, X[i], Y[i])
        X[i+1] = X[i] + 2.0*dx
        Y[i+1] = Y[i] + 2.0*dy

    plot(Y,X, linewidth=2)

tight_layout()
axis('scaled')
frame = gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
fig.savefig('vessel_plot_3.png')