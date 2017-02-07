import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    
    allowed template fields - follow python string module: 
    
    item: index within category 
    subject: participant id 
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    dwi = create_key('dmri/dwi_{item:03d}', outtype=('dicom', 'nii.gz'))
    t1 = create_key('anatomy/T1_{item:03d}', outtype=('dicom', 'nii.gz'))
    bold = create_key('bold/bold_{item:03d}/bold', outtype=('dicom', 'nii.gz'))
    info = {dwi: [], t1: [], bold: []}
    last_run = len(seqinfo)
    # check all descriptions with
    # dicom_hdr * | grep -Po .*[^0-9.]Descr[^0-9.].* | sort | uniq
    # to find that the ending ones need DTI, TRD, and T1
    '''0008 103e       12 [640     ] //          ID Series Description//Screen Save 
0008 103e       16 [704     ] //          ID Series Description//3Plane_Loc_SSFSE
0008 103e       18 [700     ] //          ID Series Description//DTI_60_Directions 
0008 103e       18 [704     ] //          ID Series Description//ASSET_calibration 
0008 103e       18 [704     ] //          ID Series Description//DTI_60_Directions 
0008 103e       34 [684     ] //          ID Series Description//PU:3D_T1_Sag-Structural_(FSPGR_BR 
0008 103e       34 [688     ] //          ID Series Description//PU:3D_T1_Sag-Structural_(FSPGR_BR 
0008 103e       34 [700     ] //          ID Series Description//3D_T1_Sag-Structural_(FSPGR_BRAVO)
0008 103e       34 [704     ] //          ID Series Description//3D_T1_Sag-Structural_(FSPGR_BRAVO)
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_1
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_2
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_3
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_4
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_5
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_6
0008 103e        8 [704     ] //          ID Series Description//SEQTRD_7
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_1
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_2
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_3
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_4
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_5
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_6
0008 103e        8 [708     ] //          ID Series Description//SEQTRD_7
    '''

    '''dicom_hdr * | grep -Po .*[^0-9.]Temporal[^0-9.].* | sort | uniq
0020 0105        2 [3174    ] //REL Number of Temporal Positions//79
0020 0105        2 [3174    ] //REL Number of Temporal Positions//90
0020 0105        2 [3176    ] //REL Number of Temporal Positions//79
0020 0105        2 [3176    ] //REL Number of Temporal Positions//90
0020 0105        2 [3178    ] //REL Number of Temporal Positions//79
0020 0105        2 [3178    ] //REL Number of Temporal Positions//90
0020 0105        2 [3180    ] //REL Number of Temporal Positions//79
0020 0105        2 [3180    ] //REL Number of Temporal Positions//90
0020 0105        4 [3174    ] //REL Number of Temporal Positions//114 
0020 0105        4 [3174    ] //REL Number of Temporal Positions//152 
0020 0105        4 [3174    ] //REL Number of Temporal Positions//226 
0020 0105        4 [3174    ] //REL Number of Temporal Positions//395 
0020 0105        4 [3174    ] //REL Number of Temporal Positions//708 
0020 0105        4 [3176    ] //REL Number of Temporal Positions//114 
0020 0105        4 [3176    ] //REL Number of Temporal Positions//152 
0020 0105        4 [3176    ] //REL Number of Temporal Positions//226 
0020 0105        4 [3176    ] //REL Number of Temporal Positions//395 
0020 0105        4 [3176    ] //REL Number of Temporal Positions//708 
0020 0105        4 [3178    ] //REL Number of Temporal Positions//114 
0020 0105        4 [3178    ] //REL Number of Temporal Positions//152 
0020 0105        4 [3178    ] //REL Number of Temporal Positions//226 
0020 0105        4 [3178    ] //REL Number of Temporal Positions//395 
0020 0105        4 [3178    ] //REL Number of Temporal Positions//708 
0020 0105        4 [3180    ] //REL Number of Temporal Positions//114 
0020 0105        4 [3180    ] //REL Number of Temporal Positions//152 
0020 0105        4 [3180    ] //REL Number of Temporal Positions//226 
0020 0105        4 [3180    ] //REL Number of Temporal Positions//395 
0020 0105        4 [3180    ] //REL Number of Temporal Positions//708 
    '''


    # Number of Temporal positions is nt
    hays = open("/scratch/PSB6351_2017/week4/hays/debug2.txt", 'w')
    hays.write(str(seqinfo))

    for s in seqinfo:
        hays.write("s[8] type {0} == {3}: str {1}, num {2}\n".format(s[8], s[8]=='186', s[8]==186, type(s[8])))
        x,y,sl,nt = (s[6], s[7], s[8], s[9])
        # number of slices for the T1
        if (sl == 186) and (nt == 1) and ('T1' in s[12]):
            info[t1].append(s[2])
        elif (nt != '**') and ('TRD' in s[12]):# nt was '**'
            info[bold].append(s[2])
            last_run = s[2]
        # we needed a DWI, and the diffusion tensor image (DTI) was the only matching label.
        elif (sl > 1) and ('DTI' in s[12]):
            info[dwi].append(s[2])
        else:
            pass
    hays.flush()
    hays.close()
    return info
