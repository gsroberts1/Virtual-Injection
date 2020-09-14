from seed import *
from bPath import *
from toa import *
from PCVIPR import *
import numpy as np
import time

########### FLAGS ##################
## Tracking/Sampling Flags
samplingType = 'plane'  # define sampling type ('spherical' or 'plane')
samplingRadius = 3.0  # define radius of sphere or half-width of plane
reverseTrackingFlag = 0  # define direction of tracking (forward=0, reverse=1)

## Pathline Flags
spread = 0.15  # NOT SURE?????????????
cutoff = 0.05  # was 0.70
steps = 1200  # iterations (steps*offset = time elapsed)
offset = 1  # temporal step size (ms)
reducer = 2.0  #
max_paths = 10000  # initial number of seeds
start = time.clock()
###################################

## Load PCVIPR Data/Header
PLoader = PCVIPR('F:\\Virtual Injection\\140314_PATIENT_AVM\\PCVIPR')
CD = PLoader.getArray('CD.dat')
MAG = PLoader.getArray('MAG.dat')
VX = PLoader.getArray('comp_vd_1.dat')
VY = PLoader.getArray('comp_vd_2.dat')
VZ = PLoader.getArray('comp_vd_3.dat')

V = zeros((PLoader.resX, PLoader.resY, PLoader.resZ, 3))
V[:, :, :, 0] = VZ  # combine velocity arrays (N x N x N x 3)
V[:, :, :, 1] = VY  # note this is in mm/s
V[:, :, :, 2] = VX

CD = CD.astype('double')  # change CD to double
CD = CD / CD.max()  # normalize CD values from 0 to 1
axial = CD.max(0)  # get axial MIP
sagittal = CD.max(1)  # get sagittal MIP

## GUI for thresh selection
thresh = 0.09  # image threshold for vessel segmentation

fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)  # plot MIPs and subsequent angiograms with interactive thresh slider
ax1.imshow(axial, cmap='gray')
ax2.imshow((CD > thresh).max(0), cmap='gray')  # plot angio based on current thresh
ax3.imshow(sagittal, cmap='gray')
ax4.imshow((CD > thresh).max(1), cmap='gray')

plt.setp(ax1.get_xticklabels(), visible=False)  # get rid of axes and tick marks
plt.setp(ax1.get_yticklabels(), visible=False)
ax1.tick_params(axis='both', which='both', length=0)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax2.get_yticklabels(), visible=False)
ax2.tick_params(axis='both', which='both', length=0)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)
ax3.tick_params(axis='both', which='both', length=0)
plt.setp(ax4.get_xticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)
ax4.tick_params(axis='both', which='both', length=0)

axcolor = 'lightgoldenrodyellow'  # color of slider
axThresh = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)  # location of slider wrt plt
sThresh = Slider(axThresh, 'Thresh', 0.0, 1.0, valinit=thresh, valstep=0.01)  # form slider object


# Update function for when slider is moved
def update(val):
    thresh = sThresh.val  # grab threshold value (slider state)
    ax2.imshow((CD > thresh).max(0), cmap='gray')  # show new angiograms
    ax4.imshow((CD > thresh).max(1), cmap='gray')
    fig.canvas.draw_idle()  # draw out angigograms


sThresh.on_changed(update)  # when slider is moved, go to update function
plt.show()
thresh = sThresh.val  # pull new threshold value
plt.show(block='false')  # force user to exit figure before code proceeds


## View CD for sampling location
angio = CD > thresh  # create final angiogram
if samplingType == 'plane':
    fig, axs = plt.subplots(1)
    axs.imshow(sagittal, cmap='gray')  # show only sagittal plot for placement of axial seeding plane
    clickPts = plt.ginput(1)  # allow for interactive point selecting on plot
    slic = clickPts[0][1]  # get locations of selection
    axs.plot(range(PLoader.resZ), repeat(slic, PLoader.resZ), '-', linewidth=samplingRadius)  # show selection as line
    plt.draw_all()
    plt.show(block='false')  # force user to exit figure before code proceeds
