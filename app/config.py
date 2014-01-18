import json

from util import set_timezone, log


conf = {
    'sys': {
        'debug': True,
        'port': 9020,
        'base_url': None,
        'secret_key': None,
        'timezone': 'America/New_York',
        'verbose': True,
        'timeout': 120,
        'max_tries': 3,
        'test-mode': False,
        'database': None
    },
}

def load_conf(filename):
    __conf__ = None
    with open('conf/'+filename) as f:
        r = f.read()
        __conf__ = json.loads(r)

    if __conf__ == None:
        raise Exception('load configuration %s failed' % filename)

    for key in __conf__:
        c = conf[key]
        _c = __conf__[key]
        for subkey in _c:
            c[subkey] = _c[subkey]

    required = {
        'sys': [ 'database' ]
    }
    for req in required:
        c = conf[req]
        for r in required[req]:
            if c[r] == None:
                raise ValueError('conf.%s.%s is None' % (req, r))

    check_test_mode()
    set_timezone(conf['sys']['timezone'])

def load_default_conf():
    if check_test_mode():
        load_conf('local.conf')
    else:
        load_conf('prod.conf')

def check_test_mode():
    try:
        with open('TEST') as f:
            pass
        log('TEST MODE')
        conf['test-mode'] = True
        return conf['test-mode']
    except:
        pass
    return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        load_conf(sys.argv[1])
        log(conf)
