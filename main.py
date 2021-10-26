import os,sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from library import *

##################################
###MAIN CODE
##################################


dirplots='PLOTS'
crdir(dirplots)

dir_gotm_txt='GOTM_INPUT'
crdir(dir_gotm_txt)


df0 = pd.read_csv("TEST_LIST_trajectories.dat", sep="\t",skiprows = 0, engine='python')

#ordering data for ascending date and ascending depth
# yyyymmdd
# Depth positive downward

#df = df0.sort_values(['yyyymmdd', 'time', 'Depth'], ascending=[True, True, True])

#-----------------------
bgc_float_list=['lovbio066d']

var_list=['sigma','TEMP','SAL','EKD','EdPAR','Ed380','Ed412','Ed490','Chl_a']

#var_list=['Temp', 'Sal1','Sig-th','NO21','NO31', 'PO41','O2(1)','CO2', 'Alk','Si1','POC','PON','POP']
#detection_limit={'NO21':0.01, # mmol/m3
#                'NO31':0.05, # mmol/3
#                'PO41':0.01, # mmol/m3
#                'O2(1)':0.5, # umol/kg --> assume is also umol/L
#                'CO2':0.0,   
#                'Alk':0.0,
#                'Si1':0.1,   # mmol/m3
#                'POC':0.5,   # ug/Kg --> assume it is also ug/L
#                'PON':0.5/14., # umol/Kg --> assume is umol/L
#                'POP':0.01,
#                'Chl':0.001,
#                'TDP':0.01,
#                'TOC':np.nan,
#                'TN':0.05,
#                'Temp': np.nan,
#                'Sal1': np.nan,
#                'Sig-th':np.nan} 

bottom_fill={'sigma':True, # if false set bottom value to zero
                'TEMP':True, 
                'SAL':True, 
                'EKD':True,
                'CO2':True,
                'EdPAR':False,
                'Ed380':False,   
                'Ed412':False,  
                'Ed490':False, 
                'Chl_a':False}

bgc_dates=get_float_dates(df0,bgc_float_list[0])
bgc_dates.sort()

outdir="OUTPUT"

for var in var_list:

   file_gotm = outdir + '/' + var + '.prof'
   fid = open(file_gotm,'w')

   for mydate in bgc_dates:

       yyyymmdd=mydate.strftime("%Y%m%d")
       filein=bgc_float_list[0]+ '/' + yyyymmdd +'.profile'
       print(filein)

       if os.path.isfile(filein):

            profile=pd.read_csv(filein, sep="\t",skiprows = 0, engine='python')
            nrows=profile.shape[0] + 2
            gotm_header= mydate.strftime("%Y-%m-%d %H:%M:%S\t" + str(nrows) + "\t2")
            fid.write(gotm_header)
            fid.write("\n")
            fid.write(str(0.))
            fid.write("\t")
            if var=='TEMP':
              t=profile[var].values[0]
              s=profile['SAL'].values[0]
              p=0
              THETA=ptmp(s, t, p, pr=0)
              fid.write(str(THETA))
            else:
              fid.write(str(profile[var].values[0]))

            for d,sal,val in zip(profile['depth'].values,profile['SAL'].values, profile[var].values):
                fid.write("\n")
                fid.write(str(-d))
                fid.write("\t")
                if var=='TEMP':
                   t=val
                   s=sal
                   p=d
                   THETA=ptmp(s, t, p, pr=0)
                   fid.write(str(THETA))
                else:
                   fid.write(str(val))

            fid.write("\n")
            fid.write(str(-10000.))
            fid.write("\t")
            if bottom_fill[var]:
                if var=='TEMP':
                    t=profile[var].values[-1]
                    s=profile['SAL'].values[-1]
                    p=10000
                    THETA=ptmp(s, t, p, pr=0)
                    fid.write(str(THETA))
                else:
                    fid.write(str(profile[var].values[-1]))
            else:
               fid.write(str(0.))

   fid.close()