elif samplingType == 'spherical':
    fig, axs = plt.subplots(ncols=2)
    axs[0].imshow(axial, cmap='gray')  # show MIPs
    axs[1].imshow(sagittal, cmap='gray')
    clickPts = fig.ginput(2, show_clicks='True', timeout=-1)  # select two points on both images
    row = clickPts[0][1]  # get row,col,slice in image space from point selection
    col1 = clickPts[0][0]
    col2 = clickPts[1][0]
    col = mean([col1, col2])  # average selected location in x (index selected twice from 2 views)
    slic = clickPts[1][1]
    axs[0].scatter(col1, row, marker='o', color='lime', alpha=0.8, s=(pi * samplingRadius ** 2))  # show selected points
    axs[1].scatter(col2, slic, marker='o', color='lime', alpha=0.8, s=(pi * samplingRadius ** 2))
    plt.draw_all()
    plt.show(block='false')  # force user to exit figure before code proceeds
else:
    print('ERROR: Need to define a suitable sampling type ("spherical" or "plane").')  # need to select one or the other

CD[angio] = thresh  # cap high CD signal at thresh, keep everything else same

conv = PLoader.resX / PLoader.fovX / 1000  # 320 pixels, 220 mm typically (assumes isotropy)
V *= conv  # convert to pixels/ms


## For reverse (venous) tracking
if reverseTrackingFlag == 1:
    V = -V  # reverse velocities
    offset = -offset  # reverse direction of step (for RK4)


## Plane sampling
allpaths = []
if samplingType == 'plane':
    samplingRadius = round(samplingRadius) # turn to int
    slic = int(round(slic))
    plane = np.sum(CD[slic-samplingRadius:slic+samplingRadius, :, :], axis=0)  # get slice of width*2
    plane = plane/(samplingRadius*2 + 1)  # average to preserve local values
    plane[angio[slic, :, :]] = thresh  # turn values in vessel back to thresh (averaging can change this)
    velDir = np.sum(V[slic-samplingRadius:slic+samplingRadius, :, :, 0], axis=0)/(samplingRadius*2 + 1)
    dplane = sign(velDir)  # get direction of z-velocity at every point in axial slice
    plane = plane==thresh  # binarize plane
    plane[dplane < 0] = 0  # discard spins moving in the opposite direction (-z direction)

    Xm, Ym = nonzero(plane)  # get list of all available points to sample
    for i in range(max_paths):
        allpaths.append(bPath([sampleInPlane(Xm, Ym, slic)]))  # create initial path list
elif samplingType == 'spherical':
    r0 = array([col, row, slic])
    for i in range(int(max_paths)):
        allpaths.append(bPath([sampleInSphere(samplingRadius, r0)]))
else:
    print('ERROR: Need to define a suitable sampling type ("spherical" or "plane").')


## Begin probabilist streamline generation
TOA = zeros(CD.shape)
stoppedpaths = []
for i in range(steps):
    print(('Iteration: ' + str(i)))
    stepPathsDisplaceRand(allpaths, V, offset, CD, spread, cutoff, reducer, PLoader)

    print('Length: ' + str(len(allpaths)))

    TOA = TOA + TOAMap(allpaths, CD.shape, max_paths / len(allpaths))
    if (i + 1) % 25 == 0:
        savename = 'inject_data/TOAf1_t%04d.npy' % i
        print(savename)
        save(savename, TOA.astype('uint16'))

print(('Time: ' + str(time.process_time() - start)))

# figure()
# imshow(CD[:,60:200,:].max(1), origin='upper')
# set_cmap('gray')
# colorbar()
# for path in allpaths:
#    path.plot((2,0))
# for path in stoppedpaths:
#    path.plot((2,0))
# savefig('out2.png')
# show()
