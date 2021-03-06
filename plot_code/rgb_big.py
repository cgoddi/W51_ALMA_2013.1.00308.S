"""
REQUIRES aplpy branch my_master_mar2016
"""
import numpy as np
from astropy import coordinates
from astropy import units as u
import os
import pylab as pl
import aplpy
import paths
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy import wcs
import paths
from outflow_meta import e2e
from spectral_cube import SpectralCube


fn303 = paths.dpath('merge/moments/W51_b6_7M_12M.H2CO303_202.image.pbcor_medsub_max.fits')
fn321 = paths.dpath('merge/moments/W51_b6_7M_12M.H2CO321_220.image.pbcor_medsub_max.fits')
fn322 = paths.dpath('merge/moments/W51_b6_7M_12M.H2CO322_221.coarser.image.pbcor_medsub_max.fits')
fnc18o = paths.dpath('merge/moments/W51_b6_7M_12M.C18O2-1.image.pbcor_medsub_max.fits')
fnSO = paths.dpath('merge/moments/W51_b6_7M_12M.SO65-54.image.pbcor_medsub_max.fits')
fnku = paths.dpath('evla/W51Ku_BDarray_continuum_2048_both_uniform.hires.clean.image.fits')
fnhc3n = paths.dpath('merge/moments/W51_b6_7M_12M.HC3N24-23.image.pbcor_medsub_max.fits')
fnch3oh422 = paths.dpath('merge/moments/W51_b6_7M_12M.CH3OH422-312.image.pbcor_medsub_max.fits')
#fits303 = fits.open(fn303)
#fits321 = fits.open(fn321)
#fits322 = fits.open(fn322)

fitsKu = fits.open(fnku)
cutout_Ku = Cutout2D(fitsKu[0].data.squeeze(),
                     coordinates.SkyCoord('19:23:41.495','+14:30:40.48',unit=(u.hour,u.deg)),
                     2.22*u.arcmin, wcs=wcs.WCS(fitsKu[0].header).celestial)
fitsKu_cutout = fits.PrimaryHDU(data=cutout_Ku.data, header=cutout_Ku.wcs.to_header())
fitsKu_fn = "rgb/Kuband_e2e_cutout.fits"
fitsKu_cutout.writeto(fitsKu_fn, clobber=True)


def make_rgb(outname, redline='H2CO303_202', greenline='H2CO321_220', blueline='H2CO322_221',
             fntemplate=paths.dpath('merge/moments/W51_b6_7M_12M.{0}.image.pbcor_medsub_max.fits'),
             suffix="_auto",
             **kwargs):

    print(outname, suffix)
    rgb_cube_fits = outname
    if not os.path.exists(rgb_cube_fits):
        # does not return anything
        aplpy.make_rgb_cube([fntemplate.format(redline) if 'fits' not in redline else redline,
                             fntemplate.format(greenline) if 'fits' not in greenline else greenline,
                             fntemplate.format(blueline) if 'fits' not in blueline else blueline,],
                            rgb_cube_fits)

    rgb_cube_png = rgb_cube_fits[:-5]+suffix+".png"
    rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                                  embed_avm_tags=True, **kwargs)
    return rgb_im

make_rgb('full_h2co_12monly_rgb.fits',
         fntemplate=paths.dpath('12m/moments/W51_b6_12M.{0}.image.pbcor_medsub_max.fits'),
        )
make_rgb('h2co_hc3n_ch3oh_rgb.fits',
         blueline='HC3N24-23',
         greenline='CH3OH422-312')
make_rgb('h2co_so_hc3n_rgb.fits',
         blueline='HC3N24-23',
         greenline='SO65-54')
make_rgb('c18o_hc3n_ch3oh_rgb.fits',
         redline='C18O2-1',
         blueline='HC3N24-23',
         greenline='CH3OH422-312')
make_rgb('c18o_hc3n_so_rgb.fits',
         redline='C18O2-1',
         blueline='HC3N24-23',
         greenline='SO65-54')
make_rgb('ku_hc3n_ch3oh_rgb.fits',
         redline=fnku,
         blueline='HC3N24-23',
         greenline='CH3OH422-312')
make_rgb('ku_hc3n_ch3oh_rgb.fits',
         suffix="_max",
         pmax_r=99.75,
         pmax_b=99.9,
         pmax_g=99.9999,
         redline=fnku,
         blueline='HC3N24-23',
         greenline='CH3OH422-312')
make_rgb('hc3n_ch3oh_ocs_rgb.fits',
         greenline='OCS18-17',
         redline='HC3N24-23',
         blueline='CH3OH422-312')

rgb_cube_fits = 'full_h2co_rgb.fits'
if not os.path.exists(rgb_cube_fits):
    # does not return anything
    aplpy.make_rgb_cube([fn303, fn321, fn322,], rgb_cube_fits)

rgb_cube_png = rgb_cube_fits[:-5]+"_auto.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              embed_avm_tags=True)

rgb_cube_png = rgb_cube_fits[:-5]+"_setlevels.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              vmin_b=-0.005,
                              vmax_b=0.4,
                              vmin_g=-0.005,
                              vmax_g=0.4,
                              vmin_r=-0.005,
                              vmax_r=0.4,
                              embed_avm_tags=True)

rgb_cube_fits = 'c18o_h2co_ku_rgb.fits'
if not os.path.exists(rgb_cube_fits):
    # does not return anything
    aplpy.make_rgb_cube([fitsKu_fn, fn303, fnc18o,], rgb_cube_fits)

rgb_cube_png = rgb_cube_fits[:-5]+"_auto.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              embed_avm_tags=True)

rgb_cube_png = rgb_cube_fits[:-5]+"_setlevels.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              vmin_b=-0.05,
                              vmax_b=0.65,
                              vmin_g=-0.005,
                              vmax_g=0.4,
                              vmin_r=-0.0005,
                              vmax_r=0.1,
                              embed_avm_tags=True)

rgb_cube_png = rgb_cube_fits[:-5]+"_logred.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              vmin_b=-0.05,
                              vmax_b=0.65,
                              vmin_g=-0.005,
                              vmax_g=0.4,
                              vmin_r=-0.0005,
                              vmax_r=0.01,
                              stretch_r='log',
                              embed_avm_tags=True)

rgb_cube_fits = 'ku_so_c18o_rgb.fits'
if not os.path.exists(rgb_cube_fits):
    # does not return anything
    aplpy.make_rgb_cube([fitsKu_fn, fnSO, fnc18o,], rgb_cube_fits)

rgb_cube_png = rgb_cube_fits[:-5]+"_auto.png"
rgb_im = aplpy.make_rgb_image(data=rgb_cube_fits, output=rgb_cube_png,
                              embed_avm_tags=True)
