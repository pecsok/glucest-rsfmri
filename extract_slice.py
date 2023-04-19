import os
import nibabel as nib
import numpy as np


def extract_slice(map_path, mask, cest_path, mode, sub_out):
    # run extract_slice2 to get the right 2D slab from 3D mask
    sub = os.path.basename(sub_out)  # find sub label

    # set output path/name for the resulting 2d mask
    sub_2d_map = os.path.join(sub_out, sub + '_' + mask + '_2d.nii')

    extract_script = os.path.realpath(__file__)
    extract_script = os.path.dirname(extract_script)
    extract_script = os.path.join(extract_script, 'extract_slice2.sh')
    mask_cmd = ['bash', extract_script, '-MultiLabel', map_path,
                cest_path, sub_2d_map]

    os.system(' '.join(mask_cmd))

    # gzip if .nii.gz
    if mask.endswith('.nii.gz'):
        os.system('gzip ' + map_path.split('.gz')[0])

    # reorient the images
    sub_2d_map = nib.load(sub_2d_map)
    sub_2d_map = sub_2d_map.get_data()
    sub_2d_map = np.array(sub_2d_map)

    if mode != 'syrp':
        sub_2d_map = np.swapaxes(sub_2d_map, 0, 2)

        if mode == 'hippocampus':
            sub_2d_map = np.swapaxes(sub_2d_map, 1, 2)

    # return 2d version of mask if dim3 == 1
    if sub_2d_map.shape[0] == 1:
        sub_2d_map = sub_2d_map[0]

    # need to orient the image correctly depending on the type/mode
    if mode == '3d':
        sub_2d_map = np.flip(sub_2d_map, axis=1)

    if mode == 'syrp':
        sub_2d_map = np.rot90(sub_2d_map, k=2)
        sub_2d_map = sub_2d_map.transpose()

    if mode == 'hippocampus':
        sub_2d_map = np.fliplr(sub_2d_map)
        sub_2d_map = sub_2d_map.transpose()

    sub_2d_map = sub_2d_map.astype('int64')
    return (sub_2d_map)
