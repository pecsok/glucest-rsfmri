import os

project = '/cbica/projects/bgdimagecentral/Data/clip-controls/derivatives/qsiprep_0.14.2'
data = os.path.join(project, 'dti_fit')
adult = os.path.join(project, 'tbss', 'fmrib58', 'run_tbss', 'adult')

for sub in os.listdir(data):

    sub_dir = os.path.join(data, sub)

    for ses in os.listdir(sub_dir):

        if ses == 'infant':
            continue

        ses_dir = os.path.join(sub_dir, ses)

        age = ses.split('age')[-1]
        age = int(age)
        age = age / 365.25

        if age >= 3:
            cmd = ['cp', os.path.join(ses_dir, '*FA.nii.gz'), adult]
            os.system(' '.join(cmd))
