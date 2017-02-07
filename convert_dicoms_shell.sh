#!/bin/bash

#BSUB -J psb6351_dcm_convert_hays
#BSUB -o /scratch/PSB6351_2017/week4/hays/dcm_convert_out_hays
#BSUB -e /scratch/PSB6351_2017/week4/hays/dcm_convert_err_hays

./dicomconvert2_GE.py -d /scratch/PSB6351_2017/dicoms -o /scratch/PSB6351_2017/week4/hays/project_folder/ -f /scratch/PSB6351_2017/week4/hays/heuristic_shell.py -q PQ_fasoto -s subj001

