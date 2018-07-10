from __future__ import print_function
from benchpress import util
import bohrium as np

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
    def loop_body(cp, dp):
        i = get_iterator(1)
        m = b[...,i] - cp[...,i-1] * a[...,i]
        fxa = 1.0 / m
        cp[...,i] = c[...,i] * fxa
        dp[...,i] = (d[...,i]-dp[...,i-1]*a[...,i]) * fxa
    B.do_while(loop_body, n-1, cp, dp)
    x[...,n-1] = dp[...,n-1]
    def loop_body(x):
        i = get_iterator()
        x[...,n-2-i] = dp[...,n-2-i] - cp[...,n-2-i]*x[...,n-1-i]
    B.do_while(loop_body, n-1, x)
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
