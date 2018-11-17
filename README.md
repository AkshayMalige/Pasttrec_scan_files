# Pasttrec_scan_files

In order to setup the pasttrec tools refer https://github.com/HADES-Cracovia/pasttrectools 


To get the width analysis from the baseline scan files run the script calc_baselines_width.py from the folder containing the setup.py in the folder pasttractools-master.
ex:
> sudo python3 setup.py install


> calc_baselines_width.py 


To make changes in the script, edit the file "calc_baselines_width.py" by opening it in the folder "baseline"

The output of "calc_baselines_width.py" is .txt file having the tdc id, card number, asic no, channel , width of the noise, peak position, case status and the file name.

Run 
> Fee_scan_analysis.C 

to get the root file and the desired histogams.
