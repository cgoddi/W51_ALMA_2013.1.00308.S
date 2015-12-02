import numpy as np
from calibrated_configuration import field, phasecenter, cell, imsize, weighting, robust, threshold, spws_12m, spws_7m, finalvis12m, finalvis7m

for spwnum in '1320':
    spwnum = int(spwnum)

    concatvis = 'w51_concat_7m12m.spw{0}.merge'.format(spwnum)
    if not os.path.exists(concatvis):
        print "# running cvel on all lines in spw{0}".format(spwnum)
        cvelvises = []
        spw = spws_12m[spwnum]
        for ss in spw.split(","):
            ss = int(ss)
            cvelvis12m = 'w51_concat.spw{0}.cvel'.format(ss)
            cvelvises.append(cvelvis12m)
            if not os.path.exists(cvelvis12m):
                cvel(vis=finalvis12m,
                     outputvis=cvelvis12m,
                     passall=False, field=field, spw=str(ss), selectdata=True,
                     timerange='', array='', antenna='', scan='', mode='frequency',
                     nchan=nchans_total[spwnum],
                     start='{0}MHz'.format(frange[spwnum][0]),
                     width='{0}kHz'.format(fstep[spwnum]), interpolation='linear',
                     phasecenter='', restfreq='', outframe='LSRK', veltype='radio',
                     hanning=False,)
        spw = spws_7m[spwnum]
        for ss in spw.split(","):
            ss = int(ss)
            cvelvis7m = 'w51_concat_7m.spw{0}.cvel'.format(ss)
            cvelvises.append(cvelvis7m)
            if not os.path.exists(cvelvis7m):
                cvel(vis=finalvis7m,
                     outputvis=cvelvis7m,
                     passall=False, field=field, spw=str(ss), selectdata=True,
                     timerange='', array='', antenna='', scan='', mode='frequency',
                     nchan=nchans_total[spwnum],
                     start='{0}MHz'.format(frange[spwnum][0]),
                     width='{0}kHz'.format(fstep[spwnum]), interpolation='linear',
                     phasecenter='', restfreq='', outframe='LSRK', veltype='radio',
                     hanning=False,)
        concat(vis=cvelvises,
               concatvis=concatvis,)
    else:
        print "Already cvel'd spw {0} to {1}".format(spwnum, concatvis)
