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




def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def FWHM(sigma):
    return sigma * np.sqrt(8 * np.log(2))

def bl_list_with_marker(l, pos):
    s = ""
    for i in range(len(l)):
        if i == pos:
            s += Fore.YELLOW + "{:d}".format(l[i]) + Style.RESET_ALL + ", "
        else:
            s += "{:d}, ".format(l[i])
    return s


# if __name__=="__main__":
#     parser=argparse.ArgumentParser(description='Calculates baselines from scan results')
#     parser.add_argument('json_file', help='list of arguments', type=str)

#     parser.add_argument('-o', '--output', help='output file', type=str)

#     group = parser.add_mutually_exclusive_group()
#     group.add_argument('-d', '--dump', help='trbcmd dump file, bl regs only', type=str)
#     group.add_argument('-D', '--Dump', help='trbcmd dump file, all regs', type=str)

#     parser.add_argument('-v', '--verbose', help='verbose level: 0, 1, 2, 3', type=int, choices=[ 0, 1, 2, 3 ], default=0)

#     parser.add_argument('-blo', '--offset', help='offset to baselines (ask for each chip if not given)', type=lambda x: int(x,0))

#     parser.add_argument('-Vth', '--threshold', help='threshold: 0-127 (overwrites value from input file)', type=lambda x: int(x,0))
#     parser.add_argument('-g', '--gain', help='gain: 0-3 (overwrites value from input file)', type=lambda x: int(x,0))


#     args=parser.parse_args()

