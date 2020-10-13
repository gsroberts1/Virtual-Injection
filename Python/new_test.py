from seed import *
from bPath import *
from toa import *
from PCVIPR import *
import numpy as np
import time
import os
import datetime

#import GUI library -Tkinter
from tkinter import *
from tkinter import messagebox
#from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from tkinter import filedialog

sampling_options = [
    "plane",
    "spherical"
]

#today = date.today()
#date = today.strftime('%x')
gui=Tk()
gui.configure(bg='White')
gui.geometry('700x300')
gui.title("Virtual Injection")
#gui.iconbitmap('icon.ico')



def open_second():

    bot=Toplevel()
    bot.title = ("Virtual Injection")
    bot.configure(bg='White')
    bot.geometry('380x700')
    ttk.Label(bot, text="Select the folder containing MR scans", font=('Arial', 10), anchor="e", background='White', justify=LEFT).grid(
        column=0, row=7, pady=10, padx=30)
    ttk.Label(bot, text="Make sure that the selected folder contains the following files:\nCD.dat, comp_vd_1.dat, comp_vd_2.dat, comp_vd_3.dat,\nMAG.dat and pcvipr_header.txt.", font=('Arial', 10), anchor="e", background='White', justify=LEFT).grid(
        column=0, row=9, pady=10, padx=10)
    #bot.iconbitmap('icon.ico')

    ttk.Label(bot, text="Set following parameters:", font=('Arial', 10), anchor="e",
              background='White', justify=LEFT).grid(
        column=0, row=0, pady=10, padx=30)
    ttk.Label(bot,
              text="1. Select sampeling type:",
              font=('Arial', 10), anchor="w", background='White', justify=LEFT).grid(
        column=0, row=1, pady=10, padx=10)

     #set parameters
    sampling = StringVar(bot)
    sampling.set('plane')  # default value

    option1 = OptionMenu(bot, sampling, "plane", "spherical").grid(
            column=0, row=2, pady=10, padx=10)

    ttk.Label(bot,
              text="2. Select sampling radius:",
              font=('Arial', 10), anchor="w", background='White', justify=LEFT).grid(
        column=0, row=3, pady=10, padx=10)

    sampling_Radius= StringVar(bot)
    sampling_Radius.set('3.0')
    option2 = OptionMenu(bot, sampling_Radius, "1.0", "5.0","10.0","20.0").grid(
        column=0, row=4, pady=10, padx=10)

    ttk.Label(bot,
              text="2. Select tracking direction:",
              font=('Arial', 10), anchor="w", background='White', justify=LEFT).grid(
        column=0, row=5, pady=10, padx=10)

    reverse_TrackingFlag= StringVar(bot)
    reverse_TrackingFlag.set('Forward')
    option3 = OptionMenu(bot, reverse_TrackingFlag, 'Forward', 'Reverse' ).grid(
        column=0, row=6, pady=10, padx=10)

    progress = ttk.Progressbar(bot, orient=HORIZONTAL,
                           length=200, mode='determinate').grid(column=0, row=10, pady=10, padx=10)


    def get_data():
        global df, address_2, email, med_conditions

        import_folder = filedialog.askdirectory()



        # Add directory 'inject_data' if it doesn't exist
        dirName = 'inject_data_'+str(datetime.date.today())

        try:
            # Create target Directory
            os.mkdir(dirName)
        except FileExistsError:
            pass

        ########### FLAGS ##################
        ## Tracking/Sampling Flags
        samplingType = sampling.get()  # define sampling type ('spherical' or 'plane') give option
        samplingRadius = sampling_Radius.get()  # define radius of sphere or half-width of plane (1.0-50.0)
        samplingRadius=float(samplingRadius)
        reverseTrackingFlag = reverse_TrackingFlag.get()  # define direction of tracking (forward=0, reverse=1) give option forward/back
        if reverseTrackingFlag=='Forward':
            reverseTrackingFlag=0
        else:
            reverseTrackingFlag=1
        ## Pathline Flags
        spread = 0.15  # NOT SURE?????????????
        cutoff = 0.05  # was 0.70
        steps = 1200  # iterations (steps*offset = time elapsed)
        offset = 1  # temporal step size (ms)
        reducer = 2.0  #
        max_paths = 10000  # initial number of seeds (choose 1000-20 000 accuracy)
        start = time.clock()
        ###################################

        ## Load PCVIPR Data/Header

        ##chose folder option; rewrite files in inject_data; add timestamps to folder and/or data
        PLoader = PCVIPR(import_folder)
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



    browseButton = ttk.Button(bot, text="Select Data Folder", command=get_data, width=40
                              ).grid(column=0, row=8, pady=20, padx=20)

    #button_start= ttk.Button(bot2, text="Ok", command=run, width=40).grid(column=1, row=3, pady=20, padx=20)



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

title1=ttk.Label(gui, text="Virtual injection (VI) is a tool developed by University of Wisconsin used for visualizing blood flow from MR scans",background='White', font=('Arial', 10), justify=LEFT)
title1.grid(column=1, row=0, padx=10, pady=20)
title2=ttk.Label(gui, text="1. You will be required to select the data for visulaization (MR Scans)\n2. Set a treshold for analyzing data \n3. Select a plane or a sphere indicating the start of blood flow in a region",background='White', font=('Arial', 10), justify=LEFT)
title2.grid(column=1, row=1, padx=10, pady=10)
title=ttk.Label(gui ,text="VI was developed by UW scientists and it is used for clinical purposes. For professional clinical use only.", background='White', foreground='Grey',font=('Arial', 10), justify=LEFT)
title.grid(column=1, row=4, padx=20, pady=20)
#button1= ttk.Button(gui, text='Enter manually',  width=40, command=open)
#button1.grid(column=1, row=3, padx=10, pady=10)
button2=ttk.Button(gui, text='Continue', width=40, command=open_second)
button2.grid(column=1, row=2, padx=10, pady=10)





copyright_s=ttk.Label(gui, text="\u00a9 2020 UW Madison Department of Medical Physics",background='White', font=('Arial', 10), justify=LEFT)
copyright_s.grid(column=1, row=5, padx=50, pady=10)


exit=ttk.Button(gui, text='Exit', command=gui.quit, width=20)
exit.grid(column=1, row=5, padx=22, pady=10, sticky='e')
gui.mainloop()