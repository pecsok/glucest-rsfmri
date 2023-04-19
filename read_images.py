import os
import warnings
import numpy as np
import nibabel as nib
from math import pi, ceil
import anisotropic_diffusion as ad
from calculate_T1 import calc_t1
from create_cest_masks import extract_slice, read_masks
from read_dicom_series import read_dicom_series, read_3d_dicom_series


# line 370-434
def read_2d_B1(B1_path):
    '''Read B1 image


    Parameters:

    B1_path (str): path to the B1 image


    Returns:

    B1_info (dict): dictionary that includes <B1_img1>, <B1_img2>,
                     <B1_img3>, <alpha>, <B1_hdr>

    '''

    # line 370-384 truncated
    B1_info = {}

    # There is always 1 directory of B1 dicom images to read
    # line 392-408 truncated

    [B1_hdr, B1_img, B1_raw_hdr] = read_dicom_series(B1_path)
    [nreps, nrows, ncols] = B1_img.shape
    B1_info.update({"B1_img1": B1_img[0],
                    "B1_img2": B1_img[1]})

    if nreps == 3:
        B1_info.update({"B1_img3": B1_img[2]})

    # line 417-425 because our file is moco

    B1_info.update({"alpha": pi * (B1_hdr["WIPdbl"][1] / 180.0),
                    "B1_hdr": B1_hdr})

    return(B1_info)


# function pushbutton4_Callback: line 683 - 805
def read_2d_cest(cest_path):
    '''Read cest image.


    Parameters:

    cest_path (str): path to the CEST image


    Returns:

    cest_info (dict): dictionary that includes <CEST_path>, <CEST_ppm_list>,
                     <nCEST_ppm>, <nCEST_ppm>, <CEST_pos_images>,
                     <CEST_neg_images>, <CEST_hdr>, <CEST_pw>, <CEST_pw1>,
                     <CEST_b1>, <CEST_dc>

    '''

    # cest info dictionary to be returned
    cest_info = {}

    [cest_hdr, cest_img, dcm_hdr] = read_dicom_series(cest_path)

    nfreq = cest_hdr["reps"] // 2
    nfiles = cest_hdr["reps"]

    # handles.refpath
    cest_info.update({"CEST_path": cest_path})

    seq_name = cest_hdr["SeqName"]

    if "swversion" not in cest_hdr.keys():
        # TODO: throw error...??
        return

    swversion = cest_hdr["swversion"]

    # "swversion" is a key in cest_hdr:
    if "VD13A" in swversion:
        wip_ppm_index = 3
        prep_mode_index = 1
        cestz2_value = 5
        CEST_pw = cest_hdr["WIPlong"][10]
        CEST_pw1 = cest_hdr["WIPlong"][12]
        CEST_b1 = cest_hdr["WIPlong"][13]
        CEST_dc = cest_hdr["WIPlong"][0]

    elif "VD13D" in swversion:
        wip_ppm_index = 2
        prep_mode_index = 2
        cestz2_value = 3
        CEST_pw = 0.001 * cest_hdr["WIPlong"][12]
        CEST_pw1 = 0.001 * cest_hdr["WIPlong"][13]

        CEST_b1 = cest_hdr["WIPlong"][15]
        CEST_dc = cest_hdr["WIPlong"][0]

    # TODO: line 710 to 770 truncated because it doesn't apply to our data
    elif "prep_moco" in seq_name:
        wip_ppm_index = 2
        prep_mode_index = 2
        cestz2_value = 3

        if cest_hdr["WIPlong"][18] >= 170:
            CEST_pw = cest_hdr["WIPlong"][9]
            CEST_pw1 = cest_hdr["WIPlong"][12]
            CEST_b1 = cest_hdr["WIPlong"][10]
            CEST_dc = cest_hdr["WIPlong"][0]

    # line 722
    if "VE11U" or "VE12U" in swversion:
        wip_ppm_index = 2
        if "tlf" in seq_name:
            cestz2_value = 4
        else:
            cestz2_value = 3
        CEST_pw = cest_hdr["WIPlong"][12]
        CEST_pw1 = cest_hdr["WIPlong"][13]
        CEST_b1 = cest_hdr["WIPlong"][15]
        CEST_dc = cest_hdr["WIPdbl"][0]

    # line 770 we always have just 1 CEST image
    hdr = [None] * nfiles
    hdd = [None] * nfiles
    hdd[0] = cest_hdr

    CEST_ppm_list = np.zeros(ceil((range(1, nfiles + 1, 2)[-1] + 1) / 2))
    [z, x, y] = cest_img.shape
    pos_img = np.zeros((ceil(z / 2), x, y))
    neg_img = np.zeros((ceil(z / 2), x, y))

    for i in range(1, nfiles + 1, 2):
        j = int((i + 1)/2) - 1
        i = i - 1

        hdr[i] = hdd[0]
        hdr[i + 1] = hdd[0]
        pos_img[j] = cest_img[i]
        neg_img[j] = cest_img[i + 1]

        if hdr[i]["WIPlong"][prep_mode_index - 1] == cestz2_value:
            ppm_begin = hdr[i]["WIPdbl"][wip_ppm_index]
            ppm_end = hdr[i]["WIPdbl"][wip_ppm_index + 1]
            ppm_step = hdr[i]["WIPdbl"][wip_ppm_index + 2]

            if ppm_begin > ppm_end:
                ppm_step = -ppm_step

            CEST_ppm_list[j] = ppm_begin + j * ppm_step
        else:
            CEST_ppm_list[j] = hdr[i]["WIPdbl"][wip_ppm_index - 1]

    cest_info.update({"CEST_ppm_list": CEST_ppm_list})
