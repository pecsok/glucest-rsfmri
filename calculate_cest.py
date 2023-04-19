import os
import numpy as np
from ctypes import cdll, c_double, c_int, c_longlong, c_float
from numpy.ctypeslib import ndpointer
from anisotropic_diffusion import anisodiff_3d
from scipy.ndimage import convolve


def calc_raw_cest(CESTppm, cest_ppm_list, neg_img, pos_img, brain_mask):
    # calculate raw CEST map pushbutton7
    ppm_diff = [abs(ppm - CESTppm) for ppm in cest_ppm_list]
    img_idx = [i for i, x in enumerate(ppm_diff) if x == min(ppm_diff)]
    norm_img = neg_img[img_idx, :, :]
    norm_img = np.squeeze(norm_img)
    img2 = pos_img[img_idx, :, :]
    img2 = np.squeeze(img2)
    raw_cest = np.multiply(norm_img - img2, brain_mask)
    norm_ppm = - CESTppm
    brain_idx = brain_mask > 0

    raw_cest[brain_idx] = 100.0 * \
        np.divide(raw_cest[brain_idx], norm_img[brain_idx])

    return raw_cest

# B0correctedCEST2Dimg_AS.m
def calc_2d_b0_cest(ppm, ppm_list, pos_img, neg_img, b0map, brain_mask):

    [_, x, y] = pos_img.shape
    pos_img_out = np.zeros((x, y))
    neg_img_out = np.zeros((x, y))

    ppm_list = np.transpose(ppm_list)

    # if (min(abs(ppm_list)) > 0.01):
    poly_deg = 2

    for i in range(x):
        for j in range(y):
            if brain_mask[i, j] <= 0:
                continue

            b0offset = b0map[i, j]
            ppm_b0_corr_pos = ppm_list - b0offset
            ppm_b0_corr_neg = ppm_list + b0offset

            pos_array = np.squeeze(pos_img[:, i, j])
            neg_array = np.squeeze(neg_img[:, i, j])

            pp_fit = np.polyfit(ppm_b0_corr_pos, pos_array, poly_deg)
            np_fit = np.polyfit(ppm_b0_corr_neg, neg_array, poly_deg)

            pos_b0_corr_ppm = np.polyval(pp_fit, ppm)
            neg_b0_corr_ppm = np.polyval(np_fit, ppm)

            pos_img_out[i, j] = pos_b0_corr_ppm
            neg_img_out[i, j] = neg_b0_corr_ppm

    b0cest_map = np.divide(
        100.0 * (neg_img_out - pos_img_out), neg_img_out + 0.01)

    return b0cest_map


def calc_3d_b0_cest(ppm, ppm_list, pos_img, neg_img, b0map, brain_mask):
    # load c function calc_b0_map and define return type and argument types
    b0b1_lib = os.path.realpath(__file__)
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'scripts' folder
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'library' folder
    b0b1_lib = os.path.join(b0b1_lib, 'library', 'calc_b0corrected_cest.so')
    lib = cdll.LoadLibrary(b0b1_lib)
    calc_b0corrected_cest = lib.calc_b0corrected_cest

    calc_b0corrected_cest.restype = ndpointer(dtype=c_double,
                                              shape=(brain_mask.shape[0] * 2,
                                                     brain_mask.shape[2],
                                                     brain_mask.shape[1]))

    calc_b0corrected_cest.argtypes = [c_double,
                                      ndpointer(dtype=c_double, ndim=1,
                                                flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=c_double, ndim=4,
                                                flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=c_double, ndim=4,
                                                flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=c_double, ndim=3,
                                                flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=c_longlong,
                                                ndim=3, flags='C_CONTIGUOUS'),
                                      c_int, c_int]

    ppm = float(ppm)
    ppm_list = np.asarray(ppm_list)
    pos_img = np.ascontiguousarray(np.swapaxes(pos_img, 2, 3))
    neg_img = np.ascontiguousarray(np.swapaxes(neg_img, 2, 3))
    b0map = np.ascontiguousarray(np.swapaxes(b0map, 1, 2))
    brain_mask = np.ascontiguousarray(
        np.swapaxes(brain_mask.astype(int), 1, 2))
    nppm = len(ppm_list)
    nelem = brain_mask.size

    out = calc_b0corrected_cest(ppm, ppm_list,
                                pos_img, neg_img, b0map,
                                brain_mask,
                                nppm, nelem)

    out = np.swapaxes(out, 1, 2)
    b0_corr_pos = out[0:brain_mask.shape[0]]
    b0_corr_neg = out[brain_mask.shape[0]: brain_mask.shape[0] * 2]

    # line 1020 in CEST3DNEW.m
    # norm_img = b0_corr_neg

    return [b0_corr_pos, b0_corr_neg]


# calculate b0 corrected cest
def calc_b0_cest(ppm, ppm_list, pos_img, neg_img, b0map, brain_mask, dim):

    if dim == 2:
        b0_cest = calc_2d_b0_cest(ppm, ppm_list, pos_img, neg_img,
                                  b0map, brain_mask)
    else:
        b0_cest = calc_3d_b0_cest(ppm, ppm_list, pos_img, neg_img,
                                  b0map, brain_mask)

    return b0_cest


