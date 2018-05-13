# use for independent ring calculation like for RB1, RB2,...
#python working_atRing_level_script.py W+2_RB1
#import "/afs/cern.ch/sw/lcg/external/Python/3.2.2/x86_64-slc6-gcc48-opt/bin:$PATH"
#export PATH="/afs/cern.ch/sw/XML/texlive/latest/bin/i386-linux:$PATH"
import os
#os.environ['PATH'] = "/afs/cern.ch/sw/XML/texlive/latest/bin/i386-linux"
import pandas
import matplotlib 
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_wheel
import matplotlib.pyplot as plt_fit
import matplotlib.pyplot as plt_delta
import numpy as np
from statistics import mean
from scipy.stats import linregress
from itertools import repeat
import xlrd
from xlrd.sheet import ctype_text
import pathlib
import argparse
#new addition
from PyPDF2 import PdfFileReader, PdfFileMerger
import matplotlib.backends.backend_pdf

parser = argparse.ArgumentParser()
parser.add_argument("w_r_name", help="Calculate average for Wheels and Rings")
parser.add_argument("HV_file", help="Input HV file name")
parser.add_argument("mapping_file", help="Input mapping file name")
parser.add_argument("first_date", help="Input the date 1")
parser.add_argument("second_date", help="Input the date 2")
parser.add_argument("third_date", help="Input the date 3")
parser.add_argument("fourth_date", help="Input the date 4")
args = parser.parse_args()

font = {'family' : 'monospace',
        'weight' : 'semibold',
        'size'   : 11}
matplotlib.rc('font', **font)

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
          'figure.figsize': (7, 6),
          'axes.labelsize': 'large',
          'axes.titlesize':'large',
          'xtick.labelsize':'large',
          'ytick.labelsize':'large'}
pylab.rcParams.update(params)

# Set the font dictionaries (for plot title and axis titles)
#title_font = {'fontname':'Arial', 'size':'10', 'color':'black', 'weight':'normal',
#              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
#axis_font = {'fontname':'Arial', 'size':'10'}

from matplotlib.ticker import FuncFormatter
def sci_notation(x, pos):
    return "${:.1f} \\times 10^{{6}}$".format(x / 1.e7)
#=================Calculate slope from arrays
def best_fit_slope(xs,ys):
  m = (((mean(xs)*mean(ys)) - mean(xs*ys)) / ((mean(xs)**2) - mean(xs**2)))
  return m

MyFormatter = FuncFormatter(sci_notation)
cwd = os.getcwd()
outdir = 'chambersPlots'
if not os.path.exists(outdir):
    os.makedirs(outdir)
Infile1 = args.HV_file
Infile2 = args.mapping_file
sheet1= xlrd.open_workbook(Infile1).sheet_by_name('Sheet1')
sheet2= xlrd.open_workbook(Infile2).sheet_by_name('Sheet1')
rpc_names = []
rpc_names_id = []
for name_idx in range(0,sheet2.nrows):
  rpc_names.append(sheet2.cell_value(name_idx,1))
  rpc_names_id.append(sheet2.cell_value(name_idx,0))
#excel_sheet = xlrd.open_workbook("Copy_of_RPC_Chamber_HV_Map.xlsx")
#sheet_names = excel_sheet.sheet_names()
#print('Sheet Names', excel_sheet.sheet_names())
num_cols = sheet1.ncols
dpid_idx=date_idx=start_date_idx=stop_date_idx=v_app_idx=avg_imon_idx=-444
#for row_idx in range(0, sheet1.nrows):# Iterate through rows
vapp_w2_1, vapp_w2_2, vapp_w2_3, vapp_w2_4, imon_w2_1, imon_w2_2, imon_w2_3, imon_w2_4 = ([] for i in range(8))
vapp1, vapp2, vapp3, vapp4, imon1, imon2, imon3, imon4 = ([] for i in range(8))
voltage1, voltage2, voltage3, voltage4, current1, current2, current3, current4 = ([] for i in range(8))
sheet1_no_row = sheet1.nrows
sheet2_no_row = sheet2.nrows
sec_plot_name = ''
avg_plot_name = ''
no_sheets=0
for sheet2_idx in range(0,sheet2_no_row-1):
#for sheet2_idx in range(0,80):# use this for testing
  print('Scanning for ',args.w_r_name)
  for row_idx in range(0, sheet1_no_row-1):# Iterate through rows
