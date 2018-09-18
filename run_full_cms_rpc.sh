#!/bin/bash
#RE-2_R2==RE-1_R2, RE+2_R2==RE+2_R3
List=(W+2_RB1in W+2_RB2in W+2_RB3 W+2_RB4 W+1_RB1in W+1_RB2in W+1_RB3 W+1_RB4 W-1_RB1in W-1_RB2in W-1_RB3 W-1_RB4 W-2_RB1in W-2_RB2in W-2_RB3 W-2_RB4 W0_RB1in W0_RB2in W0_RB3 W0_RB4 W+2_RB1out W+2_RB2out W+1_RB1out W+1_RB2out W-1_RB1out W-1_RB2out W-2_RB1out W-2_RB2out W0_RB1out W0_RB2out RE+1_R1 RE+1_R2 RE+1_R3 RE+2_R2 RE+2_R3 RE+3_R2 RE+3_R3 RE+4_R2 RE-4_R2 RE-3_R2 RE-3_R3 RE-2_R2 RE-2_R3 RE-1_R2 RE-1_R3)
for name in ${List[@]} 
do
  echo "Scanning "$name 
  python working_atRing_level_script_general.py $name $1 $2 $3 $4 $5 $6 $7 $8
done
