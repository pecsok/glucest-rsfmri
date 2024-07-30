import os
import sys
import argparse

post=$1 # Path to sliced nmaps and atlases in subject space (PREV $post)
outputpath=$2
nmaps=$3 # NMAPS path
str=$4 # UNI or INV2

def postprocess(script, post, output, nmaps, str_type):
    
    for case in os.listdir(data):

        if not os.path.isdir(os.path.join(post, case)) and os.path.isfile(os.path.join(pre, case, case + '-B0B1CESTMAP.nii')):
            # use bsub line below of LSF emails don't work
            #'bsub -o /project/bbl_roalf_longglucest/sandbox/ally/test_schaefer/error_log.txt'

            print(case)
            cmd = ['bsub', script, data, pre, post, 
                   nmaps, log, case, resolution, str_type]
            os.system(' '.join(cmd))
    
    return

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '-d', '--data',
        help = 'Path to data directory',
        required = True)
    required.add_argument(
        '-p', '--pre',
        help = 'path to preprocessed cest data',
        required = True)
    required.add_argument(
        '-o', '--post',
        help = 'Path to postprocessed output cest',
        required = True)
    required.add_argument(
        '-n', '--nmap',
        help = 'Path to neuromaps',
        required = True)
    required.add_argument(
        '-l', '--logs',
        help = 'Path to logs',
        required = True)
    required.add_argument(
        '-s', '--script',
        help = 'Path to step1_slice_nmap.sh',
        required = True)
    required.add_argument(
        '-r', '--resolution',
        help = 'Voxel resolution (ex. 0.7)',
        required = True)
    required.add_argument(
        '-t', '--str_type',
        help = 'Type of structural image (ex. INV2, UNI, mprage)',
        required = True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    postprocess(args.script, args.data, args.pre, args.post, 
                args.atlas, args.logs, args.resolution, args.str_type)

    return


if __name__ == "__main__":
    main()

