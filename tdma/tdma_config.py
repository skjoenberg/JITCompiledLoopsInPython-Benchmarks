import benchpress

executable = "tdma_dw"
sizes = ['10000*100','100000*100','100000*100',
         '1000*1000','10000*1000','10000*1000']
args = [{'label': executable + ' ' + size + ' with dw',
         'cmd': 'python -m bohrium ' + executable + '.py --size=' + size,
         'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' without dw',
          'cmd': 'python -m bohrium ' + executable + '.py --size=' + size + ' --no-do_while',
          'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' with pure Numpy',
          'cmd': 'python tdma.py --size=' + size,
          'env': {}}
        for size in sizes]

benchpress.benchpress.create_suite(args, './' + executable + '.json')
