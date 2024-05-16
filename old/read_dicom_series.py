import pydicom
import os
import numpy as np
from nibabel.nicom import csareader


def read_dicom_series(dcm_series_dir):
    '''
    Reads a series of dicom files in path <dcm_series_dir>


        Parameters:

            dcm_series_dir (str): path to a series of dicom files


        Returns:

            sum_dcm_series (list): list including a header dictionary, numpy array of images, and a pydicom object

    '''

    header = {}

    dcm_files = []

    # TODO: if the loop ends without finding a proper dcm file raise warning

    num_dcm_files = 0
    for dcm in os.listdir(dcm_series_dir):

        if dcm.endswith(".txt"):
            dcm_hdr_file = os.path.join(dcm_series_dir, dcm)

        # check if dcm is actually a dicom file
        elif not dcm.endswith(".dcm") or dcm.startswith("."):
            continue

        # dcm is a dicom file
        else:
            dcm_path = os.path.join(dcm_series_dir, dcm)
            dcm_files.append(dcm_path)
            num_dcm_files = num_dcm_files + 1

    # need to sort the dcm files by name to read them in correct order
    dcm_files.sort()

    # first file and extract information
    dcm = pydicom.read_file(dcm_files[0])
    # update header info
    header.update({"n1": dcm.Rows,
                   "n2": dcm.Columns,
                   "trajectory": "cartesian"})

    # TODO: Ask Abby What is this????
    # Initialize WIP values
    WIPlong = []
    WIPdbl = []
    for i in range(0, 64):
        WIPlong.append(0)
        if i < 16:
            WIPdbl.append(0)
    # update header info
    header.update({"WIPlong": WIPlong,
                   "WIPdbl": WIPdbl})

    # TODO: I think I should first check if the below attributes exists
    # because maybe it varies by file type. If they are returned regardless,
    # We should be able to extract explicit metadata info by passing an argument
    # in the pydicom.read_file()
    # ProtocolName
    header.update({"ProtocolName": dcm.ProtocolName})

    # ImagedNucleus value
    nucleus = dcm.ImagedNucleus
    if "23N" in nucleus:
        gamma = 11.2620
    elif "170" in nucleus:
        gamma = 5.7716
    elif "13C" in nucleus:
        gamma = 10.7063
    else:
        gamma = 42.5756

    # update header
    header.update({"Nucleus": nucleus})
    header.update({"gamma": gamma})

    # ImagingFrequency
    header.update({"sf": dcm.ImagingFrequency})

    # SliceThickness
    header.update({"slthk": dcm.SliceThickness})

    # NumberofPhaseEncondingSteps
    header.update({"phfov": dcm.NumberOfPhaseEncodingSteps})

    # Number of ReferencedImagedSequence
    header.update({"echoes": len(dcm.ReferencedImageSequence)})

    header.update({"ndim": 2})

    # try:
    #     dcm_txt = open(dcm_hdr_file, "r")
    # except UnboundLocalError:
    #     print("check subject " + dcm_series_dir)

    #TODO: just read the first dicom file not the .txt files
    dcm = pydicom.read_file(dcm_files[0])
    ascconv = csareader.get_csa_header(dcm, 'series')

    ascconv = dict(t.split(' = ') for t in                     # convert key = value format to python dictionary
                   # get ASCII header
                   ascconv['tags']['MrPhoenixProtocol']['items'][0]
                   # strip out the XML-like prefix and suffix
                   .split('### ASCCONV BEGIN')[1]
                   .split('### ASCCONV END ###')[0]
                   .replace('\t', '')                     # remove tabs
                   # split into list by newline
                   .split('\n')
                   [1:-1])                                    # ignore first and last (empty) elements

    if "tSequenceFileName" in ascconv.keys():
        seqname = ascconv["tSequenceFileName"]
        tindex1 = seqname.find('""') + 2
        tindex2 = len(seqname) - 2
        seqname = seqname[tindex1:tindex2]
        header.update({"SeqName": seqname})

    if "sRXSPEC.alDwellTime[0]" in ascconv.keys():
        dwus = float(ascconv["sRXSPEC.alDwellTime[0]"]) * 0.001
        header.update({"dwus": dwus})
        header.update({"sw": 1.0e6 / dwus})

    if "lContrasts" in ascconv.keys():
        header.update({"contrasts": float(ascconv["lContrasts"])})

    if "sSliceArray.asSlice[0].dReadoutFOV" in ascconv.keys():
        rdfov = ascconv["sSliceArray.asSlice[0].dReadoutFOV"]
        header.update({"rdfov": float(rdfov)})

    if "sSliceArray.lSize" in ascconv:
        nslices = ascconv["sSliceArray.lSize"]
        header.update({"nslices": float(nslices)})

    if "sKSpace.lBaseResolution" in ascconv.keys():
        nx = ascconv["sKSpace.lBaseResolution"]
        header.update({"nx": float(nx)})

    if "sKSpace.lPhaseEncodingLines" in ascconv.keys():
        ny = ascconv["sKSpace.lPhaseEncodingLines"]
        header.update({"ny": float(ny)})

    header.update({"ndim": 2})

    if "sKSpace.lImagesPerSlab" in ascconv.keys():
        nz = ascconv["sKSpace.lImagesPerSlab"]
        header.update({"nz": float(nz)})

    if "sKSpace.lRadialViews" in ascconv.keys():
        nrad = ascconv["sKSpace.lRadialViews"]
        header.update({"nrad": float(nrad)})

    if "lAverages" in ascconv.keys():
        averages = ascconv["lAverages"]
        header.update({"averages": float(averages)})

    if "lRepetitions" in ascconv.keys():
        reps = ascconv["lRepetitions"]
        header.update({"reps": int(float(reps)) + 1})

    for ilong in range(0, 64):
        tnamestr = "sWiPMemBlock.alFree[%i]" % ilong
        if tnamestr in ascconv.keys():
            value = float(ascconv[tnamestr])
            header["WIPlong"][ilong] = value

    TEms = []
    for iTE in range(0, 10):
        tnamestr = "alTE[%i]" % iTE
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            TEms.append(float(tname) * 0.001)

    header.update({"TEms": TEms})

    for idbl in range(0, 16):
        tnamestr = "sWiPMemBlock.adFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPdbl"][idbl] = value

    for idbl in range(0, 16):
        tnamestr = "sWipMemBlock.alFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPlong"][idbl] = value

    for idbl in range(0, 16):
        tnamestr = "sWipMemBlock.adFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPdbl"][idbl] = value

    if "sKSpace.ucTrajectory" in ascconv.keys():
        tname = ascconv["sKSpace.ucTrajectory"]

        if "0x" in tname:
            tname1 = tname[3:len(tname)]
            traj = float(tname1, 16)
        else:
            traj = float(tname)
        if traj < 2:
            header.update({"trajectory": "cartesian"})
        else:
            header.update({"trajectory": "radial"})

    if "sKSpace.ucDimension" in ascconv.keys():
        tname = ascconv["sKSpace.ucDimension"]

        if "0x" in tname:
            tname1 = tname[3:len(tname)]
            ndimflag = float(tname1, 16)
            ndim = 1

            while(ndimflag > 1):
                ndim = ndim + 1
                ndimflag = ndimflag/2
            header.update({"ndim": ndim})

        else:
            header.update({"ndim": float(tname)})

    # if ("sProtConsistencyInfo.tBaselineString" in dcm_txt_line) or \
    #         ("sProtConsistencyInfo.tMeasuredBaselineString" in dcm_txt_line):
    #     tindex1 = dcm_txt_line.find('""') + 2
    #     tindex2 = len(dcm_txt_line) - 2
    #     tname = dcm_txt_line[tindex1:tindex2]
    #     header.update({"swversion": tname})

    if "sProtConsistencyInfo.tBaselineString" in ascconv.keys():
        swversion = ascconv["sProtConsistencyInfo.tBaselineString"]
        tindex1 = swversion.find('""') + 2
        tindex2 = len(swversion) - 2
        swversion = swversion[tindex1:tindex2]
        header.update({"swversion": swversion})

    if "echoes" not in header.keys():
        header.update({"echoes": 1})

    header.update({"nTE": header["echoes"]})

    if "radi" in header["trajectory"]:
        header.update({"nrad": 0})

    if header["ndim"] < 3:
        header.update({"nz": 1})

    if "reps" not in header.keys():
        header.update({"reps": 1})

    dcm_images = np.zeros((header["reps"], header["n1"], header["n2"]))

    for rep in range(0, header["reps"]):
        dcm = pydicom.read_file(dcm_files[rep])
        dcm_images[rep] = dcm.pixel_array

    sum_dcm_series = [header, dcm_images, pydicom.dcmread(
        dcm_files[0], stop_before_pixels=True)]

    return sum_dcm_series


