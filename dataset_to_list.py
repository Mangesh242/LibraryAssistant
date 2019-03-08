#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 15:41:53 2019

@author: iamsdp
"""
import csv

lines = csv.reader(open(r'train_dataset.csv'))

dataset = list(lines)

print(dataset)