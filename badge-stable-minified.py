import math
import time

from vectorscope import Vectorscope

def draw(v):
    
    ## To animate, you need to clear v.wave.outBuffer_ready and wait for it to go true
    ## Each output buffer frame has 256 samples, so takes ~8.5 ms at 30 kHz

    while(True):

        ramp = range(-2**15, 2**15, 2**8)
        
        v.wave.packX(ramp)
        
        v.wave.outBuffer_ready = False
        
        for i in range(4000):
            
            sine = [int(math.sin((50*i)+2*x*math.pi/256)*16_000) for x in range(256)]
            
            while not v.wave.outBuffer_ready:
                pass
            
            time.sleep(0.015)
            
            v.wave.packY(sine)
            
            v.wave.outBuffer_ready = False

if __name__ == "__main__":

    v = Vectorscope()
    
    draw(v)
    
    v.deinit() ## if you don't do this you'll see `OSError: 16` in thonny output (must disconnect and reconnect the device)