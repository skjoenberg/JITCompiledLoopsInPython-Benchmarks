# -*- coding: utf-8 -*-
from benchpress import util
import numpy as np

def main():
    B = util.Benchmark()

    k       = B.size[0] # number of plane waves
    stripes = B.size[1] # number of stripes per wave
    N       = B.size[2] # image size in pixels
    ite     = B.size[3] # iterations

    phases = np.array([i * (2*np.pi/(ite)) for i in range(ite)])


    image   = np.empty((N, N), dtype=B.dtype)
    d       = np.arange(-N/2, N/2, dtype=B.dtype)

    xv, yv = np.meshgrid(d, d)
    theta  = np.arctan2(yv, xv)
    r      = np.log(np.sqrt(xv*xv + yv*yv))
    r[np.isinf(r) == True] = 0

    arr = np.array([i*np.pi/k for i in range(k)])
    tcos   = theta * np.cos(arr)[:, np.newaxis, np.newaxis]
    rsin   = r * np.sin(arr)[:, np.newaxis, np.newaxis]

    inner  = (tcos - rsin) * stripes

    cinner = np.cos(inner)
    sinner = np.sin(inner)

    B.start()

    def loop_body(phases, image):
        i = get_iterator()
        phase = phases[i]
        image[:] = np.sum(cinner * np.cos(phase) - sinner * np.sin(phase), axis=0) + k

    B.do_while(loop_body, len(phases), phases, image)

    B.stop()
    B.pprint()

    if B.outputfn:
        B.tofile(B.outputfn, {'res': image})

    if B.verbose:
        print(image)


if __name__ == "__main__":
    main()