#  for row_idx in range(0, 3000):# Iterate through rows
    for col_idx in range(0, num_cols):# Iterate through columns to find the headers
      cell_val = sheet1.cell_value(row_idx, col_idx)
      if cell_val=='DPID':
        dpid_idx = col_idx 
      elif cell_val=='DATE':
        date_idx = col_idx
      elif cell_val=='START_DATE':
        start_date_idx = col_idx
      elif cell_val=='STOP_DATE':
        stop_date_idx = col_idx
      elif cell_val=='V_APPLIED':
        v_app_idx = col_idx
      elif cell_val=='AVG_IMON':
        imon_idx = col_idx
    new_dpid = sheet1.cell_value(row_idx+1, dpid_idx)
    new_date = sheet1.cell_value(row_idx+1, date_idx)
    new_vapp = sheet1.cell_value(row_idx+1, v_app_idx)
    new_imon = sheet1.cell_value(row_idx+1, imon_idx)
             
#    if new_dpid==rpc_names_id[sheet2_idx]: # compare sheet1 and sheet2 ids. For a single id, it will save the data. 
    if (args.w_r_name in rpc_names[sheet2_idx] and new_dpid==rpc_names_id[sheet2_idx]):
#      print('args.w_r_name: %s rpc_names[sheet2_idx]: %s'%(args.w_r_name,rpc_names[sheet2_idx] ))
      sec_plot_name = rpc_names[sheet2_idx]
      avg_plot_name = rpc_names[sheet2_idx+1]
      if args.first_date in new_date:
        voltage1.append(new_vapp)
        current1.append(new_imon)
        vapp1.append(new_vapp), imon1.append(new_imon)
      if args.second_date in new_date:
        voltage2.append(new_vapp)
        current2.append(new_imon) 
        vapp2.append(new_vapp), imon2.append(new_imon)
      if args.third_date in new_date:
        voltage3.append(new_vapp)
        current3.append(new_imon) 
        vapp3.append(new_vapp), imon3.append(new_imon)
      if args.fourth_date in new_date:
        voltage4.append(new_vapp)
        current4.append(new_imon) 
        vapp4.append(new_vapp), imon4.append(new_imon)
  vapp_w2_temp1=vapp1[:]
  imon_w2_temp1=imon1[:]
  vapp_w2_temp2=vapp2[:]
  imon_w2_temp2=imon2[:]
  vapp_w2_temp3=vapp3[:]
  imon_w2_temp3=imon3[:]
  vapp_w2_temp4=vapp4[:]
  imon_w2_temp4=imon4[:]
  if len(vapp_w2_temp1) != 0:
    vapp_w2_1.append(vapp_w2_temp1)
    imon_w2_1.append(imon_w2_temp1)
  if len(vapp_w2_temp2) != 0:
    vapp_w2_2.append(vapp_w2_temp2)
    imon_w2_2.append(imon_w2_temp2)
  if len(vapp_w2_temp3) != 0:
    vapp_w2_3.append(vapp_w2_temp3)
    imon_w2_3.append(imon_w2_temp3)
  if len(vapp_w2_temp4) != 0:
    vapp_w2_4.append(vapp_w2_temp4)
    imon_w2_4.append(imon_w2_temp4)
  if len(voltage1)==0 and len(voltage2)==0 and len(voltage3)==0 and len(voltage4)==0 :
    continue
  if len(voltage1)!=0:
    plt.scatter(voltage1, current1,color = 'red', label = args.first_date,marker='o')
  if len(voltage2)!=0:
    plt.scatter(voltage2, current2,color="blue", label = args.second_date, marker='o')
  if len(voltage3)!=0:
    plt.scatter(voltage3, current3,color="green", label = args.third_date,marker='o')
  if len(voltage4)!=0:
    plt.scatter(voltage4, current4,color="magenta", label = args.fourth_date,marker='o')
  plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
  plt.xlabel('Voltage (V)')
  plt.ylabel('Current ($\mu$ A)')
  plt.title(rpc_names[sheet2_idx])
  plt.grid()
  plt.draw()
  plt.legend()
  plt.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
  fig = plt.gcf()
