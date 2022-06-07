# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:53:59 2021

@author: hoskim1
"""
import pandas as pd

answers = pd.DataFrame.from_dict({1:32,
                                  2:42,
                                  3:12,
                                  4:434,
                                  5:14,
                                  6:1235,
                                  7:12,
                                  8:124,
                                  9:69,
                                  10:51}.items())

answers.columns = ['Question','Answer']