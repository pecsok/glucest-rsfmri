import os
import numpy as np
from scipy.signal.signaltools import wiener
from scipy.interpolate import interp2d, interpn
from ctypes import cdll, c_double, c_int, c_longlong, c_float
from numpy.ctypeslib import ndpointer
import anisotropic_diffusion as ad


def calc_3d_b0_map(ppmlist, pimg, nimg, brain_mask, step=0.0050):

    # load c function calc_b0_map and define return type and argument types
    b0b1_lib = os.path.realpath(__file__)
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'scripts' folder
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'library' folder
    b0b1_lib = os.path.join(b0b1_lib, 'library', 'calc_3d_b0_map.so')
    lib = cdll.LoadLibrary(b0b1_lib)
    calc_b0_map = lib.calc_3d_b0_map

    calc_b0_map.restype = ndpointer(dtype=c_double, shape=(brain_mask.shape[0],
                                                           brain_mask.shape[2],
                                                           brain_mask.shape[1]))

    calc_b0_map.argtypes = [ndpointer(dtype=c_double, ndim=1,
                                      flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_double, ndim=4,
                                      flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_double, ndim=4,
                                      flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_longlong, ndim=3,
                                      flags='C_CONTIGUOUS'),
                            c_int, c_int, c_int]

    # number of elements in ppmlist
    nppm = len(ppmlist)
    # number of elements in the 3d array
    neleming = nimg.size
    # number of elements in the 2d array
    nelem = brain_mask.size

    max_ppm = max(ppmlist)

    if ppmlist[0] > ppmlist[1]:
        ppm_list_b0 = np.linspace(max_ppm, 0.0, nppm)

    else:
        ppm_list_b0 = np.linspace(0, max_ppm, nppm)

    [r, z, x, y] = pimg.shape
    mask = np.zeros((z, x, y))

    for i in range(z):
        im = nimg[nppm - 1, i]
        max_val = np.max(im)
        m1 = mask[i]
        m1[im > 0.1 * max_val] = 1
        mask[i] = m1

    # prepare all the arguments from calc_b0_map
    # 2d & 3d arrays need to be transposed
    pimg = np.ascontiguousarray(np.swapaxes(pimg, 2, 3))
    nimg = np.ascontiguousarray(np.swapaxes(nimg, 2, 3))
    mask = mask.astype(int)
    mask = np.ascontiguousarray(np.swapaxes(mask, 1, 2))

    # calculate b0 map and transpose it back
    b0map = calc_b0_map(ppm_list_b0, pimg, nimg, mask, nppm, neleming, nelem)
    b0map = np.swapaxes(b0map, 1, 2)

    [z, x, y] = b0map.shape
    [zm, xm, ym] = brain_mask.shape
    im_unwrapped = brain_mask * 1

    if x == xm:
        im_unwrapped = b0map

    else:
        map2 = interpn(b0map)
        [z2, x2, y2] = map2.shape
        im_unwrapped[(zm - z2): zm, (xm - x2):xm, (ym-y2):ym] = map2

    b0map = ad.anisodiff_3d(im_unwrapped, 10, 50, 0.03, 1) * brain_mask

    return b0map


def calc_2d_b0_map(ppmlist, pimg, nimg, brain_mask, step=0.0050):
    # load c function calc_b0_map and define return type and argument types
    b0b1_lib = os.path.realpath(__file__)
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'scripts' folder
    b0b1_lib = os.path.dirname(b0b1_lib)  # 'library' folder
    b0b1_lib = os.path.join(b0b1_lib, 'library', 'calc_b0_map.so')
    lib = cdll.LoadLibrary(b0b1_lib)

    calc_b0_map = lib.calc_b0_map
    calc_b0_map.restype = ndpointer(dtype=c_double, shape=(
        brain_mask.shape[1], brain_mask.shape[0]))
    calc_b0_map.argtypes = [ndpointer(dtype=c_double, ndim=1, flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_double, ndim=3,
                                      flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_double, ndim=3,
                                      flags='C_CONTIGUOUS'),
                            ndpointer(dtype=c_longlong, ndim=2,
                                      flags='C_CONTIGUOUS'),
                            c_float, c_int, c_int, c_int]

    # prepare all the arguments from calc_b0_map
    # 2d & 3d arrays need to be transposed
    pimg = np.ascontiguousarray(np.swapaxes(pimg, 1, 2))
    nimg = np.ascontiguousarray(np.swapaxes(nimg, 1, 2))
    brain_mask = np.ascontiguousarray(np.swapaxes(brain_mask, 0, 1))

    # number of elements in ppmlist
    nppm = len(ppmlist)
    # number of elements in the 3d array
    neleming = np.prod([x for x in nimg.shape])
    # number of elements in the 2d array
    nelem = np.prod([x for x in brain_mask.shape])

    # calculate b0 map and transpose it back
    b0map = calc_b0_map(ppmlist, pimg, nimg, brain_mask,
                        step, nppm, neleming, nelem)
    b0map = np.transpose(b0map)

    # b0 thresholding
    b0thr = 1.3
    b0map[b0map > b0thr] = b0thr
    b0map[b0map < -b0thr] = -b0thr

    return b0map


