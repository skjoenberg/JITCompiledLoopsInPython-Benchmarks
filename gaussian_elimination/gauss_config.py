import benchpress

executable = "gauss_dw"
sizes = ['100*100','250*250','500*500','1000*1000', '2500*2500']
args = [{'label': executable + ' ' + size + ' with dw',
         'cmd': 'python -m bohrium ' + executable + '.py --size=' + size,
         'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' without dw',
          'cmd': 'OMP_NUM_THREAD=1 python -m bohrium ' + executable + '.py --size=' + size + ' --no-do_while',
          'env': {}}
        for size in sizes]

benchpress.benchpress.create_suite(args, './' + executable + '.json')