##  plt.show()
  plt.close()
  fig.savefig(outdir+'/'+rpc_names[sheet2_idx]+'.pdf')
  del voltage1[:]
  del voltage2[:]
  del voltage3[:]
  del voltage4[:]
  del current1[:]
  del current2[:]
  del current3[:]
  del current4[:]
  
  del vapp1[:]
  del vapp2[:]
  del vapp3[:]
  del vapp4[:]
  del imon1[:]
  del imon2[:]
  del imon3[:]
  del imon4[:]
# make all the lists within the main list with same length
vapp_avg1, vapp_avg2, vapp_avg3, vapp_avg4, imon_avg1, imon_avg2, imon_avg3, imon_avg4  = ([] for i in range(8))
if len(vapp_w2_1) != 0:
  maxLen1 = max(map(len, vapp_w2_1))
  for row in vapp_w2_1:
    if len(row) <= maxLen1:
      zero_list = [0] * (maxLen1 - len(row) )
      row = zero_list + row
      vapp_avg1.append(row) 
  for row in imon_w2_1:
    if len(row) <= maxLen1:
      zero_list = [0] * (maxLen1 - len(row) )
      row = zero_list + row
      imon_avg1.append(row) 

if len(vapp_w2_2) != 0:
  maxLen2 = max(map(len, vapp_w2_2))
  for row in vapp_w2_2:
    if len(row) <= maxLen2:
      zero_list = [0] * (maxLen2 - len(row) )
      row = zero_list + row
      vapp_avg2.append(row) 
  for row in imon_w2_2:
    if len(row) <= maxLen2:
      zero_list = [0] * (maxLen2 - len(row) )
      row = zero_list + row
      imon_avg2.append(row) 

if len(vapp_w2_3) != 0:
  maxLen3 = max(map(len, vapp_w2_3))
  for row in vapp_w2_3:
    if len(row) <= maxLen3:
      zero_list = [0] * (maxLen3 - len(row) )
      row = zero_list + row
      vapp_avg3.append(row) 
  for row in imon_w2_3:
    if len(row) <= maxLen3:
      zero_list = [0] * (maxLen3 - len(row) )
      row = zero_list + row
      imon_avg3.append(row) 

if len(vapp_w2_4) != 0:
  maxLen4 = max(map(len, vapp_w2_4))
  for row in vapp_w2_4:
    if len(row) <= maxLen4:
      zero_list = [0] * (maxLen4 - len(row) )
      row = zero_list + row
      vapp_avg4.append(row) 
  for row in imon_w2_4:
    if len(row) <= maxLen4:
      zero_list = [0] * (maxLen4 - len(row) )
      row = zero_list + row
      imon_avg4.append(row) 
##################################################
if len(vapp_avg1)!=0:
  plt_wheel.scatter([*map(mean, zip(*vapp_avg1))], [*map(mean, zip(*imon_avg1))], color = 'red', label = args.first_date,marker='o')
if len(vapp_avg2)!=0:
  plt_wheel.scatter([*map(mean, zip(*vapp_avg2))], [*map(mean, zip(*imon_avg2))], color = 'blue', label = args.second_date,marker='o')
