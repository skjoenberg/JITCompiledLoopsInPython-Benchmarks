import benchpress

executable = "quasicrystal_dw"
sizes = ['5*37*1000*100','5*37*1000*250','5*37*1000*500','5*37*1000*750','5*37*10*1000']
args = [{'label': executable + ' ' + size + ' with dw',
         'cmd': 'python -m bohrium ' + executable + '.py --size=' + size,
         'env': {}}
        for size in sizes] + \
        [{'label': executable + ' ' + size + ' without dw',
          'cmd': 'python -m bohrium ' + executable + '.py --size=' + size + ' --no-do_while',
          'env': {}}
        for size in sizes]

benchpress.benchpress.create_suite(args, './' + executable + '.json')
