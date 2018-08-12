#!/bin/bash
#RE-2_R2==RE-1_R2, RE+2_R2==RE+2_R3
List=(W+2_RB1in W+2_RB2in W+2_RB3in W+2_RB4in W+1_RB1in W+1_RB2in W+1_RB3in W+1_RB4in W-1_RB1in W-1_RB2in W-1_RB3in W-1_RB4in W-2_RB1in W-2_RB2in W-2_RB3in W-2_RB4in W0_RB1in W0_RB2in W0_RB3in W0_RB4in W+2_RB1out W+2_RB2out W+2_RB3out W+2_RB4out W+1_RB1out W+1_RB2out W+1_RB3out W+1_RB4out W-1_RB1out W-1_RB2out W-1_RB3out W-1_RB4out W-2_RB1out W-2_RB2out W-2_RB3out W-2_RB4out W0_RB1out W0_RB2out W0_RB3out W0_RB4out RE+1_R1 RE+1_R2 RE+1_R3 RE+2_R2 RE+2_R3 RE+3_R2 RE+3_R3 RE+4_R2 RE-4_R2 RE-3_R2 RE-3_R2 RE-3_R3 RE-2_R2 RE-2_R3 RE-1_R2 RE-1_R3)
for name in ${List[@]} 
do
  echo "Scanning "$name 
  python working_atRing_level_script_general.py $name $1 $2 $3 $4 $5 $6
done
