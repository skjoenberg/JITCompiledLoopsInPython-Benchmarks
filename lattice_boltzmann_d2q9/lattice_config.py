import benchpress

executable = "lattice_dw"
sizes = ['100*100*50', '1000*1000*50', '2500*2500*50', '100*100*100','1000*1000*100','2500*2500*100']
args = [{'label': executable + ' ' + size + ' with dw',
         'cmd': 'python -m bohrium ' + executable + '.py --size=' + size,
         'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' without dw',
          'cmd': 'python -m bohrium ' + executable + '.py --size=' + size + ' --no-do_while',
          'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' with pure Numpy',
          'cmd': 'python lattice.py --size=' + size,
          'env': {}}
        for size in sizes]

benchpress.benchpress.create_suite(args, './' + executable + '.json')
