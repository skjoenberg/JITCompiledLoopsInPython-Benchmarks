from __future__ import print_function
from benchpress import util
import numpy as np

import bohrium.linalg as la

def solve_tridiag(a, b, c, d, B):
    assert a.shape == b.shape and a.shape == c.shape and a.shape == d.shape
    #if not climate.is_bohrium:
    #    return lapack.dgtsv(a.flatten()[1:],b.flatten(),c.flatten()[:-1],d.flatten())[3].reshape(a.shape)

    n = a.shape[-1]
    x, cp, dp = np.zeros_like(a), np.zeros_like(a), np.zeros_like(a)

    # initialize c-prime and d-prime
    cp[...,0] = c[...,0]/b[...,0]
    dp[...,0] = d[...,0]/b[...,0]

    # solve for vectors c-prime and d-prime
    for i in xrange(1, n):
        m = b[...,i] - cp[...,i-1] * a[...,i]
        fxa = 1.0 / m
        cp[...,i] = c[...,i] * fxa
        dp[...,i] = (d[...,i]-dp[...,i-1]*a[...,i]) * fxa
        B.flush()
    x[...,n-1] = dp[...,n-1]
    for i in xrange(n-2, -1, -1):
        x[...,i] = dp[...,i] - cp[...,i]*x[...,i+1]
        B.flush()
    return x

def main():
    B = util.Benchmark()
    H = B.size[0]
    W = B.size[1]

    A1 = B.random_array((H, W))
    A2 = B.random_array((H, W))
    A3 = B.random_array((H, W))
    A4 = B.random_array((H, W))

    B.start()

    R = solve_tridiag(A1, A2, A3, A4, B)

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
