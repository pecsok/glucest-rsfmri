import os
import pydicom
import numpy as np
from math import pi
import nibabel as nib
from nibabel.nicom import csareader
from scipy.interpolate import interp1d
from write_images import write_image 


def mprage_func(tr, inv_times, nzslices, tr_flash, flip_angle, T1s, inv_eff):

    # line 5 of MPRAGEfunc.m
    # normal_sequence = true
    # water_excitation = false

    M0 = 1;
    flip_rad = flip_angle / 180 * pi

    # nimages == 2
    if 2 != len(flip_rad):
        temp = flip_rad

        for k in range(2):
            flip_rad[k] = temp

    # skip line 29-40 since we're only using default inversion efficiency value

    if len(nzslices) == 2:
        [nz_bef, nz_aft] = nzslices
        nzslices = sum(nzslices)
    elif len(nzslices == 1):
        nz_bef = nzslices / 2
        nz_aft = nzslices / 2

    e_1 = np.exp(np.divide(-tr_flash, T1s))
    ta = nzslices * tr_flash
    ta_bef = nz_bef * tr_flash
    ta_aft = nz_aft * tr_flash

    td = np.zeros((inv_times.shape[0] + 1))
    e_td = np.zeros((inv_times.shape[0] + 1))

    td[0] = inv_times[0] - ta_bef
    e_td[0] = np.exp(np.divide(-td[0], T1s))
    # nimages always 2
    td[2] = tr - inv_times[1] - ta_aft
    e_td[2] = np.exp(np.divide(-td[2], T1s))

    # nimages == 2 and k == 1
    td[1] = inv_times[1] - inv_times[0] - ta
    e_td[1] = np.exp(np.divide(-td[1], T1s))

    # k == 0, 1
    cosalfa_e1 = np.zeros(flip_rad.shape)
    one_minus_e1 = np.zeros((2))
    sinalfa = np.zeros(flip_rad.shape)
    for k in range(0, 2):
        cosalfa_e1[k] = np.cos(flip_rad[k]) * e_1
        one_minus_e1[k] = 1 - e_1
        sinalfa[k] = np.sin(flip_rad[k])

    # skip line 76-105
    mz_steady_state = np.divide(1,
                                (1 +
                                 np.multiply(inv_eff * np.power(np.prod(cosalfa_e1),
                                                                nzslices),
                                             np.prod(e_td))))
    mz_ss_numerator = M0 * (1 - e_td[0])

    for k in range(0, 2):
        mz_ss_numerator = mz_ss_numerator * np.power(cosalfa_e1[k],
                                                     nzslices) + \
                          np.divide(np.multiply(np.multiply(M0, 1 - e_1),
                                                1 - np.power(cosalfa_e1[k],
                                                             nzslices)),
                                    1 - cosalfa_e1[k])

        mz_ss_numerator = np.multiply(mz_ss_numerator, e_td[k + 1]) + \
                          M0 * (1 - e_td[k + 1])

    mz_steady_state = mz_steady_state * mz_ss_numerator

    m = 0
    temp = np.multiply(-inv_eff * mz_steady_state * e_td[0] + \
                       np.multiply(M0, 1 - e_td[0]),
                       np.power(cosalfa_e1[m], nz_bef)) + \
           np.divide(np.multiply(np.multiply(M0, 1 - e_1),
                                 1 - np.power(cosalfa_e1[m],
                                              nz_bef)),
                     1 - cosalfa_e1[m])

    signal = np.zeros(sinalfa.shape)
    signal[0] = sinalfa[m] * temp

    # line 133, nimages == 2 & m == 1
    m = 1
    temp = temp * np.power(cosalfa_e1[m - 1], nz_aft) + \
           np.divide(np.multiply(np.multiply(M0, 1 - e_1),
                                 1 - np.power(cosalfa_e1[m - 1] , nz_aft)),
                     1 - cosalfa_e1[m - 1])

    temp = np.multiply(temp * e_td[m] + M0 * (1 - e_td[m]),
                       np.power(cosalfa_e1[m], nz_bef)) + \
           np.divide(np.multiply(np.multiply(M0, 1 - e_1),
                                 1 - np.power(cosalfa_e1[m], nz_bef)),
                     1 - cosalfa_e1[m])

    signal[m] = sinalfa[m] * temp

    return signal