#     There's only 1 nfreq
    cest_info.update({"nCEST_ppm": nfreq})
    cest_info.update({"CEST_pos_images": pos_img})
    cest_info.update({"CEST_neg_images": neg_img})
    cest_info.update({"CEST_hdr": hdr})
    cest_info.update({"CEST_pw": CEST_pw})
    cest_info.update({"CEST_pw1": CEST_pw1})
    cest_info.update({"CEST_b1": CEST_b1})
    cest_info.update({"CEST_dc": CEST_dc})

    # line 807-861 truncated because our data is always NSELIR
    return cest_info


# line 206-360
def read_2d_wassr(wassr_path):
    '''Read wassr image


    Parameters:

    wassr_path (str): path to the wassr image


    Returns:

    wassr_info (dict): dictionary that includes <WASSR_pw>, <WASSR_pw1>,
                       <WASSR_b1>, <WASSR_dc>, <WASSR_ppm_list>, <nWASSR_ppm>,
                       <WASSR_pos_img>, <WASSR_neg_img>, <WASSR_hdr>

    '''

    wassr_info = {}

    wassr_info.update({"b0type": "WASSR"})

    # line 209-233 because we have siemens data and only 1 wassr dcm dir
    [wassr_hdr, wassr_img, _] = read_dicom_series(wassr_path)
    nfiles = wassr_hdr["reps"]

    # line 245-262 truncated because our wassr data has swversion "VE11U"
    wip_ppm_index = 2
    prep_mode_index = 2
    cestz2_val = 3

    wassr_info.update({"WASSR_pw": wassr_hdr["WIPlong"][12],
                       "WASSR_pw1": wassr_hdr["WIPlong"][13],
                       "WASSR_b1": wassr_hdr["WIPlong"][15],
                       "WASSR_dc": wassr_hdr["WIPdbl"][0]})

    # line 275-318 truncated
    hd_index = 0
    ppm_index = 0

    hdr = [None] * (nfiles + hd_index)
    pos_img = [None] * (nfiles // 2 + ppm_index)
    neg_img = [None] * (nfiles // 2 + ppm_index)
    WASSR_ppm_list = [None] * ceil(nfiles / 2)

    for i in range(1, nfiles + 1, 2):
        j = (i + 1)//2
        hdr[i - 1] = wassr_hdr
        hdr[i] = wassr_hdr
        pos_img[j - 1] = wassr_img[i - 1]
        neg_img[j - 1] = wassr_img[i]

        if hdr[i + hd_index - 1]["WIPlong"][prep_mode_index - 1] == cestz2_val:
            ppm_begin = hdr[i + hd_index - 1]["WIPdbl"][wip_ppm_index]
            ppm_end = hdr[i + hd_index - 1]["WIPdbl"][wip_ppm_index + 1]
            ppm_step = hdr[i + hd_index - 1]["WIPdbl"][wip_ppm_index + 2]

            if ppm_begin > ppm_end:
                ppm_step = -ppm_step

            WASSR_ppm_list[j + ppm_index - 1] = ppm_begin + (j - 1) * ppm_step

        else:
            WASSR_ppm_list[j+ppm_index-1] = hdr[i +
                                                hd_index-1]["WIPdbl"][wip_ppm_index]

    wassr_info.update({"WASSR_ppm_list": np.array(WASSR_ppm_list),
                       "nWASSR_ppm": len(WASSR_ppm_list),
                       "WASSR_pos_img": np.array(pos_img),
                       "WASSR_neg_img": np.array(neg_img),
                       "WASSR_hdr": hdr})

    return(wassr_info)


# helper function for load_images and load_3d_images to check that the
# dimensions of the images are matching.
def check_size(shape_list):

    mask_dim = len(shape_list[-1])

    for s in range(0, len(shape_list)):

        if len(shape_list[s]) > mask_dim:
            shape_list[s] = shape_list[s][len(shape_list[s]) - mask_dim:]

    shape_list = np.array(shape_list)
    print(shape_list)
    shape_list = np.unique(shape_list, axis=0)
    if shape_list.size == mask_dim:
        return True
    else:
        return False


# pushbutton6_Callback line
def read_3d_cest(cest_path):
    '''Read 3D cest image.


    Parameters:

    cest_path (str): path to the CEST image


    Returns:

    cest_info (dict): dictionary that includes <CEST_path>, <CEST_ppm_list>,
                     <nCEST_ppm>, <nCEST_ppm>, <CEST_pos_images>,
                     <CEST_neg_images>, <CEST_hdr>, <CEST_pw>, <CEST_pw1>,
                     <CEST_b1>, <CEST_dc>

    '''

    [cest_hdr, cest_img, dcm_hdr] = read_3d_dicom_series(cest_path)

    seq_name = cest_hdr["SeqName"]
    nfreq = cest_hdr["reps"] / 2
    wip_ppm_index = 2

    if "tfl" in seq_name:
        cestz2_mode = 4
    else:
        cestz2_mode = 3

    if cest_hdr["WIPlong"][1] == cestz2_mode:
        ppm_begin = cest_hdr["WIPdbl"][wip_ppm_index]
        ppm_end = cest_hdr["WIPdbl"][wip_ppm_index + 1]
        ppm_step = cest_hdr["WIPdbl"][wip_ppm_index + 2]

        if ppm_begin > ppm_end:
            ppm_step = - ppm_step

    cest_ppm_list = []
    curr_ppm = round(ppm_begin, 4)
    while curr_ppm <= ppm_end:
        cest_ppm_list.append(curr_ppm)
        curr_ppm += ppm_step
        curr_ppm = round(curr_ppm, 4)

    nfreq = cest_hdr["reps"] // 2
    [_, z, x, y] = cest_img.shape
    pos_img = np.zeros((nfreq, z, x, y))
    neg_img = np.zeros((nfreq, z, x, y))

    for i in range(0, cest_hdr["reps"], 2):
        j = i // 2
        for isl in range(0, z):
            pos_img[j, isl] = cest_img[i, isl]
            neg_img[j, isl] = cest_img[i + 1, isl]

    cest_ppm = 3
    # cest info dictionary to be returned
    cest_info = {}
    cest_info.update({"CEST_ppm_list": cest_ppm_list})
    cest_info.update({"CEST_path": cest_path})
#     There's only 1 nfreq
    cest_info.update({"nCEST_ppm": nfreq})
    cest_info.update({"CEST_pos_images": pos_img})
    cest_info.update({"CEST_neg_images": neg_img})
    cest_info.update({"CEST_hdr": cest_hdr})
    cest_info.update({"CEST_pw": cest_hdr["WIPlong"][10]})
    cest_info.update({"CEST_pw1": cest_hdr["WIPlong"][11]})
    cest_info.update({"CEST_b1": cest_hdr["WIPlong"][13]})
    cest_info.update({"CEST_dc": cest_hdr["WIPdbl"][0]})
    cest_info.update({"CEST_ppm": cest_ppm})

    # line 807-861 truncated because our data is always NSELIR
    return cest_info


def read_mp2rageT1(mp2rageT1_path):
    '''Read 3D mp2rage T1 image


    Parameters:

    mp2rageT1_path (str): path to the mp2rage T1 image


    Returns:

    t1_map (ndarray): T1 image


    '''

    [_, mp2rageT1_img, _] = read_3d_dicom_series(mp2rageT1_path)

    return np.squeeze(mp2rageT1_img)


# pushbutton3_Callback in CEST3DNEW.m
def read_3d_wassr(wassr_path):
    '''Read 3D wassr image


    Parameters:

    wassr_path (str): path to the wassr image


    Returns:

    wassr_info (dict): dictionary that includes <WASSR_pw>, <WASSR_pw1>,
                       <WASSR_b1>, <WASSR_dc>, <WASSR_ppm_list>, <nWASSR_ppm>,
                       <WASSR_pos_img>, <WASSR_neg_img>, <WASSR_hdr>

    '''

    wassr_info = {}

    wassr_info.update({"b0type": "WASSR"})

    # line 517- for Siemens
    [wassr_hdr, wassr_img, hdr] = read_3d_dicom_series(wassr_path)
    [r, d, h, w] = wassr_img.shape
    r = r // 2
    wassr_ppm_list = np.zeros(r)
    pos_img = np.zeros((r, d, h, w))
    neg_img = np.zeros((r, d, h, w))

    nfreq = wassr_hdr["reps"]/2

    # line 535
    wip_ppm_index = 2
    if 'tfl' in wassr_hdr["SeqName"]:
        cestz2_mode = 4
    else:
        cestz2_mode = 3

    if wassr_hdr["WIPlong"][1] == cestz2_mode:
        ppm_begin = 0
        ppm_end = wassr_hdr["WIPdbl"][wip_ppm_index + 1]
        ppm_step = wassr_hdr["WIPdbl"][wip_ppm_index + 2]

        if ppm_begin > ppm_end:
            ppm_step = - ppm_step

        for i1 in range(0, r):
            wassr_ppm_list[i1] = ppm_begin + ppm_begin + i1 * ppm_step

    im1 = wassr_img[wassr_hdr["reps"] - 1]
    im1 = 2000.0 * im1 / im1.max()
    noise = im1[im1 < 140]
    noisestd = np.std(noise)
    threshold = 5 * noisestd
    mask = im1 * 0.0
    mask[im1 > threshold] = 1.0
    im1 = ad.anisodiff_3d(im1, 50, 800000, 0.25, 1)
    bias = im1 * 0.0
    im1_max_val = np.max(im1)
    im = im1_max_val / (im1 + 0.01)
    im[mask == 0] = 1.0
    im[im < 0] = 1.0
    im1 = (im1 * mask) * im
    im[im1 > 2000] = im[im1 > 2000] * (2000 / (im1[im1 > 2000]))
    bias = im

    for i in range(0, wassr_hdr["reps"], 2):
        j = i // 2
        for isl in range(0, wassr_hdr["nz"]):
            pos_img[j, isl] = wassr_img[i, isl]
            neg_img[j, isl] = wassr_img[i + 1, isl]

    wassr_ppm = (ppm_begin + ppm_end) / 2.0

    wassr_info.update({"WASSR_pw": wassr_hdr["WIPlong"][10],
                       "WASSR_pw1": wassr_hdr["WIPlong"][11],
                       "WASSR_b1": wassr_hdr["WIPlong"][13],
                       "WASSR_dc": wassr_hdr["WIPdbl"][0],
                       "WASSR_ppm_list": wassr_ppm_list,
                       "WASSR_ppm": wassr_ppm,
                       "nWASSR_ppm": nfreq,
                       "WASSR_pos_img": pos_img,
                       "WASSR_neg_img": neg_img,
                       "WASSR_hdr": hdr,
                       "WASSR_path": wassr_path,
                       "B0_bias": bias})

    return(wassr_info)


# pushbutton5_Callback in CEST3DNEW.m
def read_3d_B1(B1_path):
    '''Read 3D B1 image


    Parameters:

    B1_path (str): path to the B1 image


    Returns:

    B1_info (dict): dictionary that includes <B1_img1>, <B1_img2>,
                     <B1_img3>, <alpha>, <B1_hdr>

    '''
    # line 370-384 truncated
    B1_info = {}

    # There is always 1 directory of B1 dicom images to read
    # line 392-408 truncated

    [B1_hdr, B1_img, B1_raw_hdr] = read_3d_dicom_series(B1_path)
    [nreps, ndepth, nrows, ncols] = B1_img.shape
    B1_info.update({"B1_img1": B1_img[0],
                    "B1_img2": B1_img[1],
                    "B1_img3": B1_img[2]})

    B1_info.update({"alpha": pi * (B1_hdr["WIPdbl"][1] / 180.0),
                    "B1_hdr": B1_hdr})

    return(B1_info)


def read_cest(cest_path, dim):

    if dim == 2:
        cest_info = read_2d_cest(cest_path)
    else:
        cest_info = read_3d_cest(cest_path)

    return cest_info


def read_wassr(wassr_path, dim):

    if dim == 2:
        wassr_info = read_2d_wassr(wassr_path)
    else:
        wassr_info = read_3d_wassr(wassr_path)

    return wassr_info


# read b1 maps (dicom) 2d: line 370-434, 3d: pushbutton5_Callback in CEST3DNEW.m
def read_B1(B1_path, dim):

    # line 370-384 truncated
    B1_info = {}

    # There is always 1 directory of B1 dicom images to read
    # line 392-408 truncated
    if dim == 2:
        [B1_hdr, B1_img, _] = read_dicom_series(B1_path)
        nreps = B1_img.shape[0]
        if nreps == 3:
            B1_info.update({"B1_img3": B1_img[2]})
        # line 417-425 because our file is moco (for setting alpha and B1_hdr)

    # pushbutton5_Callback in CEST3DNEW.m
    else:
        [B1_hdr, B1_img, _] = read_3d_dicom_series(B1_path)
        B1_info.update({"B1_img3": B1_img[2]})

    B1_info.update({"B1_img1": B1_img[0],
                    "B1_img2": B1_img[1]})
    B1_info.update({"alpha": pi * (B1_hdr["WIPdbl"][1] / 180.0),
                    "B1_hdr": B1_hdr})

    return B1_info


def calc_t1_from_uni(uni_nii, uni_dicom, none_nii, sub_out, mode):

    # get the first .dcm file in UNI DICOM
    for dcm in os.listidr(uni_dicom):
        if dcm.endswith('.dcm'):
            uni_dicom = os.path.join(uni_dicom, dcm)
            break

    # calculate t1_map
    sub = os.basename(sub_out)
    t1_nii = calc_t1(uni_nii, uni_dicom,
                     os.path.join(sub_out, sub + '-' + 'T1fromUNI.nii'))
    # get the corresponding 3d slab of the t1_map
    # TODO: check if the mask_exists and cest.nii exists and also add back the
    # reading of the GUI mask if mask_exists == FALSE
    t1_img = extract_slice(t1_nii, 't1', none_nii, mode, sub_out)

    return t1_img


def load_all_images(sub_data, sub_masks, mask_type, mode, sub_out, fdict, dim):

    # set <file_type>_path = None to later check if
    # this subject has all necessary files
    img_paths = {"cest_dcm": [],
                 "t1_dcm": [],
                 "wassr_dcm": [],
                 "b1_dcm": [],
                 "none_nii": [],
                 "mask": [],
                 "seg": []}

    # parse each file type to be read later
    sub_files = [os.path.join(sub_data, x) for x in os.listdir(sub_data)]
    for img in os.listdir(sub_data):
        img_path = os.path.join(sub_data, img)
        img = img.lower()
        # cest image
        if fdict["cest_dcm"] in img:
            img_paths["cest_dcm"].append(img_path)
            sub_files.remove(img_path)
        # wassr image
        elif fdict["wassr_dcm"] in img:
            img_paths["wassr_dcm"].append(img_path)
            sub_files.remove(img_path)
        # b0 image
        elif fdict["b1_dcm"] in img:
            img_paths["b1_dcm"].append(img_path)
            sub_files.remove(img_path)
        # b0 image
        elif fdict["none_nifti"] in img:
            img_paths["none_nii"].append(img_path)
            sub_files.remove(img_path)
        # read mp2rage T1 image for 3d image
        elif dim == 3 and fdict["t1_dcm"] in img:
            img_paths["t1_dcm"].append(img_path)
            sub_files.remove(img_path)

    # if cest is 3d and if T1 dicom doesn't exit, calculate t1 using UNI
    if dim == 3 and len(img_paths["t1_dcm"]) == 0:
        # find UNI nifti image
        [uni_nii] = [x for x in sub_files if 'UNI.nii' in x]
        img_paths["t1_dcm"] = uni_nii
        # find UNI DICOM
        [uni_dicom] = [x for x in sub_files if (x.endswith('UNI_Images') and
                       '2D' not in x)]
        img_paths.update({"uni_dcm": uni_dicom})

    # if cest is 2d, remove the "t1_dcm" key from img_paths as it is unnecessary
    elif dim == 2:
        img_paths.pop("t1_dcm")

    # get brain mask and segmenation map
    [img_paths["mask"], img_paths["seg"]] = read_masks(sub_masks,
                                                       mask_type, mode,
                                                       img_paths["none_nii"])
    # check if subject has all the necessary raw data
    for key, value in img_paths.items():
        if len(value) != 0 and type(value[0]) is str:
            value.sort(reverse=True)
            # all values in img_paths should now be strings instead of lists
            img_paths[key] = value[0]

        elif len(value) == 0:
            warnings.warn("Subject " + os.path.basename(sub_data) +
                          " is missing necessary file: " + key + ".",
                          UserWarning)
            return

    # subject has all the necessary files so now read them all
    cest_info = read_cest(img_paths["cest_dcm"], dim)
    wassr_info = read_wassr(img_paths["wassr_dcm"], dim)
    b1_info = read_B1(img_paths["b1_dcm"], dim)

    # if cest is 3d, read the t1 map
    if dim == 3:
        if img_paths["t1_dcm"].endswith('UNI.nii'):
            # TODO: t1_map is not being written
            t1_map = calc_t1_from_uni(img_paths["t1_dcm"],
                                      img_paths["uni_dcm"],
                                      img_paths["none_nii"],
                                      sub_out, mode)
        else:
            t1_map = read_mp2rageT1(img_paths["t1_dcm"])

    # check that the dimension of every image is the same
    if dim == 2:
        dim_pass = check_size([cest_info["CEST_pos_images"].shape,
                               wassr_info["WASSR_pos_img"].shape,
                               b1_info["B1_img1"].shape,
                               img_paths["mask"].shape,
                               img_paths["seg"].shape])
    else:
        dim_pass = check_size([cest_info["CEST_pos_images"].shape,
                               wassr_info["WASSR_pos_img"].shape,
                               b1_info["B1_img1"].shape,
                               t1_map.shape,
                               img_paths["mask"].shape,
                               img_paths["seg"].shape])

    # if dimensions don't match, print warning and return
    if not dim_pass:
        warnings.warn("Subject " + sub_data +
                      " images do not have the same dimensions")
        return

    # get the affine matrix from the cest nifti. This is necessary for writing
    # out the final results in the correct space.
    none_nii = nib.load(img_paths["none_nii"])
    none_affine = none_nii.affine
    none_dtype = none_nii.get_data_dtype()
    affine_dtype = [none_affine, none_dtype]

    # don't return seg_map if cest is 3d
    if dim == 3:
        img_paths["seg"] = 0
    # set t1_map to None if cest is 2d
    else:
        t1_map = 0

    return [cest_info, t1_map, wassr_info, b1_info,
            img_paths["mask"], img_paths["seg"], affine_dtype]
