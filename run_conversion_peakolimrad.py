#! /usr/bin/env python3
# coding=utf-8

import datetime
#import matplotlib
#matplotlib.use('Agg')
#import numpy as np
#import matplotlib.pyplot as plt

#import sys, os
import peakTree
import peakTree.helpers as h

import logging
log = logging.getLogger('peakTree')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

#pTB = peakTree.peakTreeBuffer(system='limrad_peako')
pTB = peakTree.peakTreeBuffer(system='limrad_punta')

# IDEA: for now run with temporal_average = False
# t_avg: number of neighbors in time dimension (both sides)
# h_avg: number of neighbors in range dimension (both sides)
# span: loess span
# width_thres: minimum peak width [m/s]
# prom_thres: minimum peak prominence in dBZ

#pTB.load_limrad_spec('data/20181216-1210-1215_LIMRAD94_spectra.nc', load_to_ram=True)
#pTB.load_limrad_spec('data/20181216-1510-1515_LIMRAD94_spectra.nc', load_to_ram=True)
#pTB.load_limrad_spec('data/20190223-1440-1500_LIMRAD94_spectra.nc', load_to_ram=True)
#pTB.load('data/210319_140002_P05_ZEN.LV0_rpgpy.NC', load_to_ram=True)
#pTB.load('data/rpgpy_limrad_new/190911_030001_P05_ZEN.LV0.NC', load_to_ram=True)
#pTB.load('data/190911_030001_P05_ZEN.LV0.rpgpy.NC', load_to_ram=True)

# with the binary reader
#pTB.load('data/190911_030001_P05_ZEN.LV0', load_to_ram=True)
#pTB.load('data/190313_080000_P05_ZEN.LV0', load_to_ram=True)
#pTB.assemble_time_height('output/', fname_system=True)

pTB = peakTree.peakTreeBuffer(system='limrad_peako')
pTB.load('data/210319_140002_P05_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
