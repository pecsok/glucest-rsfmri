#!/bin/bash

## DEFINE PATHS ##
structural=$1 
pre=$2
post=$3 #Path to newly warped nmaps 
nmaps=$4 # path to nmaps niftis
log=$5
case=$6
method=$7 
reso=$8 # Resolution. Make sure to resample nmaps before running this script.
str=$9 # UNI or INV2


#######################################################################################################
## ENSURE STRUCTURAL DATA IS AVAILABLE FOR PROCESSING ##

echo "CASE: $case"

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

mkdir $post/$case/ -p
mkdir $post/$case/nmaps
mkdir $post/$case/nmaps/$str

#######################################################################################################
## REGISTER NEUROMAPS TO UNI IMAGES AND GLUCEST IMAGES ##

for nmap in nmaps; do
    nmap_name="${nmap##*/}"

    # Warp neuromap to subject space
    antsApplyTransforms -d 3 -r $structural/$case/${case}-${str}_masked.nii.gz \
      -i ${nmap}_${reso}mm.nii.gz \
      -n MultiLabel \
      -o $post/$case/nmaps/$str/${case}-${nmap_name}.nii.gz \
      -t [$structural/$case/MNI_transforms/${case}-${str}inMNI-0GenericAffine.mat,1] \
      -t $structural/$case/MNI_transforms/${case}-${str}inMNI-1InverseWarp.nii.gz
    
      
    /project/bbl_projects/apps/melliott/scripts/extract_slice2.sh \
      -MultiLabel $post/$case/nmaps/$str/${case}-${nmap_name}.nii.gz \
      $pre/$case/$case-B0B1CESTMAP.nii \
      $post/$case/nmaps/$str/${case}-slice-${nmap_name}.nii
    
    gzip $post/$case/nmaps/$str/${case}-slice-${nmap_name}.nii
    
    fslmaths $post/$case/nmaps/$str/${case}-slice-${nmap_name}.nii.gz \
      -mul $post/$case/$case-tissuemap-bin.nii.gz \
      $post/$case/nmaps/$str/${case}-slice-${nmap_name}.nii.gz
    
    fslmaths $post/$case/nmaps/$str/${case}-slice-${nmap_name}.nii.gz \
      -bin $post/$case/nmaps/$str/${case}-slice-${nmap_name}-bin.nii

done

