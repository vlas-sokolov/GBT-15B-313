import pyspeckit
import numpy as np
from matplotlib import pylab as plt
from astropy import units as ut
from astropy.io import fits
import os

cloud = 'J'

file_mirex    = '/home/vsokolov/Data/BT12/IRDCs/{}-8umNIR_comb.fits'.format(cloud)
ag_dir = '/home/vsokolov/Projects/BTclouds/cut/'
file_ag = ag_dir + [f for f in os.listdir(ag_dir) if ('fits' in f and cloud in f)][0]

if cloud is 'J':
    ag_rms = 0.08 # measured by hand from ds9
    ag_lev = np.linspace(3*ag_rms,58*ag_rms,11) # 3-58 sigma levels, step of 5 rms (x11)
    scale1pc = 1/1.8e3
    vmin,vmax = 21,23
    Tmin,Tmax = 8,20
    Nmin,Nmax = 13,15
    xlim,ylim = (15,44),(16,43)
    dmin,dmax = 0.2,1
if cloud is 'I':
    ag_rms = 0.08 # measured by hand from ds9
    ag_lev = np.linspace(3*ag_rms,15*ag_rms,4) # 3-15 sigma levels, step of 3 rms (x4)
    scale1pc = 1/2.7e3
    vmin,vmax = 41,43
    Tmin,Tmax = 10,19
    Nmin,Nmax = 13,15
    xlim,ylim = (15,45),(10,40)
    dmin,dmax = 0.2,1
if cloud is 'E':
    ag_rms = 0.08 # measured by hand from ds9
    ag_lev = np.linspace(3*ag_rms,8*ag_rms,5) # 3-8 sigma levels, step of 1 rms
    scale1pc = 1/5.1e3
    vmin,vmax = 78.4,79.5
    Tmin,Tmax = 8,15
    Nmin,Nmax = 13,15
    xlim,ylim = (17,43),(20,46)
    dmin,dmax = 0.2,1

def zoomzoom(spc, xlim, ylim):
    spc.mapplot.axis.set_xlim(*xlim)
    spc.mapplot.axis.set_ylim(*ylim)

file_nh3_fit  = 'cloud{}_parameter_maps.fits'.format(cloud)

fit = fits.getdata(file_nh3_fit)
fit[:,:,:][fit[:,:,:]==0]=np.nan

plt.rc('text', usetex=True)

# plotting
spclst = []
for win in reversed(range(1,4)):
    file_nh3   = 'cloud{}/cloud{}_NH3_{}{}_base1.fits'.format(cloud,cloud,win,win)
    # putting it all in the list keeps interactive 
    # features of mapplot() active! yay!
    spclst.append(pyspeckit.Cube(file_nh3))
    spc = spclst[-1]
    spc.load_model_fit('cloud{}_pars.fits'.format(cloud), 
                npars=6,npeaks=1, _temp_fit_loc=(29,33))
    spc.mapplot()
    ##############################
    # TODO: make a pull request! #
    spc.smooth(3)                #
    ##############################
    if win==1: # kinetic temperature
        lab = r'$\mathrm{T_{kin},~K}$'
        parslice = 0
        #cmap = 'coolwarm'
        cmap = 'viridis'
        outfile = 'figures/cloud{}_Tkin.png'.format(cloud)
        zmin, zmax = Tmin, Tmax

    if win==2: # line centroid velocity
        lab = r'$\mathrm{V_{lsr},~km~s^{-1}}$'
        parslice = 4
        #cmap = 'coolwarm'
        cmap = 'viridis'
        outfile = 'figures/cloud{}_Vlsr.png'.format(cloud)
        zmin, zmax = vmin, vmax

    if win==3: # line width
        lab = r'$\sigma$, $\mathrm{km~s^{-1}}$'
        parslice = 3
        cmap = 'viridis'
        outfile = 'figures/cloud{}_sigma.png'.format(cloud)
        zmin, zmax = dmin, dmax

    spc.mapplot.plane = fit[parslice,:,:]
    spc.mapplot(cmap=cmap,estimator=None, vmin=zmin, vmax=zmax)
    spc.mapplot.FITSFigure.colorbar.set_axis_label_text(lab)
    spc.mapplot.FITSFigure.show_contour(file_ag,
    				    levels=ag_lev,
    				    colors='black')
    beam_gbt_nh3 = 30.00*ut.arcsecond
    spc.mapplot.FITSFigure.add_beam(major=beam_gbt_nh3,
    				minor=beam_gbt_nh3,
    				angle=0, edgecolor='black',
    				facecolor='white',
    				alpha=0.7)
    spc.mapplot.FITSFigure.add_scalebar(scale1pc * ut.radian,
                                        label='1 pc', color='black',
                                        corner = 'bottom right')
    spc.mapplot.FITSFigure.colorbar.set_axis_label_font(size='medium')
    spc.mapplot.canvas.set_window_title('Cloud {} NH3 ({},{})'.format(cloud,win,win))
    zoomzoom(spc,xlim,ylim)

    spc.mapplot.FITSFigure.save(outfile)
