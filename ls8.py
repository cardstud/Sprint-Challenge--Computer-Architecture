#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(r"C:/Users/price/OneDrive/Desktop/cs_s3/Sprint-Challenge--Computer-Architecture/sctest.ls8")
cpu.run()