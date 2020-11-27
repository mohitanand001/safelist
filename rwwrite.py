import threading
import time

def safelist(mode="dirty"):

    if mode == "dirty":
        return DirtyList()
    elif mode == "safe_write":
        return SafeWriteList()
    elif mode == "safe_readwrite":
        return SafeReadWriteList()
    else:
        raise ValueError

class BaseSafeList:
    def __repr__(self):
        return "python list"

    def __init__(self):
        pass
    
    def modify(self, indx, val):
        return None

    def get(self, indx):
        return None

    def push(self, val):
        return None

class DirtyList(BaseSafeList):
    
    def __init__(self):
        self._lis = []

    def push(self, val):
        self._lis.append(val)

    def modify(self, indx, val):
        self._lis[indx] = val

    def get(self, indx):
        return self._lis[indx]

class SafeWriteList(BaseSafeList):

    def __init__(self):
        self._lis = []
        self.s_writer = threading.Semaphore()

    def push(self, val):
        self.s_writer.acquire()
        self._lis.append(val)
        self.s_writer.release()

    def modify(self, indx, val):
        self.s_writer.acquire()
        self._lis[indx] = val
        self.s_writer.release()

    def get(self, indx):
        return self._lis[indx]

class SafeReadWriteList(BaseSafeList):

    def __init__(self):
        self._lis = []
        self.readers = 0
        self.s_readers = threading.Semaphore()
        self.s_readerwriter = threading.Semaphore()
    
    def push(self, val):
        self.s_readerwriter.acquire()
        self._lis.append(val)
        self.s_readerwriter.release()

    def modify(self, indx, val):
        self.s_readerwriter.acquire()
        self._lis[indx] = val
        self.s_readerwriter.release()

    def get(self, indx):
        self.s_readers.acquire()
        self.readers +=1
        
        if (self.readers == 1):
            self.s_readerwriter.acquire()
        self.s_readers.release()

        val = self._lis[indx]

        self.s_readers.acquire()
        self.readers -=1

        if (self.readers == 0):
            self.s_readerwriter.release()
        
        self.s_readers.release()

        return val