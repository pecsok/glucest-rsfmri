import numpy as np
import nibabel as nib


def write_image(img, img_path, affine_matrix, data_type, mode):

    # if rescale is True:
    #     if 'b0b1_cest_map' in img_path:
    #         img = img.astype(int)
    #     img = scale_image(img)
    #     img = img.astype(int)

    # reorient the arrays
    # flip anterior posterior
    
    if mode == "hippocampus":
        img = np.fliplr(img.transpose())
        img = img[..., np.newaxis]

    elif mode == "syrp":
        # img = np.rot90(img)
        img = np.rot90(img.transpose(), k=2)
        img = img[..., np.newaxis]

    elif mode == "3d":
        img = np.swapaxes(img, 0, 2)
        img = np.flip(img, axis=1)

    # save as nifti file
    img = nib.Nifti1Image(img, affine_matrix)
    img.set_data_dtype(data_type)
    img.to_filename(img_path)
