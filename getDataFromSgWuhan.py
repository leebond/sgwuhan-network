#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 16:09:24 2020

@author: david
"""

import requests
import pickle as pkl

sgwuhan_api = 'https://sgwuhan.xose.net/api/'
data = requests.get(sgwuhan_api)

data_dict = dict(data.json())

with open('./data/sgwuhandata.pkl', 'wb') as f:
    pkl.dump(data_dict, f)