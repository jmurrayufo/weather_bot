#!/usr/bin/env python

# Standard Library
import argparse
import datetime
import os
import time

# Local imports
import eco_bee

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", 
    "--verbose", 
    action="count", 
    default=0,
    help="increase output verbosity",
    )
args = parser.parse_args()
if args.verbose > 2:
    print(args)


e = eco_bee.ECO_BEE()

e.update()