def calc_b0_map(ppmlist, pimg, nimg, mask, dim, step=0.0050):

    if dim == 2:
        b0map = calc_2d_b0_map(ppmlist, pimg, nimg, mask, step=0.0050)

    else:
        b0map = calc_3d_b0_map(ppmlist, pimg, nimg, mask, step=0.0050)

    return b0map


def calc_2d_b1_map(img1, img2, img3, brain_mask, alpha):

    [img1_x, img1_y] = np.shape(img1)
    mask1 = np.zeros([img1_x, img1_y])

    im = img1
    maxval = np.max(im)
    m1 = im * 0.0
    m1[im > 0.01 * maxval] = 1.0
    mask1 = m1

    img1 = wiener(img1, (5, 5))
    img2 = wiener(img2, (5, 5))
    img3 = wiener(img3, (5, 5))

    r = np.divide(img2, 1.0 + img1)
    r[img2 > img1] = -r[img2 > img1]
    x = 0.25 * (r + np.sqrt(np.multiply(r, r) + 8.0))
    r1 = np.arccos(x) / alpha
    r = np.divide(img3, (1.0 + img2))
    r[img3 > img2] = -r[img3 > img2]
    x = 0.25 * (r + np.sqrt(np.multiply(r, r) + 8.0))
    r2 = np.arccos(x) / (2 * alpha)
    r2[mask1 == 0] = 0.0

    [mask_x, _] = np.shape(brain_mask)
    if (mask_x > img1_x):
        b1_map = brain_mask
        r3 = interp2d(r1)
        [h1, w1] = np.shape(r3)
        b1_map[:h1, :w1] = r3
    else:
        b1_map = r1

    b1_map = np.multiply(b1_map, brain_mask)

    return b1_map


# calc_B1map3d.m
def calc_3d_b1_map(img1, img2, brain_mask, alpha):

    r = img2 / (1.0 + img1)
    r[img2 > img1] = -r[img2 > img1]
    x = 0.25 * (r + np.sqrt(r * r + 8.0))
    b1_map1 = np.arccos(x) / alpha

    [z, x, y] = b1_map1.shape
    [zm, xm, ym] = brain_mask.shape
    if xm > x:
        b1_map = 1.0 + (brain_mask * 0.0)
        b1_map[1:zm, 1:xm, 1:ym] = interpn(b1_map1)

    else:
        b1_map = b1_map1

    b1_map[b1_map > 1.8] = 0.0

    b1_map = b1_map * brain_mask

    return b1_map


# calc_B1map3d_new.m
def calc_3d_b1_map_new(img1, img2, img3, brain_mask, alpha):

    [d, h, w] = img1.shape
    mask1 = np.zeros(img1.shape)

    for i in range(d):
        im = img1[i]
        max_val = np.max(im)
        m1 = im * 0.0
        m1[im > (0.08 * max_val)] = 1.0
        mask1[i] = m1

    r = (img2 * mask1) / (1.0 + img1)
    x = 0.25 * (r + np.sqrt(r * r + 8.0))
    # JOELLE JEE ADDED: NEED TO ACCOUNT FOR VALUES IN X > 1
    # this returns NAN when running np.arccos()
    x[x > 1.0] = 1.0
    r1 = np.arccos(x) / alpha
    r1[mask1 == 0] = 0.0

    r = img3 / (1.0 + img2)
    r[img3 > img2] = -r[img3 > img2]
    x = 0.25 * (r + np.sqrt(r * r + 8.0))
    # JOELLE JEE ADDED: NEED TO ACCOUNT FOR VALUES IN X > 1
    # this returns NAN when running np.arccos()
    x[x > 1.0] = 1.0
    r2 = np.arccos(x) / (2 * alpha)
    r2[mask1 == 0] = 0.0

    r1[r1 < 0.5] = r2[r1 < 0.5]
    r1[r1 > 2.0] = 2.0

    [dm, hm, wm] = brain_mask.shape

    if hm > h:
        b1_map = brain_mask
        r3 = interpn(r1)
        [d1, h1, w1] = r3.shape
        b1_map[0:d1, 0:h1, 0:w1] = r3

    else:
        b1_map = r1

    b1_map = b1_map * brain_mask

    b1_map = ad.anisodiff_3d(b1_map, 20, 50, 0.03, 1) * brain_mask

    return b1_map


def calc_b1_map(img1, img2, img3, brain_mask, alpha, dim, reps):

    if dim == 2:
        b1_map = calc_2d_b1_map(img1, img2, img3, brain_mask, alpha)

    else:

        if reps == 2:
            b1_map = calc_3d_b1_map(img1, img2, brain_mask, alpha)

        else:
            b1_map = calc_3d_b1_map_new(img1, img2, img3, brain_mask, alpha)

    return b1_map

