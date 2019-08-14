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

DEBUG = 1

class PandaController(BaseController):

    def __init__(self):
        super(PandaController, self).__init__()
        self.t_last = -1
        self.iteration = 0
        #Initialize idle duration while in steady state
        self.filter_old = -1
        #Controller parameters
        self.k = 0.14
        self.w = 300000.0/8. #Units??? (it should be Mbps)
        self.Q = 40 #seconds
        self.beta = 0.2
        self.alpha = 0.2 #Ewma filter
        self.x_hat_last = 0
        self.eps = 0.15
        self.T_old = 0
	self.algo = 'panda'

    def __repr__(self):
        return '<PandaController-%d>' %id(self)

    def calcControlAction(self):
        video_rates = self.feedback['rates']
        T_tilde = self.feedback['last_download_time']
        tau = self.feedback['fragment_duration']
        x_tilde = self.feedback['cur_rate'] * self.feedback['fragment_duration'] / T_tilde #bandwidth estimate sample on the last downloaded segment
        T_hat_old = self.getIdleDuration()
        #Actual inter-request time
        T = max(T_hat_old, T_tilde)
        self.T_old = T
        k = self.k
        w = self.w   #in B/s 
        beta = self.beta

        x_hat = max(0, self.x_hat_last + T * k * (w - max(0, self.x_hat_last - x_tilde)))
         
        self.x_hat_last = x_hat
        control_action = self.__ewma_filter(x_hat)

        r = self.quantizeSpecialRate(control_action)
        B = self.feedback['queued_time']

        T_hat = r * float(tau) / control_action + beta * ( float(B) - float(self.Q) )
        self.setIdleDuration(T_hat-T_tilde)
        debug(DEBUG, "%s calcControlAction: ca: %s/s r: %s/s x_tilde: %s/s x_hat: %s/s T_tilde: %.2f T_hat: %.2f T: %.2f", self, 
            format_bytes(control_action), format_bytes(r), format_bytes(x_tilde), format_bytes(x_hat), T_tilde, T_hat, T)
        return r

    def isBuffering(self):
        return self.feedback['queued_time'] < self.Q

    def onPaused(self):
        debug(DEBUG, '%s onPaused called. Steady state is false',self);
        self.steady_state = False	

    def __levelLessThanRate(self, rate):
        vr = self.feedback['rates']
        l = 0
        for i in range(0,len(vr)):
            if rate >= vr[i]:
                l = i
        return l
        
    def quantizeSpecialRate(self,rate):
        video_rates = self.feedback['rates']
        cur = self.feedback['cur_rate']
        #D_up = self.w + self.eps*rate
        #D_down = self.w
        D_up = self.eps*rate
        D_down = 0

        r_up = video_rates[self.__levelLessThanRate(rate - D_up)]
        r_down = video_rates[self.__levelLessThanRate(rate - D_down)]
        new_level = 0
        if cur < r_up:
            new_level = r_up
        elif r_up <= cur and cur <= r_down:
            new_level = cur
        else:
            new_level = r_down
        debug(DEBUG, "%s quantizeRate: rate: %s/s D_up: %s/s D_down: %s/s r_up: %s/s r_down: %s/s new_level_rate: %s/s", self, 
            format_bytes(rate), format_bytes(D_up), format_bytes(D_down), format_bytes(r_up), format_bytes(r_down), format_bytes(new_level))
        debug(DEBUG, "%s quantizeRate: rates: %s", self, video_rates)
        return new_level    

    def __ewma_filter(self, x_hat):
        #First time called
        if self.filter_old < 0:
            self.filter_old = x_hat
            return x_hat
        #T = self.feedback['last_download_time']
        T = self.T_old
        y_old = self.filter_old
        y = y_old - T * self.alpha * ( y_old - x_hat )
        self.filter_old = y
        return y
