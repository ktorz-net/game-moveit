import time

# Attributes

class _:
    doSleep= False

def sleep( dur= 0.33):
    if _.doSleep :
        time.sleep(dur)
