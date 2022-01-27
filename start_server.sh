#!/usr/bin/env bash

if [ $# -eq 0 ]
then
  echo "You need to specify the port"
  exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

. /apps/anaconda3/etc/profile.d/conda.sh # taken from .bashrc to initialise conda
module load openeye
conda activate smartsrefine_ws
python smartsrefine.py $1