if len(vapp_avg3)!=0:
  plt_wheel.scatter([*map(mean, zip(*vapp_avg3))], [*map(mean, zip(*imon_avg3))], color = 'green', label = args.third_date,marker='o')
if len(vapp_avg4)!=0:
  plt_wheel.scatter([*map(mean, zip(*vapp_avg4))], [*map(mean, zip(*imon_avg4))], color = 'magenta', label = args.fourth_date,marker='o')

plt_wheel.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
plt_wheel.xlabel('Voltage (V)')
plt_wheel.ylabel('Current ($\mu$ A)')
#print('wheel name is ',args.w_r_name )
plt_wheel.title(args.w_r_name)
plt_wheel.grid()
plt_wheel.draw()
plt_wheel.legend()
plt_wheel.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
fig = plt_wheel.gcf()
#plt_wheel.show()
plt_wheel.close()
fig.savefig(outdir+'/'+args.w_r_name+'_avg.pdf')
#----------------- fit data of Mar-18------------------
i_fit_final_1 = []
v_fit_1 = [*map(mean, zip(*vapp_avg1))]
v_fit1_1= v_fit_1[:6]
v_fit2_1= v_fit_1[6:]
i_fit_1 = [*map(mean, zip(*imon_avg1))]
i_fit1_1= i_fit_1[:6]# ohmic current is here
if len(v_fit_1)!=0:
  z1 = np.polyfit(v_fit1_1, i_fit1_1, 1)# make fit for first part < 7000 V
  f1 = np.poly1d(z1)# find the corresponding polynomial
  i_fit2_1 = f1(v_fit2_1)# find the extrapolated ohmic current
  i_fit_final_1 = np.concatenate((i_fit1_1, i_fit2_1), axis = 0)#make final list of ohmic initial and final extrapolated current
  plt_fit.plot(v_fit_1, i_fit_final_1,'.',v_fit_1,f1(v_fit_1),color = 'red')
  plt_fit.scatter([*map(mean, zip(*vapp_avg1))], [*map(mean, zip(*imon_avg1))], color = 'red', label = args.first_date,marker='o')
#----------------- fit data of April-17------------------
i_fit_final_2 = []
v_fit_2 = [*map(mean, zip(*vapp_avg2))]
v_fit1_2= v_fit_2[:6]
v_fit2_2= v_fit_2[6:]
i_fit_2 = [*map(mean, zip(*imon_avg2))]
i_fit1_2= i_fit_2[:6]# ohmic current is here
if len(v_fit_2)!=0:
  z2 = np.polyfit(v_fit1_2, i_fit1_2, 1)# make fit for first part < 7000 V
  f2 = np.poly1d(z2)# find the corresponding polynomial
  i_fit2_2 = f2(v_fit2_2)# find the extrapolated ohmic current
  i_fit_final_2 = np.concatenate((i_fit1_2, i_fit2_2), axis = 0)#make final list of ohmic initial and final extrapolated current
  plt_fit.plot(v_fit_2, i_fit_final_2,'.',v_fit_2,f2(v_fit_2),color = 'blue')
  plt_fit.scatter([*map(mean, zip(*vapp_avg2))], [*map(mean, zip(*imon_avg2))], color = 'blue', label = args.second_date,marker='o')

#----------------- fit data of Jul-17------------------
i_fit_final_3 = []
v_fit_3 = [*map(mean, zip(*vapp_avg3))]
v_fit1_3= v_fit_3[:6]
v_fit2_3= v_fit_3[6:]
i_fit_3 = [*map(mean, zip(*imon_avg3))]
i_fit1_3= i_fit_3[:6]# ohmic current is here
if len(v_fit_3)!=0:
  z3 = np.polyfit(v_fit1_3, i_fit1_3, 1)# make fit for first part < 7000 V
  f3 = np.poly1d(z3)# find the corresponding polynomial
  i_fit2_3 = f3(v_fit2_3)# find the extrapolated ohmic current
  i_fit_final_3 = np.concatenate((i_fit1_3, i_fit2_3), axis = 0)#make final list of ohmic initial and final extrapolated current
  plt_fit.plot(v_fit_3, i_fit_final_3,'.',v_fit_3,f3(v_fit_3),color = 'green')
  plt_fit.scatter([*map(mean, zip(*vapp_avg3))], [*map(mean, zip(*imon_avg3))], color = 'green', label = args.third_date,marker='o')

