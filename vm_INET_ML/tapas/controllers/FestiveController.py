#!/usr/bin/env python
# -*- Mode: Python -*-
# -*- encoding: utf-8 -*-
# Copyright (c) Giuseppe Cofano <g.cofano87@gmail.com>

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE" in the source distribution for more information.
import os, sys
#from numpy import numarray
import numpy
import time
from utils_py.util import debug, format_bytes, CircularBuffer
from BaseController import BaseController
import random

DEBUG = 1
   
class FestiveController(BaseController):

    def __init__(self):
        super(FestiveController, self).__init__()
        self.horizon = 10
        self.bwe_vec = CircularBuffer(self.horizon) 
        self.switches = CircularBuffer(self.horizon)
        self.iteration = 0
        self.target_buf = 40 # seconds
        self.alpha = 12

    def __repr__(self):
        return '<FestiveController-%d>' %id(self)

    def calcControlAction(self):
        self.iteration += 1
        self.bwe_vec.add(self.feedback['bwe'])
       
        level = self.feedback['cur_rate']

        def __harmonic_mean(v):
            '''Computes the harmonic mean of vector v'''
            x = numpy.array(v)
            debug(DEBUG+1, "%s __harmonic_mean: Bwe vect: %s", self, str(x))
            m =  1.0/(sum(1.0/x)/len(x))
            debug(DEBUG, "%s__harmonic_mean: Harmonic mean: %s/s", self, format_bytes(m))
            return m
        w = __harmonic_mean(self.bwe_vec.getBuffer())
        debug(DEBUG, "%s calcControlAction: iteration %d", self, self.iteration)
        if self.iteration >= self.horizon:
            q = self.feedback['queued_time']
            delta = self.feedback['fragment_duration']

            randbuf = random.uniform(self.target_buf - delta, self.target_buf + delta) 
            
            b_ref = self.__evalRefLevel(w)
            b_cur = self.feedback['cur_rate']
            n = sum(self.switches.getBuffer())

            debug(DEBUG, "%s q: %.2f randbuf: %.2f b_ref: %.2f b_cur: %s/s n: %d", self, q, randbuf, b_ref, format_bytes(b_cur), n)
            if self.__evalScore(b_ref, b_ref, w, n) < self.__evalScore(b_cur, b_ref, w,n):
                self.switches.add(1)
                level = b_ref + 1000.0
            else:
                self.switches.add(0)
                level = b_cur + 1000.0

            #Randomized scheduling
            if q < randbuf:
                self.setIdleDuration(0.0)
            else:
                self.setIdleDuration(q - randbuf)
        return level

    def __evalScore(self, b, b_ref, w, n):
        efficiency = abs(b/min(w, b_ref) - 1)

        if b == b_ref:
            stability = 2**n + 1
        else:
            stability = 2**n
        
        return stability + self.alpha * efficiency

    def __evalRefLevel(self, bwe_filt):
        cur = self.feedback['cur_rate']
        cur_idx = self.feedback['level']
        new_idx = cur_idx
        
        video_rates = self.feedback['rates']

        debug(DEBUG, "%s __evalRefLevel: vrates: %s", self, str(video_rates))
        if cur > 0.85*bwe_filt:
            new_idx = cur_idx - 1
        else:
            for i in range(0,len(video_rates) - 1):
                if bwe_filt >= video_rates[i]:
                    debug(DEBUG, "%s __evalRefLevel: Bwe: %s/s vrate: %s/s", self, format_bytes(bwe_filt), format_bytes(video_rates[i]))
                    new_idx = i
        
        new_idx = min(max(new_idx,0), len(video_rates) -1)
        debug(DEBUG, "%s __evalRefLevel: Cur_idx: %d new_idx: %d", self, cur_idx, new_idx)
        return video_rates[new_idx] 
