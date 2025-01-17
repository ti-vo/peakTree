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
import gc

import logging
log = logging.getLogger('peakTree')
log.setLevel(logging.INFO)
#log.addHandler(logging.StreamHandler())

#pTB = peakTree.peakTreeBuffer(system='limrad_peako')

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
pTB = peakTree.peakTreeBuffer(system='limrad_punta')
pTB.load('data/190911_030001_P05_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

pTB = peakTree.peakTreeBuffer(system='limrad_punta')
pTB.load('data/190313_080000_P05_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

pTB = peakTree.peakTreeBuffer(system='limrad_peako')
pTB.load('data/210319_140002_P05_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

exit()

pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220220_020002_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220220_050003_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220221_020000_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()

pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220225_030002_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()
 
pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220302_120000_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()
 
pTB = peakTree.peakTreeBuffer(system='rpg94_eri')
pTB.load('data/rpg94_lacros/220226_080003_P02_ZEN.LV0', load_to_ram=True)
pTB.assemble_time_height('output/', fname_system=True)
del(pTB); gc.collect()