def read_3d_dicom_series(dcm_series_dir):
    '''
    Reads a series of 3D dicom files in path <dcm_series_dir>


        Parameters:

            dcm_series_dir (str): path to a series of dicom files


        Returns:

            sum_dcm_series (list): list including a header dictionary, numpy array of images, and a pydicom object

    '''

    header = {}

    dcm_files = []

    # TODO: if the loop ends without finding a proper dcm file raise warning

    num_dcm_files = 0
    for dcm in os.listdir(dcm_series_dir):

        if dcm.endswith(".txt"):
            dcm_hdr_file = os.path.join(dcm_series_dir, dcm)

        # check if dcm is actually a dicom file
        elif not dcm.endswith(".dcm"):
            continue

        # dcm is a dicom file
        else:
            dcm_path = os.path.join(dcm_series_dir, dcm)
            dcm_files.append(dcm_path)
            num_dcm_files = num_dcm_files + 1

    # need to sort the dcm files by name to read them in correct order
    dcm_files.sort()

    # first file and extract information
    dcm = pydicom.read_file(dcm_files[0])
    # update header info
    header.update({"n1": dcm.Rows,
                   "n2": dcm.Columns})
    # "trajectory": "cartesian"})

    # TODO: Ask Abby What is this????
    # Initialize WIP values
    WIPlong = []
    WIPdbl = []
    for i in range(0, 64):
        WIPlong.append(0)
        if i < 16:
            WIPdbl.append(0)
    # update header info
    header.update({"WIPlong": WIPlong,
                   "WIPdbl": WIPdbl})

    # TODO: I think I should first check if the below attributes exists
    # because maybe it varies by file type. If they are returned regardless,
    # We should be able to extract explicit metadata info by passing an argument
    # in the pydicom.read_file()
    # ProtocolName
    header.update({"ProtocolName": dcm.ProtocolName})

    # ImagedNucleus value
    nucleus = dcm.ImagedNucleus
    if "23N" in nucleus:
        gamma = 11.2620
    elif "170" in nucleus:
        gamma = 5.7716
    elif "13C" in nucleus:
        gamma = 10.7063
    else:
        gamma = 42.5756

    # update header
    header.update({"Nucleus": nucleus})
    header.update({"gamma": gamma})

    # ImagingFrequency
    header.update({"sf": dcm.ImagingFrequency})

    # SliceThickness
    header.update({"slthk": dcm.SliceThickness})

    # NumberofPhaseEncondingSteps
    header.update({"phfov": dcm.NumberOfPhaseEncodingSteps})

    # Number of ReferencedImagedSequence
    header.update({"echoes": len(dcm.ReferencedImageSequence)})

    header.update({"ndim": 2})

    # try:
    #     dcm_txt = open(dcm_hdr_file, "r")
    # except UnboundLocalError:
    #     print("check subject " + dcm_series_dir)

    #TODO: just read the first dicom file not the .txt files
    dcm = pydicom.read_file(dcm_files[0])
    ascconv = csareader.get_csa_header(dcm, 'series')

    ascconv = dict(t.split(' = ') for t in                     # convert key = value format to python dictionary
                   # get ASCII header
                   ascconv['tags']['MrPhoenixProtocol']['items'][0]
                   # strip out the XML-like prefix and suffix
                   .split('### ASCCONV BEGIN')[1]
                   .split('### ASCCONV END ###')[0]
                   .replace('\t', '')                     # remove tabs
                   # split into list by newline
                   .split('\n')
                   [1:-1])                                    # ignore first and last (empty) elements

    if "tSequenceFileName" in ascconv.keys():
        seqname = ascconv["tSequenceFileName"]
        tindex1 = seqname.find('""') + 2
        tindex2 = len(seqname) - 2
        seqname = seqname[tindex1:tindex2]
        header.update({"SeqName": seqname})

    if "sRXSPEC.alDwellTime[0]" in ascconv.keys():
        dwus = float(ascconv["sRXSPEC.alDwellTime[0]"]) * 0.001
        header.update({"dwus": dwus})
        header.update({"sw": 1.0e6 / dwus})

    if "lContrasts" in ascconv.keys():
        header.update({"contrasts": float(ascconv["lContrasts"])})

    if "sSliceArray.asSlice[0].dReadoutFOV" in ascconv.keys():
        rdfov = ascconv["sSliceArray.asSlice[0].dReadoutFOV"]
        header.update({"rdfov": float(rdfov)})

    if "sSliceArray.lSize" in ascconv:
        nslices = ascconv["sSliceArray.lSize"]
        header.update({"nslices": int(nslices)})

    if "sKSpace.lBaseResolution" in ascconv.keys():
        nx = ascconv["sKSpace.lBaseResolution"]
        header.update({"nx": float(nx)})

    if "sKSpace.lPhaseEncodingLines" in ascconv.keys():
        ny = ascconv["sKSpace.lPhaseEncodingLines"]
        header.update({"ny": float(ny)})

    # header.update({"ndim": 2})

    if "sKSpace.lImagesPerSlab" in ascconv.keys():
        nz = ascconv["sKSpace.lImagesPerSlab"]
        header.update({"nz": int(nz)})

    if "sKSpace.lRadialViews" in ascconv.keys():
        nrad = ascconv["sKSpace.lRadialViews"]
        header.update({"nrad": float(nrad)})

    if "lAverages" in ascconv.keys():
        averages = ascconv["lAverages"]
        header.update({"averages": float(averages)})

    if "lRepetitions" in ascconv.keys():
        reps = ascconv["lRepetitions"]
        header.update({"reps": int(float(reps)) + 1})

    # for ilong in range(0, 64):
    #     tnamestr = "sWiPMemBlock.alFree[%i]" % ilong
    #     if tnamestr in ascconv.keys():
    #         value = float(ascconv[tnamestr])
    #         header["WIPlong"][ilong] = value

    for ilong in range(0, 64):
        tnamestr = "sWipMemBlock.alFree[%i]" % ilong
        if tnamestr in ascconv.keys():
            value = int(ascconv[tnamestr])
            header["WIPlong"][ilong] = value

    TEms = []
    for iTE in range(0, 10):
        tnamestr = "alTE[%i]" % iTE
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            TEms.append(float(tname) * 0.001)

    header.update({"TEms": TEms})

    for idbl in range(0, 16):
        tnamestr = "sWiPMemBlock.adFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPdbl"][idbl] = value

    for idbl in range(0, 16):
        tnamestr = "sWipMemBlock.alFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPlong"][idbl] = value

    for idbl in range(0, 16):
        tnamestr = "sWipMemBlock.adFree[%i]" % idbl
        if tnamestr in ascconv.keys():
            tname = ascconv[tnamestr]
            value = float(tname)
            header["WIPdbl"][idbl] = value

    if "sKSpace.ucTrajectory" in ascconv.keys():
        tname = ascconv["sKSpace.ucTrajectory"]

        if "0x" in tname:
            tname1 = tname[3:len(tname)]
            traj = float(tname1, 16)
        else:
            traj = float(tname)
        if traj < 2:
            header.update({"trajectory": "cartesian"})
        else:
            header.update({"trajectory": "radial"})

    if "sKSpace.ucDimension" in ascconv.keys():
        tname = ascconv["sKSpace.ucDimension"]

        # if "0x" in tname:
        #     tname1 = tname[3:len(tname)]
        #     ndimflag = float(tname1)
        ndimflag = float(tname)
        ndim = 1
        while(ndimflag > 1):
            ndim = ndim + 1
            ndimflag = ndimflag/2
        header.update({"ndim": ndim})

        # else:
        #     header.update({"ndim": int(tname)})

    # if ("sProtConsistencyInfo.tBaselineString" in dcm_txt_line) or \
    #         ("sProtConsistencyInfo.tMeasuredBaselineString" in dcm_txt_line):
    #     tindex1 = dcm_txt_line.find('""') + 2
    #     tindex2 = len(dcm_txt_line) - 2
    #     tname = dcm_txt_line[tindex1:tindex2]
    #     header.update({"swversion": tname})

    if "sProtConsistencyInfo.tBaselineString" in ascconv.keys():
        swversion = ascconv["sProtConsistencyInfo.tBaselineString"]
        tindex1 = swversion.find('""') + 2
        tindex2 = len(swversion) - 2
        swversion = swversion[tindex1:tindex2]
        header.update({"swversion": swversion})

    if "echoes" not in header.keys():
        header.update({"echoes": 1})

    header.update({"nTE": header["echoes"]})

    # if "radi" in header["trajectory"]:
    header.update({"nrad": 0})

    if header["ndim"] < 3:
        header.update({"nz": header["nslices"]})

    if "reps" not in header.keys():
        header.update({"reps": 1})

    ### TODO: figure out 4 dimension indexing style for Python
    # if num_dcm_files != header["reps"] * header["nz"]:
        # TODO: throw WARNING:

    dcm_images = np.zeros((header["reps"], header["nz"],
                           header["n1"], header["n2"]))

    for rep in range(0, header["reps"]):
        for z in range(0, header["nz"]):
            ind1 = rep * header["nz"] + z
            dcm = pydicom.read_file(dcm_files[ind1])
            dcm_images[rep, z] = dcm.pixel_array

    sum_dcm_series = [header, dcm_images, pydicom.dcmread(
        dcm_files[0], stop_before_pixels=True)]

    return sum_dcm_series
