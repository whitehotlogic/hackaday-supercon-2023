import math
import time

from vectorscope import Vectorscope
from random_walk import RW


""" spin square """
""" run doom



- start with 4 points -- not using perspective yet
- try moving the dots around







"""


def rotate_row_elements(matrix, row,by, right=True):
    if right:
        for i in range(by):
            matrix[row] = [matrix[row].pop(), matrix[row]]
    else:
        for i in range(by):
            matrix[row] = [matrix[row][1:], matrix[row][0]]

def rotate_col_elements(matrix, col,by, down=True):
    if down:
        temp = [matrix[j][col] for j in range(len(matrix))]
        
        for i in range(by):
            temp = [temp.pop(), *temp]
            
        for j in range(len(matrix)):
            matrix[j][col] = temp[j]
            
    else:
        
        temp = [matrix[j][col] for j in range(len(matrix))]
        for i in range(by):
            temp = temp[1:] + [temp[0]]
        
        for j in range(len(matrix)):
            matrix[j][col] = temp[j]        


def animated_buffer_example(v):
    ## To animate, you need to clear v.wave.outBuffer_ready and wait for it to go true
    ## Each output buffer frame has 256 samples, so takes ~8.5 ms at 30 kHz

    while(True):

        ramp = range(-2**15, 2**15, 2**8)
        v.wave.packX(ramp)
        
        v.wave.outBuffer_ready = False
        for i in range(200):  
            sine = [int(math.sin((50*i)+2*x*math.pi/256)*16_000) for x in range(256)]
            while not v.wave.outBuffer_ready:
                pass
            v.wave.packY(sine)
            v.wave.outBuffer_ready = False

        ## Any stuck pixels you see are a figment of your imagination.  :)
        ## Or a desperate call for a pull request.  Your call.






def minimal_example(v):
    ## Minimal example
    for i in range(200):
        v.wave.constantX(int(math.cos(i * math.pi / 180 * 5) * 10000))
        v.wave.constantY(int(math.sin(i * math.pi / 180 * 5)* 10000))
        time.sleep_ms(10)


def static_buffer_example(v):
    ## Example of more complicated, repetitive waveform
    ## v.wave has two buffers of 256 samples for putting sample-wise data into: 
    ## v.wave.outBufferX and outBufferY.  These are packed 16 bits each, LSB first
    ## To make your life easier, v.wave.packX() will put a list of 16-bit ints there for you

    ramp = range(-2**15, 2**15, 2**8)
    v.wave.packX(ramp)

    sine = [int(math.sin(2*x*math.pi/256)*16_000) for x in range(256)]
    v.wave.packY(sine)

    time.sleep_ms(1000)

    ## That discontinuity and wobble is real -- 
    ##  that's what happens when you try to push around a real DAC that's bandwidth-limited.


def animated_buffer_example(v):
    ## To animate, you need to clear v.wave.outBuffer_ready and wait for it to go true
    ## Each output buffer frame has 256 samples, so takes ~8.5 ms at 30 kHz

    while(True):

        ramp = range(-2**15, 2**15, 2**8)
        v.wave.packX(ramp)
        
        v.wave.outBuffer_ready = False
        for i in range(200):  
            sine = [int(math.sin((50*i)+2*x*math.pi/256)*16_000) for x in range(256)]
            while not v.wave.outBuffer_ready:
                pass
            v.wave.packY(sine)
            v.wave.outBuffer_ready = False

        ## Any stuck pixels you see are a figment of your imagination.  :)
        ## Or a desperate call for a pull request.  Your call.

    
    
def vos_main():
    import vos_state,vectoros,gc,vos_debug, asyncio
    from vos_debug import debug_print as debug
    vectoros.get_screen().idle()
    gc.collect()
    vos_state.gc_suspend=True
    asyncio.sleep(4)
    v = Vectorscope()
    minimal_example(v)
    await asyncio.sleep(5)
    static_buffer_example(v)
    await asyncio.sleep(5)
    animated_buffer_example(v)
    random_walk_example(v)
    debug(vos_debug.DEBUG_LEVEL_INFO,"Demo done, reboot!") 
    vectoros.reset()
    
    

if __name__ == "__main__":


    matrix = [
    [0 ,5, 2],   
    [7 ,8 ,4],
    [1, 6, 3]]
    rotate_col_elements(matrix, 1, 2)
    print(matrix)

    v = Vectorscope()
    #minimal_example(v)
    #static_buffer_example(v)
    animated_buffer_example(v)
    #random_walk_example(v)

    v.deinit()
    
    ## before you reload, you have to deinitialize all of the DMA
    ##  machines, else you get an error OS: 16