import os
import scipy.io
import subprocess
import numpy as np
import nibabel as nib


# helper function that reads and correctly orrients the CEST corresponding maps
def read_niftis(img_path, mode):
    nifti = nib.load(img_path)
    nifti = nifti.get_data()
    nifti = np.array(nifti)

    if mode != 'syrp':
        nifti = np.swapaxes(nifti, 0, 2)

        if mode == 'hippocampus':
            nifti = np.swapaxes(nifti, 1, 2)

    # return 2d version of mask if dim3 == 1
    if nifti.shape[0] == 1:
        nifti = nifti[0]

    # need to orient the image correctly depending on the type/mode
    if mode == '3d':
        nifti = np.flip(nifti, axis=1)

    if mode == 'syrp':
        nifti = np.rot90(nifti, k=2)
        nifti = nifti.transpose()

    if mode == 'hippocampus':
        nifti = np.fliplr(nifti)
        nifti = nifti.transpose()

    nifti = nifti.astype('int64')
    nifti = np.squeeze(nifti)

    return nifti


# creates 2d/3d CEST corresponding masks and seg maps
def extract_slice(map_path, mask, none_path, mode, sub_out):
    # run extract_slice2 to get the right 2D slab from 3D mask
    sub = os.path.basename(sub_out)  # find sub label

    # set output path/name for the resulting 2d mask
    sub_2d_map = os.path.join(sub_out, sub + '_cest' + mask + '.nii')

    extract_script = os.path.realpath(__file__)
    extract_script = os.path.dirname(extract_script)
    extract_script = os.path.join(extract_script, 'extract_slice2.sh')
    mask_cmd = ['bash', extract_script, '-MultiLabel', map_path,
                none_path, sub_2d_map]

    os.system(' '.join(mask_cmd))

    # read in the 2d ouput
    nifti = read_niftis(sub_2d_map, mode)

    return nifti


# helper function for load_all_images. It reads mask and seg maps
def read_masks(sub_masks, mask_type, mode, none_nifti=None):

    mask = None
    seg = None

    # read brain mask and seg mask if they exist
    sub_files = [os.path.join(sub_masks, x) for x in os.listdir(sub_masks)]

    # if mask doesn't exist and we have to rely on MATLAB object
    if mask_type == 'mat':
        mat_file = [x for x in sub_files if '-GluCEST_GUI.mat' in x]

        # if proper files weren't found or there were more than one:
        if len(mat_file) != 1:
            return [None, None]

        mat_file = mat_file[0]

        # read in the brain mask
        mat_file = scipy.io.loadmat(mat_file)
        mask = mat_file["output"]["roimask"][0][0]
        # mask = mask.tolist()
        mask = np.array(mask, dtype='int64')

        if mode == '3d':
            mask = np.swapaxes(mask, 0, 2)
            mask = np.swapaxes(mask, 1, 2)

        # read in the segmentation mask
        seg = mat_file['output']['segmask'][0][0]
        seg = np.array(seg, dtype='int64')

    else:
        if len(none_nifti) == 0 or len(none_nifti) > 1:
            return [mask, seg]
        mask_nifti = [x for x in sub_files if '_mask.nii' in x]
        seg_nifti = [x for x in sub_files if '_seg.nii' in x]

        # if proper files weren't found or there were more than one:
        if len(mask_nifti) != 1 or len(seg_nifti) != 1:
            return [None, None]

        # read in the maps
        mask_nifti = mask_nifti[0]
        seg_nifti = seg_nifti[0]
        none_nifti = none_nifti[0]
        mask = extract_slice(mask_nifti, 'mask', none_nifti, mode, sub_masks)
        seg = extract_slice(seg_nifti, 'seg', none_nifti, mode, sub_masks)

    return [mask, seg]


# creates or reads brain mask and segmentation map
def create_masks(sub_data, sub_masks, sub_out, mask_type, seg_type):

    # get path to script that runs brain extraction and segmentation
    script_dir = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_dir)

    if mask_type == 'exist' and seg_type == 'exist':
        # TODO: create 2d slice???
        # TODO: make sure there is only 1 mask and 1 seg
        return

    # find the INV2 nifti images to run hdbet
    elif mask_type in ['hdbet', 'mni']:
        inv2 = [f for f in os.listdir(sub_data) if 'INV2.nii' in f]
        if len(inv2) == 0:
            inv2 = [f for f in os.listdir(sub_data) if 'mprage.nii' in f]


        # raise error if the INV2 was not found or multiple were found
        if len(inv2) != 1:
            raise RuntimeError("Need 1 INV2 or MPRAGE nifti image.")

        inv2 = inv2[0]
        inv2 = inv2.split('.nii')[0]

        if mask_type == 'hdbet':

            # get path to hdbet image
            ex_script = 'run_hdbet.sh'
            hdbet_img = os.path.dirname(script_dir)
            hdbet_img = os.path.join(hdbet_img, 'images', 'hd-bet_latest.sif')

            # make command list to run hdbet
            cmd = [os.path.join(script_dir, ex_script),
                   os.path.basename(sub_data), sub_data, sub_out,
                   hdbet_img, inv2]

        else:
            ex_script = 'run_mnimask.sh'
            # TODO:
            cmd = []

        # catch error if run_hdbet.sh or run_mnimask.sh fails
        try:
            subprocess.run(cmd, check=True)
            print("Checking it finishes first\n")
        except subprocess.CalledProcessError:
            print('Failed to run ' + ex_script + '\n')
    
    print("Segmentation starting on create_cest_masks.py line 168\n")
    if seg_type == 'create':
        uni = [f for f in os.listdir(sub_data) if 'UNI.nii' in f]
        if len(uni) == 0:
            uni = [f for f in os.listdir(sub_data) if 'mprage.nii' in f]

        # raise error if the UNI was not found or multiple were found
        if len(uni) != 1:
            raise RuntimeError("Need 1 UNI or MPRAGE nifti image.")

        uni = uni[0]
        uni = uni.split('.nii')[0]

        # create segmentation map
        seg_script = 'run_fast_first.sh'
        cmd = [os.path.join(script_dir, seg_script),
               os.path.basename(sub_data), sub_data, sub_out, uni]

        # catch error if run_hdbet.sh or run_fast_first.sh fails
        try:
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError:
            print('Failed to run ' + seg_script + '\n')

    return
