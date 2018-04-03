#!/bin/bash
#RE-2_R2==RE-1_R2, RE+2_R2==RE+2_R3
List=(W+2_RB1 W+2_RB2 W+2_RB3 W+2_RB4 W+1_RB1 W+1_RB2 W+1_RB3 W+1_RB4 W-1_RB1 W-1_RB2 W-1_RB3 W-1_RB4 W-2_RB1 W-2_RB2 W-2_RB3 W-2_RB4 W0_RB1 W0_RB2 W0_RB3 W0_RB4 RE+1_R1 RE+1_R2 RE+1_R3 RE+2_R2 RE+2_R3 RE+3_R2 RE+3_R3 RE+4_R2 RE-4_R2 RE-3_R2 RE-3_R2 RE-3_R3 RE-2_R2 RE-2_R3 RE-1_R2 RE-1_R3)
for name in ${List[@]} 
do
  echo "Scanning "$name 
  python working_atRing_level_script_2018data.py $name
done
