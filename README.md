### Jason Hays readme file for homework: week 4
There were a few steps to making the nii files:
* Finding the right values for the convert shell file.
* Fixing/debugging errors and changing err/out files.
 * Finding what to change in the heuristic file.
  * Finding appropriate values for the heuristic file.

### Finding the right values for the convert shell file.
* Using the default converter (no -c means dcm2nii), the file would start like this:
`./dicomconvert2_GE.py -d /scratch/... -o /scratch/... -f /scratch/... -q ... -s ...`

* This step involved looking into the dicomconvert2_GE.py file to double check what the parameters were.
 * -d is the dicom folder.
 * -o is the output project folder.
 * -f is the heuristic file that establishes what types of scans for which nii files are created.
 * -q is the LSF queue.
 * -s is the subject list (one person).
 * -c was the converter, but I'm using the default (no known reason to use mri_convert over dcm2nii yet).

* Thus, the file ended like this:
`./dicomconvert2_GE.py -d /scratch/PSB6351_2017/dicoms -o /scratch/PSB6351_2017/week4/hays/project_folder/ -f /scratch/PSB6351_2017/week4/hays/heuristic_shell.py -q PQ_fasoto -s subj001`

### Fixing/debugging errors and changing err/out files.
* Running the convert_dicom_shell.sh as it was would cause both runtime errors and debugging issues.
 * The variable, trd_bold, was not defined and needed to simply be "bold" in the heuristic file (because "bold" was defined and the placement corresponded with the t1 and dwi).
 * Furthermore, the err and out file locations needed to be updated in the dicomconvert2_GE.py to avoid overriding other students' err and out files.

### Finding what to change in the heuristic file.
* I wrote debugging file writers (because print() doesn't always work conveniently on LSF jobs) to figure out what values seqinfo contained before I knew what the heuristic file parameters were.
 * They suggested that sl was the total slice count, nt was number of temporal positions, and s[12] was the series description.

### Finding appropriate values for the heuristic file.
* To find the slices for the structural scan, you can check Z01 (a T1 dicom) for the slice count (186) using the dicom_hdr command and the bash command grep with Perl regular expressions.
`dicom_hdr /scratch/PSB6351_2017/dicoms/subj001/A/Z01 | grep -Po .*Acquisition//.*`

* There was no particular reason to prevent the bold dicoms' nt's from being a single value, so it was left as `nt != "**"` because it would not affect any of them -- the sub-name restriction of "TRD" was enough to get the full list of bold dicom files.
 * To make sure there were not negative nt values (or some other obvious bad values).  The full list of the number of temporal positions was obtained with:
 `dicom_hdr /scratch/PSB6351_2017/dicoms/subj001/A/* | grep -Po .*Temporal.* | sort | uniq`

* To find a list of all applicable scan descriptions, the following command can be run to pipe the header to a regular expression search:
`dicom_hdr /scratch/PSB6351_2017/dicoms/subj001/A/* | grep -Po .*Descr.* | sort | uniq`
 * This revealed that the diffusion weighted image needed to look for "DTI" (after waiting a while!), which represents diffusion tensor imaging.

### Output .nii Files
* In total, there were 7 bold nii files, 1 diffusion weighted image nii file, and 1 anatomical (T1) nii file, which were readable in afni's viewer.
