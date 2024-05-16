#!/bin/sh

case=$1
case_data=$2
case_out=$3
struc_img=$4

# make output directories for fast and first segmentation
if [ ! -d $case_out/fast ]; then
  mkdir $case_out/fast
fi

if [ ! -d $case_out/first ]; then
  mkdir $case_out/first
fi

if [ ! -d $case_out/log ]; then
  mkdir $case_out/log
fi

# convert and bias correct UNI
if [ ! -e $case_out/${struc_img}_corrected.nii.gz ]; then
  N4BiasFieldCorrection -d 3 -i $case_data/${struc_img}.nii* \
    -o $case_out/${struc_img}_corrected.nii.gz
fi

# apply the mask to corrected UNI
fslmaths $case_out/${struc_img}_corrected.nii.gz \
  -mas $case_out/$case*_mask.nii.gz \
  $case_out/${struc_img}_masked.nii.gz

# run first
if [ ! -e $case_out/first/${struc_img}_all_fast_firstseg.nii.gz ]; then
  run_first_all -b \
    -i $case_out/${struc_img}_masked.nii.gz \
    -o $case_out/first/${struc_img}
fi

# run fast
if [ ! -e $case_out/fast/${struc_img}-fast_3_seg.nii.gz ]; then
  fast -n 3 \
    -o $case_out/fast/${struc_img}-fast_3 \
    $case_out/${struc_img}_masked.nii.gz
fi

# combine fast and first on UNI
if [ ! -e $case_out/${struc_img}-fast_3_first_seg.nii.gz ]; then
  # binarize FIRST output to mask
  fslmaths $case_out/first/${struc_img}_all_fast_firstseg.nii.gz \
    -bin $case_out/log/${struc_img}_all_fast_firstseg_gm.nii.gz

  # remove FIRST mask from FAST 3 seg image by creating an inverse map
  # (*neg.nii.gz - GM=0, else=1) then multiplying
  fslmaths $case_out/log/${struc_img}_all_fast_firstseg_gm.nii.gz \
    -mul -1 \
    -add 1 $case_out/log/${struc_img}_all_fast_firstseg_gm_neg.nii.gz

  fslmaths $case_out/log/${struc_img}_all_fast_firstseg_gm_neg.nii.gz \
    -mul $case_out/fast/${struc_img}-fast_3_seg.nii.gz \
    $case_out/log/${struc_img}-fast_3_seg_neg.nii.gz

  # add FIRST mask back in as GM=2 to match with FAST 3 seg (CSF=1, GM=2, WM=3)
  fslmaths $case_out/log/${struc_img}_all_fast_firstseg_gm.nii.gz \
    -mul 2 \
    -add $case_out/log/${struc_img}-fast_3_seg_neg.nii.gz \
    $case_out/${struc_img}-fast_3_first_seg.nii.gz
fi
