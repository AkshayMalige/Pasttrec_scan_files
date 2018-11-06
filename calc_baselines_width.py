import argparse
from colorama import Fore, Style
import copy
import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from pasttrec import *
from scipy.optimize import curve_fit
from scipy.interpolate import splrep, sproot, splev
import os


def bl_list_with_marker(l, pos):
    s = ""
    for i in range(len(l)):
        if i == pos:
            s += Fore.YELLOW + "{:d}".format(l[i]) + Style.RESET_ALL + ", "
        else:
            s += "{:d}, ".format(l[i])
    return s


file = open("output.txt","w")


path = "/home/akshay/FEE_Tests/pasttrectools-master/scan_files/no_pulsar/"
#path = "/home/akshay/FEE_Tests/pasttrectools-master/scan_files/with_pulsar/"
#path = "/home/akshay/FEE_Tests/pasttrectools-master/threshold_scan/D_038_D_039/"
#path = "/home/akshay/FEE_Tests/pasttrectools-master/threshold_scan/test_folder/"


filelist = os.listdir(path)
FWHM_list = []
Peak_norm = []
tdc_cal0 = [1,2]
tdc_cal1 = [0,1]
tdc_cal2 = [0]

plt.figure(1)

for i in filelist:
    if i.endswith(".json"):
        print("Available files : ",i)
 
        with open(path + i, 'r') as json_data:
            d = json.load(json_data)
            json_data.close()

        tdc_cal = []
        file_name = i
        print("just_checking ",file_name)

        if i.startswith("20181010"): #Because only two out of three tdc's were used in my scans.
            tdc_cal = tdc_cal0
        elif i.startswith("20181015_102636"): #Some manipulation required based on the file system for my scans
        #elif i.startswith("20181015_102636"):
            tdc_cal = tdc_cal2
        else:
            tdc_cal = tdc_cal1
         

        print("TDC CAL : ",tdc_cal)

        bls = d['baselines']
        cfg = d['config']

        x_ind =[]
        tlist = []
        p = PasttrecRegs()


        for k,v in cfg.items():
            setattr(p, k, v)

        print(cfg)

        x = list(range(0,32))
        idx = 1
        for k,v in bls.items():
            t = TdcConnection(k)
            plt.figure(idx)

            for c in tdc_cal:
                card = PasttrecCard("noname")

                for a in [0,1]:
                    print(Fore.YELLOW + "Scanning {:s}  CARD: {:d}  ASIC: {:d}".format(k, c, a) + Style.RESET_ALL)
                    bl = [0] * 8
                    for ch in list(range(8)):
                        b = v[c][a][ch]
                        s = 0
                        w = 0
                        #plt.subplot(3, 2, c*2 + a + 1)

                        for i in range(32):
                            s = s + (i+1) * b[i]
                            w += b[i]
                        if w == 0:
                            b = 0
                        else:
                            b = s/w - 1
                        bl[ch] = int(round(b))

                        print(ch,
                              " bl:", Fore.GREEN, "{:2d}".format(bl[ch]), Style.RESET_ALL,
                              "(0x{:s})".format(hex(bl[ch])[2:].zfill(2)),
                              Fore.RED, "{:>+3d} mV".format(-31 + 2 * bl[ch]), Style.RESET_ALL,
                              " [ ", bl_list_with_marker(v[c][a][ch], bl[ch]), "]")
                        
                        dd = v[c][a][ch]
                        sum_d = sum(dd)
                        if sum_d > 0:
                            n = 1.0/sum_d
                        elif sum_d < 0:
                            n = 0
                        else:
                            n = 1.0

                        x_valu =[]

                        Peak_norm.append(np.argmax(dd))

                        for i, j in enumerate(dd):
                            if j > ((np.argmax(dd)) / 10): #anythig above 10% of the peak value
                                x_valu.append(i)
                        ch_status = 1

                        if dd[0]==0 and dd[31]==0 and max(dd)>0:
                            Full_width_hf = len(x_valu)
                            file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        elif dd[0]!=0 and dd[31]!=0:
                             Full_width_hf = len(x_valu)
                             ch_status = 4;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        elif dd[0]==0 and dd[31]!=0:
                             Full_width_hf = len(x_valu)
                             ch_status = 2;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        elif dd[0]!=0 and dd[31]==0:
                             Full_width_hf = len(x_valu)
                             ch_status = 3;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        else:
                             Full_width_hf = len(x_valu)
                             ch_status = 0;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        Ch_sq_no = (16*c)+(8*a)+ch
                        FWHM_list.insert(Ch_sq_no,Full_width_hf)

                t.set_card(c, card)
            tlist.append(t)
            idx += 1

all_peaks =[]
max_of_peak = max(Peak_norm)
for q in Peak_norm:
     all_peaks.append((q*5)/max_of_peak)

xx = [a for a in range((len(filelist)*32)-16)] #-16 since one of the files contains only the results for 1 tdc
plt.plot(xx, FWHM_list, label="some_label1")
plt.xticks([i*16.0 for i in range(0,2*len(filelist))])
plt.yticks([0.,0.5,1.,1.5,5])
plt.grid(True)

file.close()
plt.show()
