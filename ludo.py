#! /bin/python
# staging script for running in a non-dev env
import sys
sys.path.insert(0,'/usr/local/ludo/libs')

from ludomain import main
main()
