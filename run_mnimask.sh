#!/bin/sh

# path to MNI152 1mm brain mask
mni=$1
mni_mask=$2
case_data=$3
cest=$4
case_out=$5
case=$6

antsExe=`which antsRegistration`

if [[ ! -f "$antsExe" ]]; then
    echo "This script requires ANTs executables (check PATH)"
    exit 1
fi


# make output folders in the subject's outupt folder
mkdir $case_out/structural_to_mni
mkdir $case_out/cest_to_structural

#  bias correct INV2
if [ ! -e $case_out/$case-INV2_corrected.nii.gz ]; then
  N4BiasFieldCorrection -d 3 -i $case_data/$case-INV2.nii* \
    -o $case_out/$case-INV2_corrected.nii.gz
fi

# register the subject's 3d structural to MNI152 1mm
antsRegisterSyN.sh \
  -d 3 \
  -m $case_out/$case-INV2_corrected.nii.gz \
  -f $mni \
  -t s \
  -o $case_out/structural_to_mni/$case-INV2inMNI-

############################### PHIL COOK BEGIN ################################
# register the subject's 3d CEST to structural
sysTmpDir=/tmp

if [[ -d "$TMPDIR" ]]; then
    sysTmpDir=$TMPDIR
fi

tmpDir=`mktemp -d -p $sysTmpDir cestToT1.XXXXXXXX`

if [[ ! -d "$tmpDir" ]]; then
    echo "Could not create tmp dir $tmpDir"
    exit 1
fi

# Make a mask based on cest image, assuming cest is 0 in the background
movingMask="${tmpDir}/cestRegMask.nii.gz"
ThresholdImage 3 $cest $movingMask 0.00001 Inf 1 0

# Dilate to capture registration metric close to edges
ImageMath 3 $movingMask MD $movingMask 5

antsRegistration \
  -d 3 \
  -v 1 \
  -t Rigid[ 0.1 ] \
  -m Mattes[ $case_data, $cest, 1, 32, Regular ] \
  -f 2x1 -s 1x0vox -c [ 10x10, 1e-8, 5 ] \
  -x [ none, $movingMask ] \
  -o ${out}/cest_to_structural/$case-CESTinstructural-

rm -f ${tmpDir}/*
rmdir $tmpDir

############################### PHIL COOK END ##################################

# bring the MNI152 1mm brain mask to structural space
antsApplyTransforms \
  -d 3 \
  -e 0 \
  -i $mni_mask \
  -r $case_out/$case-INV2_corrected.nii.gz \
  -o $case_out/${sub}_MNIinINV2_mask.nii.gz \
  -t $case_out/structural_to_mni/$case-INV2inMNI-1InverseWarp.nii.gz \
  -t [$case_out/structural_to_mni/$case-INV2inMNI-0GenericAffine.mat,1]

# bring the MNI152 1mm brain mask to cest space
antsApplyTransforms \
  -d 3 \
  -e 0 \
  -i $case_out/${sub}_MNIinINV2_mask.nii.gz \
  -r $cest \
  -o $case_out/${sub}_MNIinCEST_cestmask.nii.gz \
  -t $case_out/structural_to_mni/$case-CESTinstructural-1InverseWarp.nii.gz \
  -t [$case_out/structural_to_mni/$case-CESTinstructural-0GenericAffine.mat,1]
