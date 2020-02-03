#!/bin/bash

def=$(date '+%Y%m%d')

python3 ~/javlibrary/bestrated.py | tee ~/javlibrary/bestrated-${def}.txt
python3 ~/javlibrary/mostwanted.py | tee ~/javlibrary/mostwanted-${def}.txt
python3 ~/javlibrary/star_mostfav.py | tee ~/javlibrary/star_mostfav-${def}.txt
