# Installation packages and running instructions for CMS RPC analyzer code

```
# Input files
The script uses two files "RPC name mapping" and "Current, Voltage" as input 
Ask expert to provide these files and make sure in the script it has same name 

# Set miniconda and latex path
 export PATH="/afs/cern.ch/work/m/mgul/public/rpc_2018_analysis/miniconda3/bin:$PATH"
 export PATH="/afs/cern.ch/sw/XML/texlive/latest/bin/i386-linux:$PATH"

# Clone the analyzer,
 git clone https://github.com/muhammadgul/scripts.git

# (Expert only, works only on my local machine) combine xlsx files:
 python combine_excel_files.py

# Generalized for maximum six data sets:
 python working_atRing_level_script_general.py W+2_RB1 rpc_2018_HV_Imon.xlsx Copy_of_RPC_Chamber_HV_Map.xlsx 14-SEP-16 04-APR-17 24-JUL-17 27-OCT-17 18-APR-18 20-JUN-18

# If you want to less than six, just non that date but then the difference will not be calculated, like:
 python working_atRing_level_script_general.py W+2_RB1 rpc_2018_HV_Imon.xlsx Copy_of_RPC_Chamber_HV_Map.xlsx non 14-SEP-16 04-APR-17 24-JUL-17 27-OCT-17 18-APR-18 

# For full CMS RPCs, run ,
 ./run_full_cms_rpc.sh rpc_2018_HV_Imon.xlsx Copy_of_RPC_Chamber_HV_Map.xlsx 14-SEP-16 04-APR-17 24-JUL-17 27-OCT-17 18-APR-18 20-JUN-18

# (old, not necessary) For a specific Ring/Wheel, with 2016 data use,
 python working_atRing_level_script.py W+2_RB1

# (old, not necessary)For a specific Ring/Wheel, with 2018 data use,
 python working_atRing_level_script_2018data.py W+2_RB1

#The output will be written in chambersPlots directory and a combine pdf will be produced named as combine_plots.pdf 

# Possible error can occur if you have extra paths set in .bashrc file

# git push remotely.
 git add file_name_or_directory
 git commit -m "what you did"
 git push https://github.com/muhammadgul/scripts.git
```    


# (Optional) Required packages for PC or Virutual Machine

```
Uses Python3.6 in Anaconda 
In case of Miniconda,
Install miniconda, https://conda.io/miniconda.html
Update conda by, conda update -n base conda (If needed)

# Open a new terminal to take into account the changes

# Install pandas or numpy or matplotlib or xlrd or  mesa-libgl-cos6-x86_64 by, 
conda install pandas, numpy ,matplotlib, xlrd/mesa-libgl-cos6-x86_64

#For pdflatex, export the path in bash, while in sh, use setenv
export PATH="/afs/cern.ch/sw/XML/texlive/latest/bin/i386-linux:$PATH"

# Clone the analyzer,
git clone https://github.com/muhammadgul/scripts.git

# For a specific Ring/Wheel, use,
python3.6 working_atRing_level_script.py W+2_RB1

# For full CMS RPCs, run, 
./run_full_cms_rpc.sh

#The output will be written in chambersPlots directory and a combine pdf will be produced named as combine_plots.pdf 
```    

# (Optional) If you are interested to use lxplus Virtual Machine, follow the following procedure.
#--------------VM activation-------------
``` 
https://openstack.cern.ch/project/
Subscribe

# wait for an hour to get the confirmation by mail
go again to openstack....
click on instance, just follow the sequence by creating your machine_name,key, etc.

# Depend on network it will take some time to configure machine.
# Once it ready, go to overview to make sure its done
# Open a terminal and connect to your Virtual machine
ssh user_name@machine_name.cern.ch

# To start afs,
/etc/rc.d/init.d/afs start

#Or some time it needs
sudo /etc/rc.d/init.d/afs start

# For more information about HTTPD
https://wwwx.cs.unc.edu/~sparkst/howto/afs.php

#Once it ready, you can install the above packages and run the analysis on VM.
```
