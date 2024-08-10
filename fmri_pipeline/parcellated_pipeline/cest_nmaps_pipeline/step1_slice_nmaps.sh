#!/bin/bash

## DEFINE PATHS ##
structural=$1 
pre=$2
post=$3 # Path to output 
nmaps=$4 # Path to nmaps niftis
log=$5
case=$6
reso=$7 # Resolution. Make sure to resample nmaps before running this script.
str=$8 # UNI or INV2


#######################################################################################################
## ENSURE STRUCTURAL DATA IS AVAILABLE FOR PROCESSING ##

echo "CASE: $case"
echo "Sanity check: UNI= $str"

#check for structural data
if [ -e $structural/$case/MNI_transforms/$case-${str}inMNI-Warped.nii.gz ]
then
echo "Structural Data exists for $case"
sleep 1.5
else
echo "Oh No! Structural Data is missing. Cannot process CEST! Run register_to_MNI.sh first."
return
fi


#######################################################################################################
## make directories, set variables ##

mkdir $post/$case/nmaps
mkdir $post/$case/nmaps/$str

#######################################################################################################
## REGISTER NEUROMAPS TO UNI IMAGES AND GLUCEST IMAGES ##

# Define array of nmaps
declare -a maps=(
  "mGluR5"
  "NMDA"
  "GABA"
)

# Loop through each atlas
for map in "${maps[@]}"; do
    echo $post/$case/nmaps/$str/${case}-${map}.nii.gz

    # Warp neuromap to subject space
    antsApplyTransforms -d 3 -r $structural/$case/${case}-${str}_masked.nii.gz \
      -i ${nmaps}/${map}_${reso}mm.nii.gz \
      -n MultiLabel \
      -o $post/$case/nmaps/$str/${case}-${map}.nii.gz \
      -t [$structural/$case/MNI_transforms/${case}-${str}inMNI-0GenericAffine.mat,1] \
      -t $structural/$case/MNI_transforms/${case}-${str}inMNI-1InverseWarp.nii.gz
    
    /project/bbl_projects/apps/melliott/scripts/extract_slice2.sh \
      -MultiLabel $post/$case/nmaps/$str/${case}-${map}.nii.gz \
      $pre/$case/$case-B0B1CESTMAP.nii \
      $post/$case/nmaps/$str/${case}-slice-${map}.nii
    
    gzip $post/$case/nmaps/$str/${case}-slice-${map}.nii
    
    fslmaths $post/$case/nmaps/$str/${case}-slice-${map}.nii.gz \
      -mul $post/$case/$case-tissuemap-bin.nii.gz \
      $post/$case/nmaps/$str/${case}-slice-${map}.nii.gz
    
    fslmaths $post/$case/nmaps/$str/${case}-slice-${map}.nii.gz \
      -bin $post/$case/nmaps/$str/${case}-slice-${map}-bin.nii

done
