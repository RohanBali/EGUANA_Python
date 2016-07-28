# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 14:51:18 2016

@author: rohanbali
"""

from enum import Enum

class InputType(Enum):
    twoDEma = 1
    threeDEma = 2

class FilterType(Enum):
    speech3D = 1
    swallow3D = 2
    speech2D = 3
    swallow2D = 4
    
    