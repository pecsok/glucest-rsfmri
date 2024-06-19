{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "38e45b22-d9b0-4f97-a151-f923cb4a393b",
   "metadata": {},
   "source": [
    "# Extract2Slice"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "38cdb3a7-3147-4035-b2c1-1bacc5accbe7",
   "metadata": {},
   "source": [
    "This notebook:\n",
    "1. loads packages\n",
    "2. loops through subjects\n",
    "3. applies subject slice to nmap to extract data "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7982cff0-ab85-4c8c-89fa-27bd18e169cb",
   "metadata": {},
   "source": [
    "## Load Packages"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "f448dad2-778b-4eda-a131-10b30669ddf5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b318884b-a968-4698-abd7-27b6c7ca8c47",
   "metadata": {},
   "source": [
    "## Set variables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "6fc98b88-4751-46e6-81d1-906cfa5b54e3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remotedata/cest/preprocessed/\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/\n"
     ]
    }
   ],
   "source": [
    "# Set path for downloading neuromaps data\n",
    "#root = '/project/bbl_roalf_pecsokphd/projects/glucest-rsfmri' # or \n",
    "root = '/Users/pecsok/Desktop/ImageData/PMACS_remote'\n",
    "\n",
    "cest_path = root + '/data/cest/'\n",
    "nmaps_path = root + '/data/nmaps/'\n",
    "outpath = root + '/data/nmaps/subj_data/'\n",
    "extract = root + '/github/glucest-rsfmri/cest_nmaps_pipeline/cest2_extract_slice.py'\n",
    "structural_path = root + '/data/cest/preprocessed/'\n",
    "subjlist_csv = root + '/data/subject_list_031124.csv'\n",
    "subjlist = pd.read_csv(subjlist_csv)\n",
    "\n",
    "nmaps = (root + '/data/nmaps/average_mGluR.nii.gz', root + '/data/nmaps/average_NMDA.nii.gz')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "727fdb39-3cfe-49ee-8f88-e3428063561d",
   "metadata": {},
   "source": [
    "## Loop through subjects and extract nmaps slice data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "01b70dab-14ca-4770-8785-8e62a2ac6eaf",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "20303_12234\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "90217_12230\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "88608_12108\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "21874_12094\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "94288_12092\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "94703_12082\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93757_12015\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "96902_11903\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20792_11887\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20325_11852\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "88760_11846\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "125073_11814\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "115783_11788\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "118864_11783\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "116354_11774\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "111720_11766\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "91422_11753\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20642_11261\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20645_11260\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20543_11259\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "112126_11157\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "106057_11122\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "89095_11100\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "97994_11114\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "19981_11106\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "96659_11096\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "91962_11090\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "92211_10981\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "85743_10944\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93292_10938\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "94276_10927\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "125511_10906\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "90281_10902\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20011_10888\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "121085_10851\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "19970_10827\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "105979_10791\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93274_10765\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "132179_10760\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "80557_10738\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "83835_10706\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "120217_10722\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93734_10694\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "119791_10705\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "132641_10692\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "106880_10699\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "102041_10675\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "121407_10688\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "90077_10962\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20082_11821\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20754_12200\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20871_11917\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20902_12766\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20903_12159\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "92089_12089\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "95257_12041\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "98370_12558\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "127065_12752\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "127935_12101\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20916_12762\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "21118_12784\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "22744_12533\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93242_12442\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "94378_11833\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "96465_12069\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "100522_12003\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "112807_11890\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "114738_11706\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "117847_12740\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "126176_12780\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "126532_12582\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "128079_11934\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "128259_12837\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "128865_12325\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "130438_11999\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "131384_12198\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "132869_12109\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "135085_11812\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "135277_12808\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "117397_10686\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "87646_10754\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93242_11850\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "116019_11135\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "106057_11122\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "89095_11100\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "97994_11114\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "19981_11106\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "96659_11096\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "90281_11093\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20180_11011\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "92211_10981\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "90077_10962\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93292_10938\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "125511_10906\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "102041_10821\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "121085_10851\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "19790_10819\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "105979_10791\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "19830_10789\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "80557_10738\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "119791_10705\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "132641_10692\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "106880_10699\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "121407_10688\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93734_10694\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "20645_11260\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "83835_10706\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "85743_10944\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20642_11261\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "20011_10888\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "91919_10683\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "20543_11259\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "81725_11109\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "87225_10933\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "88608_10764\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "90877_10907\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "92155_11022\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "93274_10765\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "112126_11157\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n",
      "139272_10739\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_mGluR.nii.gz\n",
      "/Users/pecsok/Desktop/ImageData/PMACS_remote/data/nmaps/average_NMDA.nii.gz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n",
      "sh: bsub: command not found\n"
     ]
    },
    {
     "ename": "ValueError",
     "evalue": "cannot convert float NaN to integer",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[17], line 3\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;66;03m# Loop through subjects\u001b[39;00m\n\u001b[1;32m      2\u001b[0m \u001b[38;5;28;01mfor\u001b[39;00m index, row \u001b[38;5;129;01min\u001b[39;00m subjlist\u001b[38;5;241m.\u001b[39miterrows():\n\u001b[0;32m----> 3\u001b[0m     bblid \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mstr\u001b[39m(\u001b[38;5;28;43mint\u001b[39;49m\u001b[43m(\u001b[49m\u001b[43mrow\u001b[49m\u001b[43m[\u001b[49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mBBLID\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m]\u001b[49m\u001b[43m)\u001b[49m)\n\u001b[1;32m      4\u001b[0m     ses \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mstr\u001b[39m(\u001b[38;5;28mint\u001b[39m(row[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mSCANID_CEST\u001b[39m\u001b[38;5;124m'\u001b[39m]))\n\u001b[1;32m      5\u001b[0m     case \u001b[38;5;241m=\u001b[39m bblid \u001b[38;5;241m+\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m_\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;241m+\u001b[39m ses\n",
      "\u001b[0;31mValueError\u001b[0m: cannot convert float NaN to integer"
     ]
    }
   ],
   "source": [
    "# Loop through subjects\n",
    "for index, row in subjlist.iterrows():\n",
    "    bblid = str(int(row['BBLID']))\n",
    "    ses = str(int(row['SCANID_CEST']))\n",
    "    case = bblid + \"_\" + ses\n",
    "    print(case)\n",
    "\n",
    "    # Set path to subject's structural data\n",
    "    structural = structural_path + case \n",
    "    \n",
    "    for nmap in nmaps:\n",
    "        print(nmap)\n",
    "        cmd = ['bsub', extract, structural, outpath, bblid, nmap]\n",
    "        os.system(' '.join(cmd))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}