# Installation and running instructions for CMS RPC analyzer code

```
# Input files
The script uses two files "RPC name mapping" and "Current, Voltage" as input 
Ask expert to provide these files and make sure in the script it has same name 

# Required packages
Uses Python3.6 in Anaconda 
In case of Miniconda,
Install miniconda, https://conda.io/miniconda.html
Update conda by, conda update -n base conda (If needed)

# Install pandas or numpy or matplotlib or xlrd or  mesa-libgl-cos6-x86_64 by, 
conda install pandas, numpy ,matplotlib, xlrd/mesa-libgl-cos6-x86_64

#For pdflatex, export the path in bash, while in sh, use setenv
export PATH="/afs/cern.ch/sw/XML/texlive/latest/bin/i386-linux:$PATH"

# Clone the analyzer,
git clone https://github.com/muhammadgul/scripts.git

# For full CMS RPCs, run, 
./run_full_cms_rpc.sh

# For a specific Ring/Wheel, use,
python3.6 working_atRing_level_script.py W+2_RB1 

#The output will be written in chambersPlots directory and a combine pdf will be produced named as combine_plots.pdf 
```    

# If you are interested to use lxplus Virtual Machine, follow the following procedure.
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
