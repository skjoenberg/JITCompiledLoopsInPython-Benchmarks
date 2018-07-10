from __future__ import print_function
from benchpress import util
import numpy as np

import bohrium.linalg as la

def main():
    B = util.Benchmark()
    N = B.size[0]

    if B.inputfn:
        S = B.load_array()
    else:
        S = B.random_array((N, N))

    if B.dumpinput:
        B.dump_arrays("gauss", {'input':S})

    B.start()

    def loop_body(S):
        c = get_iterator(1)
        S[c:, c - 1:] -= (S[c:,c-1:c] / S[c-1:c, c-1:c]) * S[c-1:c,c-1:]

    B.do_while(loop_body, S.shape[0]-1, S)

    S /= np.diagonal(S)[:, None]

    R = S

    if util.Benchmark().bohrium:
        R.copy2numpy()

    B.stop()

    B.pprint()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

    if B.verbose:
        print (R)


if __name__ == "__main__":
    main()