#----------------- fit data of Oct-17------------------
i_fit_final_4 = []
v_fit_4 = [*map(mean, zip(*vapp_avg4))]
v_fit1_4= v_fit_4[:6]
v_fit2_4= v_fit_4[6:]
i_fit_4 = [*map(mean, zip(*imon_avg4))]
i_fit1_4= i_fit_4[:6]# ohmic current is here
if len(v_fit_4)!=0:
  z4 = np.polyfit(v_fit1_4, i_fit1_4, 1)# make fit for first part < 7000 V
  f4 = np.poly1d(z4)# find the corresponding polynomial
  i_fit2_4 = f4(v_fit2_4)# find the extrapolated ohmic current
  i_fit_final_4 = np.concatenate((i_fit1_4, i_fit2_4), axis = 0)#make final list of ohmic initial and final extrapolated current

  plt_fit.plot(v_fit_4, i_fit_final_4,'.',v_fit_4,f4(v_fit_4),color = 'magenta')
  plt_fit.scatter([*map(mean, zip(*vapp_avg4))], [*map(mean, zip(*imon_avg4))], color = 'magenta', label = args.fourth_date,marker='o')



  plt_fit.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
  plt_fit.xlabel('Voltage (V)')
  plt_fit.ylabel('Current ($\mu$A)')
  plt_fit.title(args.w_r_name+" linear fit")
  plt_fit.grid()
  plt_fit.draw()
  plt_fit.legend()
  plt_fit.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
  fig_fit = plt_fit.gcf()
  #plt_fit.show()
  plt_fit.close()
  fig_fit.savefig(outdir+'/'+args.w_r_name+'_fit.pdf')

#-------------- Draw the delta(imax-imin) at 6kV and 9.5kV
avg_delta_6kV_xaxis = [args.first_date, args.second_date, args.third_date]
if len(i_fit_final_2)==0:
  avg_delta_95kV_xaxis = [args.first_date, args.second_date, args.third_date ]
  i_avg_delta_95kV = [i_fit_1[-1]-i_fit_final_1[-1]]+[i_fit_3[-1]-i_fit_final_3[-1]]+[i_fit_4[-1]-i_fit_final_4[-1]]
  i_avg_6kV = [i_fit_final_1[5]]+[i_fit_final_2[5]]+[i_fit_final_3[5]]+[i_fit_final_4[5]]
else:
  avg_delta_95kV_xaxis = [args.first_date, args.second_date, args.third_date, args.fourth_date ]
  i_avg_delta_95kV = [i_fit_1[-1]-i_fit_final_1[-1]]+[i_fit_2[-1]-i_fit_final_2[-1]]+[i_fit_3[-1]-i_fit_final_3[-1]]+[i_fit_4[-1]-i_fit_final_4[-1]]
  i_avg_6kV = [i_fit_final_1[5]]+[i_fit_final_2[5]]+[i_fit_final_3[5]]+[i_fit_final_4[5]]
plt_delta.scatter(avg_delta_95kV_xaxis, i_avg_6kV,color = 'red', label = "I (Ohmic)",marker='o')
plt_delta.scatter(avg_delta_95kV_xaxis, i_avg_delta_95kV,color = 'green', label = "$\Delta I (Cosmic)$",marker='o')

