#!/bin/bash
# ---------------------------------------------------------------
# EXTRACT_SLICE2.sh
#
# Extract a slice from a 3D set using a slab or 2D image to define the slice
# 
# SIGNIFICANT fix over extract_slice.sh
#   NOTES: the input 2D/slab NIFTI must think it is 3D (i.e. dim0=3)
#          if the input NIFTI is made from a single Dicom, then dcm2nii correctly makes it 3D (but NOT AFNI!!)
#
# Created: M Elliott 5/2019
# ---------------------------------------------------------------

# --- Check args ---
if [ $# -lt 3 -o $# -gt 4 ]; then
    echo "usage: `basename $0` [-MultiLabel] <3Din> <2Din> <2Dout>"
    exit 1
fi

multilabel=0
if [ $1 = "-MultiLabel" ]; then
    multilabel=1
    shift
fi

# --- Standard startup stuff ---
OCD=${PWD}; EXECDIR=`dirname $0`; cd ${EXECDIR}; EXECDIR=${PWD}; cd ${OCD}   # get absolute path to this script
#source ${EXECDIR}/qa_preamble.sh

# --- Build an identity matrix in ITK format ---
ident_matfile="/tmp/ident_itk_${USER}.txt"
cat << EOF > $ident_matfile
#Insight Transform File V1.0
# Transform 0
Transform: MatrixOffsetTransformBase_double_3_3
Parameters: 1 0 0 0 1 0 0 0 1 0 0 0 
FixedParameters: 0 0 0	
EOF

# --- Parse args ---
volfile=`imglob -extension $1`

slicefile=`imglob -extension $2`
indir=`dirname $slicefile`
inbase=`basename $slicefile`
inroot=`remove_ext $inbase`

outfile=$3
outdir=`dirname $outfile`
outbase=`basename $outfile`
outroot=`remove_ext $outbase`
outfile=${outdir}/${outroot}.nii # this makes sure there's a .nii on the outfile

# --- check that input NIFTI is not 2D ---
dim0=`fslval $slicefile dim0`
if [ $dim0 = 2 ]; then
    echo "WARNING: Input slice file $slicefile has dim0 = 2. Changing it to dim0 = 3."
    echo "         But slice location COULD be wrong. NIFTIs made from single dicoms should use dcm2nii."
    ME_fslmodhd.sh $slicefile dim0 3
fi

# --- extract matching slice/slab from 3D volume ---
echo "Extracting slice/slab from $volfile..."
if [ $multilabel = "1" ]; then
    antsApplyTransforms -n MultiLabel -i $volfile -r $slicefile -o $outfile -t $ident_matfile
else
    antsApplyTransforms -i $volfile -r $slicefile -o $outfile -t $ident_matfile
fi

#rm -f $ident_matfile    # should always delete this so next caller has permissions to overwrite it
exit 0