def mp2rage_lookuptable(mp2rage):

    all_data = 0
    # line 14 of MP2RAGE_lookuptable.m
    [inv_times_a, inv_times_b] = mp2rage["TIs"]
    t1_vector = np.arange(0.05, 5.05, 0.05)

    nzslices = mp2rage["NZslices"]
    if len(nzslices) == 2:
        [nz_bef, nz_aft] = nzslices
        nzslices2 = nzslices
        nzslices = sum(nzslices)

    elif len(nzslices) == 1:
        nz_bef = nzslices / 2
        nz_aft = nzslices / 2
        nzslices2 = nzslices

    j = 0
    tr_flash = mp2rage["TR_Flash"]
    inv_eff = mp2rage["inversion_eff"]
    signal = np.zeros((2, len(t1_vector), 1))
    for t1 in t1_vector:
        for tr in mp2rage["TR"]:
            for a in inv_times_a:
                for b in inv_times_b:
                    # line 45: b1_vector == 1 so no need for for loop
                    inv_times_2 = np.array([a, b])

                    if (np.diff(inv_times_2)[0] >= nzslices * tr_flash and \
                       a >= nz_bef * tr_flash) and \
                       b <= tr - nz_aft * tr_flash:

                       signal[0:2, j, 0] = mprage_func(tr,
                                                       inv_times_2,
                                                       nzslices2, tr_flash,
                                                       mp2rage["flip_degrees"],
                                                       t1, inv_eff)

                    else:
                        signal[0:2, j, 0] = 0
        j = j + 1

    intensity = np.squeeze(
                           np.divide(
                                     np.real(
                                             np.multiply(
                                                         signal[0],
                                                         np.conj(signal[1])
                                                         )
                                             ),
                                     (np.power(
                                               abs(signal[0]),
                                               2
                                               ) + \
                                      np.power(
                                               abs(signal[1]),
                                               2
                                               )
                                     )
                                     )
                          )
    t1_vector = np.squeeze(t1_vector)

    # line 71 (all_data == 0)
    min_idx = np.where(intensity == np.max(intensity))[0][0]
    max_idx = np.where(intensity == np.min(intensity))[0][0]
    intensity = intensity[min_idx:max_idx]
    t1_vector = t1_vector[min_idx:max_idx]
    intensity_before_comb = np.squeeze(signal[min_idx:max_idx, 0])
    intensity[[0, -1]] = [0.5, -0.5]

    return [intensity, t1_vector, intensity_before_comb]


def t1_estimate_mp2rage(mp2rage_img, mp2rage):

    # line 36 of T1estimateMP2RAGE.m
    # nimage is always == 2
    [intensity, t1_vector, _] = mp2rage_lookuptable(mp2rage)
    t1 = interp1d(intensity, t1_vector)

    if np.max(abs(mp2rage_img)) > 1:
        t1 = t1(-0.5 + 1 / 4095 * mp2rage_img)
    else:
        t1 = t1(mp2rage_img)

    t1[t1 is None] = 0
    t1 = t1 * 1000

    # TODO: need to put header info with t1 from mp2rage
    return t1


def calc_t1(uni_nii, uni_dicom, out):

    # if uni_nii is None
    # line 66 of mp2rqage_calcT1.m
    hdr = pydicom.read_file(uni_dicom, stop_before_pixels=True)
    hdr_csa = csareader.get_csa_header(hdr, 'series')

    # retrieve the protocol-inside-a-string-inside-a-protocol-inside-a-dicom-attribute
    # NOTE: tested on one DICOM file from one Siemens scanner
    mrPhoenixProtocol = dict(
            t.split(' = ') for t in                     # convert key = value format to python dictionary
             hdr_csa['tags']['MrPhoenixProtocol']['items'][0] # get ASCII header
                 .split('### ASCCONV BEGIN')[1]         # strip out the XML-like prefix and suffix
                 .split('### ASCCONV END ###')[0]
                 .replace('\t', '')                     # remove tabs
                 .split('\n')                           # split into list by newline
             [1:-1]                                     # ignore first and last (empty) elements
        )

    mp2rage = {}
    mp2rage.update({"TR_Flash": 0.006})
    mp2rage.update({"inversion_eff": 0.6500})
    mp2rage.update({"B0": float(hdr.MagneticFieldStrength)})
    mp2rage.update({"TR": [float(hdr.RepetitionTime)]})
    mp2rage.update({"filename": uni_nii})

    a = mrPhoenixProtocol["alTI[0]"]
    b = mrPhoenixProtocol["alTI[1]"]

    if type(a) is str:
        a = np.array([0.000001 * float(a)])
    else:
        a = np.array([0.000001 * float(x) for x in a])

    if type(b) is str:
        b = np.array([0.000001 * float(b)])
    else:
        b = np.array([0.000001 * float(x) for x in b])

    mp2rage.update({"TIs": np.array([a, b])})

    flip_degrees = np.array([float(mrPhoenixProtocol["adFlipAngleDegree[0]"]),
                             float(mrPhoenixProtocol["adFlipAngleDegree[1]"])])
    mp2rage.update({"flip_degrees": flip_degrees})

    nzslices = int(mrPhoenixProtocol["sKSpace.lImagesPerSlab"])
    nzslices = nzslices * np.array([6/8 - 0.5, 0.5])
    mp2rage.update({"NZslices": nzslices})

    mp2rage_nii = nib.load(uni_nii)
    mp2rage_affine = mp2rage_nii.affine
    mp2rage_img = np.array(mp2rage_nii.get_fdata())
    t1_map = t1_estimate_mp2rage(mp2rage_img, mp2rage)

    # write the t1_map as nifti and return t1_map
    write_image(t1_map, out, mp2rage_affine, mp2rage_nii.get_data_dtype(), 't1')

    return t1_map
