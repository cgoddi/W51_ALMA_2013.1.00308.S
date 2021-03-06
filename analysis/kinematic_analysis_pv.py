import pvextractor
import os
import glob
import paths
from astropy import units as u
from astropy import coordinates
from astropy import wcs
from spectral_cube import SpectralCube

import pylab as pl

#fntemplate = 'full_W51e2cutout_spw{0}_lines.fits'
#medsubtemplate = 'full_W51e2cutout_spw{0}_lines_medsub.fits'

# c&p'd from ../regions/e2e_disk_pvextract.reg  ../regions/north_disk_pvextract.reg
northdiskycoords = "19:23:40.177,+14:31:06.50,19:23:39.923,+14:31:04.52".split(",")
e2diskycoords = "19:23:44.197,+14:30:37.34,19:23:43.960,+14:30:34.55,19:23:43.882,+14:30:32.21,19:23:43.851,+14:30:31.26".split(",")
e8diskycoords = "19:23:43.913,+14:30:29.96,19:23:43.874,+14:30:26.09".split(",")

for name, diskycoordtxt, vrange in (
    ('north', northdiskycoords, (45,75)),
    ('e8', e8diskycoords, (45,75)),
    ('e2', e2diskycoords, (45,70)),
   ):

    diskycoords = coordinates.SkyCoord(["{0} {1}".format(diskycoordtxt[jj],
                                                         diskycoordtxt[jj+1]) for
                                        jj in range(0, len(diskycoordtxt), 2)],
                                       unit=(u.hour, u.deg),
                                       frame='fk5')

    for fn in glob.glob(paths.dpath("12m/cutouts/W51_b6_12M*{0}*fits".format(name))):

        namesplit = fn.split(".")
        if name not in namesplit[3]:
            # e2 matches Acetone21120...
            continue

        assert 'cutout' in fn
        basename = ".".join([os.path.basename(namesplit[0]),
                             namesplit[1],
                             name+"_diskpv",
                             "fits"])
        outfn = paths.dpath(os.path.join("12m/pv/", basename))

        cube = SpectralCube.read(fn)
        cube.allow_huge_operations=True
        cube.beam_threshold = 5
        med = cube.median(axis=0)
        medsub = cube - med

        P = pvextractor.Path(diskycoords, 0.2*u.arcsec)
        extracted = pvextractor.extract_pv_slice(medsub, P)
        #extracted.writeto(outfn, clobber=True)

        ww = wcs.WCS(extracted.header)
        ww.wcs.cdelt[1] /= 1000.0
        ww.wcs.crval[1] /= 1000.0
        ww.wcs.cunit[1] = u.km/u.s
        ww.wcs.cdelt[0] *= 3600
        ww.wcs.cunit[0] = u.arcsec

        fig = pl.figure(1)
        fig.clf()
        ax = fig.add_axes([0.15, 0.1, 0.8, 0.8],projection=ww)
        ax.imshow(extracted.data, cmap='viridis')
        ax.set_xlabel("Offset [\"]")
        ax.set_ylabel("$V_{LSR}$ [km/s]")
        ax.set_ylim(ww.wcs_world2pix(0,vrange[0],0)[1],
                    ww.wcs_world2pix(0,vrange[1],0)[1])
        ax.set_aspect(4)
        fig.savefig(paths.fpath('pv/{0}/'.format(name)+basename.replace(".fits",".png")))


        #outflow_coords = coordinates.SkyCoord(["19:23:44.127 +14:30:32.30", "19:23:43.822 +14:30:36.64"], unit=(u.hour, u.deg), frame='fk5')
        #outflowpath = pvextractor.Path(outflow_coords, 0.2*u.arcsec)
        #extracted = pvextractor.extract_pv_slice(medsub, outflowpath)
        #extracted.writeto('W51e2_PV_outflowaxis_spw{0}.fits'.format(ii), clobber=True)
