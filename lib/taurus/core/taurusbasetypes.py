#!/usr/bin/env python
#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

'''
a misc collection of basic types
'''

from enums import AttrQuality
import time, datetime

class TaurusTimeVal(object):
    def __init__(self):
        self.tv_sec = 0
        self.tv_usec = 0
        self.tv_nsec = 0
    
    def __repr__(self):
        return "%s(tv_sec=%i, tv_usec=%i, tv_nsec=%i)"%(self.__class__.__name__, self.tv_sec, self.tv_usec, self.tv_nsec)
    
    def __float__(self):
        return self.totime()
    
    def totime(self):
        return self.tv_usec*1e-9 + self.tv_usec*1e-6 + self.tv_sec
    
    def todatetime(self):
        return datetime.datetime.fromtimestamp(self.totime())
    
    def isoformat(self):
        return todatetime().isoformat()
    
    @staticmethod
    def fromtimestamp(v):
        tv = TaurusTimeVal()
        tv.tv_sec = int(v)
        usec = (v - tv.tv_sec)*1000000
        tv.tv_usec = int(usec)
        tv.tv_nsec = int((usec - tv.tv_usec)*1000)
        return tv
    
    @staticmethod
    def fromdatetime(v):
        import time
        tv = TaurusTimeVal()
        tv.tv_sec = int(time.mktime(v.timetuple()))
        tv.tv_usec = v.microsecond
        tv.tv_nsec = 0 #datetime does not provide ns info
        return tv
    
    @staticmethod
    def now():
        return TaurusTimeVal.fromdatetime(datetime.datetime.now())    
         

class TaurusAttrValue(object):
    def __init__(self):
        self.value = None
        self.w_value = None
        self.time = None
        self.quality = AttrQuality.ATTR_VALID
        self.format = 0
        self.has_failed = False
        self.err_stack = None
        self.config = TaurusConfigValue()
        
    def __getattr__(self,name):
        return getattr(self.config, name)
    
    def __repr__(self):
        return "%s%s"%(self.__class__.__name__, repr(self.__dict__))
        #values = ", ".join(["%s=%s"%(m,repr(getattr(self,m))) for m in self.__dict__])
        #return "%s(%s)"%(self.__class__.__name__, values)

class TaurusConfigValue(object):
    def __init__(self):
        self.name = None
        self.writable = None
        self.data_format = None
        self.type = None
        self.max_dim = 1, 1
        self.label = None
        self.unit = None
        self.standard_unit = None
        self.display_unit= None
        self.format = None
        self.range = float('-inf'), float('inf')
        self.alarm = float('-inf'), float('inf')
        self.warning = float('-inf'), float('inf')
        self.disp_level = None
    def __repr__(self):
        return "%s%s"%(self.__class__.__name__, repr(self.__dict__))