def calc_2d_b0b1_cest(b1map, seg_mask, mode, b0cest_map, brain_mask):

    b1cr = b1map + 0.000001
    csf_idx = seg_mask == 1
    gm_idx = seg_mask == 2
    wm_idx = seg_mask == 3

    if mode == "hippocampus":
        gm_calib = [-24.055, 54.398, -22.156]
        wm_calib = [-59.693, 126.01, -60.494]
    elif mode == "syrp":
        gm_calib = [-33.78, 69.838, -28.388]
        wm_calib = [-56.792, 111.98, -50.655]

    map = b0cest_map
    cest_max = sum(wm_calib) * (1 + 0 * b1cr)
    map[wm_idx] = b0cest_map[wm_idx] + cest_max[wm_idx] - \
        (wm_calib[2] * (np.power(b1cr[wm_idx], 3)) +
         wm_calib[1] * (np.power(b1cr[wm_idx], 2)) +
         wm_calib[0] * b1cr[wm_idx])

    cest_max = sum(gm_calib) * (1 + 0 * b1cr)
    map[gm_idx] = b0cest_map[gm_idx] + cest_max[gm_idx] - \
        (gm_calib[2] * (np.power(b1cr[gm_idx], 3)) +
         gm_calib[1] * (np.power(b1cr[gm_idx], 2)) +
         gm_calib[0] * b1cr[gm_idx])

    map[csf_idx] = np.divide(b0cest_map[csf_idx], b1cr[csf_idx] + 0.01)
    b0b1cest_map = np.multiply(map, brain_mask)

    return b0b1cest_map


def im_filt_new(img, kernel_size):

    filt = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    img_filtered = convolve(img, filt, mode='nearest')

    return img_filtered


def calc_3d_b0b1_cest(b1map, cest_b1, b0_corr_pos, b0_corr_neg, t1_map, brain_mask):

    [d, h, w] = brain_mask.shape
    pimg = np.zeros(brain_mask.shape)
    nimg = np.zeros(brain_mask.shape)
    for k in range(d):
        b1_filt = im_filt_new(b1map[k], 2)
        pimg[k] = b0_corr_pos[k] / (b1_filt + 0.001)
        nimg[k] = b0_corr_neg[k] / (b1_filt + 0.001)

    b0b1_lib = os.path.realpath(__file__)
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'scripts' folder
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'library' folder
    b0b1_lib = os.path.join(b0b1_lib, 'library')

    num_masks = np.genfromtxt(os.path.join(b0b1_lib, 'num_masks.txt'))
    num_masks = int(num_masks)
    t1_range = np.genfromtxt(os.path.join(b0b1_lib, 'intervals.csv'),
                             delimiter=',')
    b1_fit_pars = np.genfromtxt(os.path.join(b0b1_lib, 'b1_fit_pars.csv'),
                                delimiter=',')

    t1_idx = np.zeros(brain_mask.shape, dtype=int)
    sort_mask = np.zeros((h, w))

    for k in range(d):
        roi_mask = brain_mask[k]
        idx_img = t1_map[k]
        for j in range(w):
            for i in range(h):
                sort_mask[i, j] = 0.0

                if roi_mask[i, j] == 1:
                    curr_val = idx_img[i, j]
                    m = 0
                    while m < num_masks:
                        if t1_range[0, m] <= curr_val <= t1_range[1, m]:
                           t1_idx[k, i, j] = m + 1
                           sort_mask[i, j] = 1
                           m = num_masks
                        else:
                            sort_mask[i, j] = 0.0
                            m = m + 1

                    if sort_mask[i, j] == 0:
                        t1_idx[k, i, j] = num_masks

    [d, h, w] = brain_mask.shape

    for k in range(d):
        roi_mask = brain_mask[k]
        for j in range(w):
            for i in range(h):
                if roi_mask[i, j] > 0:
                    rel_b1 = b1map[k, i, j]
                    mask_idx = t1_idx[k, i, j]

                    if mask_idx >= 1:
                        param = b1_fit_pars[mask_idx - 1]
                        bn = param[0]
                        cn = param[1]
                        dn = param[2]
                        en = param[3]

                        bp = param[4]
                        cp = param[5]
                        dp = param[6]
                        ep = param[7]

                        x = cest_b1

                        ref_neg = en * (1 + (bn * np.power(x, 2) /
                                             (cn * np.power(x, 2) + 1)) -
                                        dn * np.power(x, 2))
                        ref_pos = ep * (1 + (bp * np.power(x, 2) /
                                             (cp * np.power(x, 2) + 1)) -
                                        dp * np.power(x, 2))

                        x = cest_b1 * rel_b1

                        val_neg = en * (1 + (bn * np.power(x, 2) /
                                             (cn * np.power(x, 2) + 1)) -
                                        dn * np.power(x, 2))
                        val_pos = ep * (1 + (bp * np.power(x, 2) /
                                             (cp * np.power(x, 2) + 1)) -
                                        dp * np.power(x, 2))

                        pimg[k, i, j] = pimg[k, i, j] * ref_pos / val_pos
                        nimg[k, i, j] = nimg[k, i, j] * ref_neg / val_neg

                    else:
                        pimg[k, i, j] = 0.0
                        nimg[k, i, j] = 0.0

                else:
                    pimg[k, i, j] = 0.0
                    nimg[k, i, j] = 0.0

    b0b1cest_map = 100.0 * ((nimg - pimg) / (nimg + 0.1))

    return b0b1cest_map


# calculate b0b1 corrected cest (this is the final output)
def calc_b0b1_cest(b1map, brain_mask, seg_mask = None, mode = None,
                   b0_cest_map = None, cest_b1 = None, t1_map = None,
                   b0_corr_pos = None, b0_corr_neg = None):

    # if seg_mask is given, it is a 2D cest image
    if seg_mask is not None:
        b0b1_cest = calc_2d_b0b1_cest(b1map, seg_mask, mode,
                                      b0_cest_map, brain_mask)
    else:
        b0b1_cest = calc_3d_b0b1_cest(b1map, cest_b1, b0_corr_pos, b0_corr_neg,
                                      t1_map, brain_mask)

    return b0b1_cest