#     print(args)
file = open("output.txt","w")
# file.write("This is my new file, cheers\n")
# file.write("Akshay Malige")
# file.close()

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

        if i.startswith("20181010"):
            tdc_cal = tdc_cal0
        elif i.startswith("20181015_102636"):
        #elif i.startswith("20181015_102636"):
            tdc_cal = tdc_cal2
        else:
            tdc_cal = tdc_cal1
         

        print("TDC CAL : ",tdc_cal)

        # with open('data.txt') as json_file:  
        #     data = json.load(json_file)


        # dump_file = None
        # if args.dump:
        #     dump_file = open(args.dump, 'w')

        # if args.Dump:
        #     dump_file = open(args.Dump, 'w')

        # out_file = None
        # if args.output:
        #     out_file = open(args.output, 'w')

        bls = d['baselines']
        cfg = d['config']

        x_ind =[]
        tlist = []
        p = PasttrecRegs()


        for k,v in cfg.items():
            setattr(p, k, v)
           # print("P,K,V : ",p,k,v)

        # if args.threshold is not None:
        #     p.vth = args.threshold

        # if args.gain is not None:
        #     p.gain = args.gain

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

                        #d = [i * n for i in dd]
                        Peak_norm.append(np.argmax(dd))
                        #print("Maximum index : ",np.argmax(dd))
                        # pp.append(np.argmax(dd))
                        # if dd[0]==0 and dd[31]==0 and max(dd)>0:

                        for i, j in enumerate(dd):
                            if j > ((np.argmax(dd)) / 10):
                                #print(i)
                                # x_ind.append(i)
                                x_valu.append(i)
                        # print(x_ind)
                        #file.write("D{:s} {:s} {:s} {:s}\n".format(t,c,a, hex(ch)))  
                        ch_status = 1
                        #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                        #print("Check : ", x_valu,len(x_valu),np.argmax(dd))
                        if dd[0]==0 and dd[31]==0 and max(dd)>0:
                            Full_width_hf = len(x_valu)
                            file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                            #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        elif dd[0]!=0 and dd[31]!=0:
                             Full_width_hf = len(x_valu)
                             ch_status = 4;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                             #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))


                        elif dd[0]==0 and dd[31]!=0:
                             Full_width_hf = len(x_valu)
                             ch_status = 2;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                             #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        elif dd[0]!=0 and dd[31]==0:
                             Full_width_hf = len(x_valu)
                             ch_status = 3;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                             #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))

                        else:
                             Full_width_hf = len(x_valu)
                             ch_status = 0;

                             file.write("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))
                             #print("{:s} {:d} {:d} {:d} {:d} {:d} {:d} {:s}\n".format(k,c,a,(8*a)+ch,len(x_valu),np.argmax(dd),ch_status,file_name))



                        Ch_sq_no = (16*c)+(8*a)+ch
                        FWHM_list.insert(Ch_sq_no,Full_width_hf)
                       # print(x_valu)
                        #print("X indexes : ",x_ind)
        #def Gauss(x, a, x0, sigma):
        #   return a * np.exp(-(x - x0)**2 / (2 * sigma**2))
        #popt,pcov = curve_fit(Gauss, x, y, p0=[max(y), mean, sigma])
        #plt.plot(x, y, 'b+:', label='data')
        #plt.plot(x, Gauss(x, *popt), 'r-', label='fit')
                        # mean = sum_d/32
                        # sigma = np.std(dd)
                        #print("dd  : SIGMA : ",dd,mean,sigma)
                        #popt,pcov = curve_fit(Gauss, x, d, p0=[max(d), mean, sigma])
                        #cc = np.array(dd)
                        #print("D   : ",d)
                        #mean = sum(dd)/32
                        #sigma = np.std(cc)
                        #Full_width_hf = FWHM(sigma)
                        #print(" sum mean sigma fwhm  : ",dd,sum(dd),mean,sigma,Full_width_hf)
                      #print ("POPT : ",best_vals)
                        #y = np.array([0, 1, 2, 3, 4, 5, 4, 3, 2, 1])
                       # (mu,sigma) = norm.fit(data)
                       # if mean < 10000:
                            # xx = np.linspace(0 , 31 , 100)
                            # yy = [Gauss(xval , best_vals[0] , best_vals[1] , best_vals[2]) for xval in xx]
                            # print("XX : ",xx)
                        ####plt.plot(x, dd, label='{:d}'.format(ch))
                        #plt.plot(xx, yy, label="some_label1")
                        # print("BEST VALUES : ",best_vals)

                        # xx = np.linspace(d[0] , d[31] , 100)
                        # yy = [Gauss(xval , best_vals[0] , best_vals[1] , best_vals[2]) for xval in xx]
                        # plt.plot(xx, yy, label="some_label1")
                        #print("Fit parameters", best_vals)
                        #plt.plot(x, d, label='{:d}'.format(ch))
                        #### plt.xlabel('baseline register')
                        #### plt.ylabel('pdf')
                        #print("FWHM = ",sigma,Full_width_hf)
                    #plt.legend(loc=6, title='C: {:d}  A: {:d}'.format(c, a))


                    # if args.offset == None:
                    #     while True:
                    #         bbb = input("Offset for base lines (default: 0): ")
                    #         if bbb == "":
                    #             bl_offset = 0
                    #             break

                    #         if not bbb.isdigit():
                    #             print("Input is not a number, try again")
                    #             continue

                    #         bl_offset = int(bbb)
                    #         break
                    # else:
                    #     bl_offset = args.offset

                    # for ch in list(range(8)):

                    #     _r = bl[ch] + bl_offset
                    #     _r = max(_r, 0)
                    #     _r = min(_r, 127)

                    #     p.bl[ch] = _r

                    # card.set_asic(a, copy.deepcopy(p))

                    # if args.dump:
                    #     regs = p.dump_bl_hex(c, a)
                    #     for r in regs:
                    #         dump_file.write("trbcmd w {:s} {:s} {:s}\n".format(k, hex(PasttrecRegs.c_trbnet_reg), r))

                    #         if args.verbose >= 1:
                    #             print("trbcmd w {:s} {:s} {:s}".format(k, hex(PasttrecRegs.c_trbnet_reg), r))

                    # if args.Dump:
                    #     regs = p.dump_config_hex(c, a)
                    #     for r in regs:
                    #         dump_file.write("trbcmd w {:s} {:s} {:s}\n".format(k, hex(PasttrecRegs.c_trbnet_reg), r))

                    #         if args.verbose >= 1:
                    #             print("trbcmd w {:s} {:s} {:s}".format(k, hex(PasttrecRegs.c_trbnet_reg), r))

                t.set_card(c, card)
            tlist.append(t)
            idx += 1

#print("number of peaks",len(Peak_norm))
all_peaks =[]
max_of_peak = max(Peak_norm)
for q in Peak_norm:
     all_peaks.append((q*5)/max_of_peak)
#print("number of peaks ",len(all_peaks))
#print("Number of files : ",len(filelist),len(filelist)*32,len(FWHM_list))
xx = [a for a in range((len(filelist)*32)-16)]
plt.plot(xx, FWHM_list, label="some_label1")
# plt.plot(xx, Peak_norm, label="some_label1")
plt.xticks([i*16.0 for i in range(0,2*len(filelist))])
plt.yticks([0.,0.5,1.,1.5,5])
plt.grid(True)

    # *** printing

    #print(Fore.YELLOW + "{:s}".format(k) + Style.RESET_ALL)

    #for c in [0,1,2]:
        #for a in [0,1]:
            #print(Fore.YELLOW + "  CARD: {:d} ASIC: {:d}".format(k, c, a))
    #print("-----------------------------------------------------------------------------------------------------------------------")
    #print(Style.RESET_ALL)

    #for ch in list(range(8)):
        #for c in [0,1,2]:
            #for a in [0,1]:

    # *** end printing

# if dump_file:
#     dump_file.close()

# if out_file:
#     out_file.write(json.dumps(dump(tlist), indent=2))
#     out_file.close()
file.close()
plt.show()