#plt_delta.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
plt_delta.xlabel('Condition')
plt_delta.ylabel('I ($\mu$A)')
plt_delta.title(args.w_r_name+" Current differenc")
plt_delta.grid()
plt_delta.draw()
plt_delta.legend()
plt_delta.legend(bbox_to_anchor=(0.01, 0.99), loc=2, borderaxespad=0.)
fig_delta = plt_fit.gcf()
plt_delta.close()
fig_delta.savefig(outdir+'/'+args.w_r_name+'_delta.pdf')
#----------------------------
files_renamed = []
for a in os.listdir(outdir):
  if a.endswith(".pdf"):
    new_name = a.replace("_","")
    new_name1 = new_name.replace("+","p")
    new_name2 = new_name1.replace("-","m")
    os.rename(outdir+"/"+a, outdir+"/"+new_name2)
    files_renamed.append(new_name2)

outtex = open("combine_plots.tex", "w")
outtex.write("\documentclass{article}"+"\n")
outtex.write(r"\usepackage{python}"+"\n")
outtex.write(r"\usepackage{graphicx}"+"\n")
outtex.write(r"\usepackage{caption}"+"\n")
outtex.write(r"\usepackage{hyperref}"+"\n")
outtex.write(r"\usepackage{float}"+"\n")
outtex.write(r"\begin{document}"+"\n")
outtex.write(r"\listoffigures"+"\n")
outtex.write(r"\newpage"+"\n")
outtex.write(r"\begin{python}"+"\n")
outtex.write("import os"+"\n")
outtex.write("directory = 'chambersPlots/'"+"\n")
outtex.write("extension = '.pdf'"+"\n")
outtex.write("files = [file for file in os.listdir(directory) if file.lower().endswith(extension)]"+"\n")
outtex.write("for file in files:"+"\n")
outtex.write("  print (r'\\begin{figure}[H]')"+"\n")
outtex.write("  print (r'\centering')"+"\n")
outtex.write("  print (r'\includegraphics[width=1.2\\textwidth]{%s%s}' % (directory,file))"+"\n")
outtex.write("  print (r'\caption{\detokenize{%s}}' % file)"+"\n")
#outtex.write("  print (r'\label{" "}')"+"\n")
outtex.write("  print (r'\end{figure}')"+"\n")
outtex.write("\end{python}"+"\n")
outtex.write("\end{document}"+"\n")
outtex.close()
os.system("pdflatex --shell-escape combine_plots.tex")
os.system("bibtex combine_plots.aux")
os.system("pdflatex --shell-escape combine_plots.tex")
os.system("pdflatex --shell-escape combine_plots.tex")
########################################################### following lines are for testing
v1 = [3000,4000,5000,6000, 7000,8000,8500,9000,9100,9200,9300,9400,9500,9600,9700]

v2 = [2000,3000,4000,5000,6000,7000,8000,9000,9200,9400,9600]
v3 = [1000,2000,3000,4000,5000,6000,7000,8000,8500,9000,9100,9200,9300,9400,9500,9600,9700,9800]
v4 = [1000,2000,3000,4000,5000,6000,7000,8000,9000,9200,9400,9600,9800]


i1 = [0.200000003,0.178129448,0.122340887,0.300000012, 0.300000012,0.200000003,0.300000012,0.334294573,0.311430586,0.266095899,0.326389427,0.358379679,
0.302102851,0.477980259,0.5]
i2 = [0.345962436,0.354821617,0.414440086,0.472369481,0.586315585,0.591069196,0.530239885,0.702556866,0.717240632,0.781978261,0.799991953]
i4 = [0.35794342,0.502501658,0.64520497,0.699999988,0.699999988,0.815720365,0.936842099,1.033779272,1.196657416,1.105304235,1.200000048,1.319625554,1.373274677]

i3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
'''
plt.scatter(v1, i1,color="red", label = "Mar-18")
plt.scatter(v2, i2,color="blue", label = "Apr-17")
plt.scatter(v3, i3,color="green", label = "Jul-17")
plt.scatter(v4, i4,color="magenta", label = "Oct-17")
'''
############################################################
#def 
