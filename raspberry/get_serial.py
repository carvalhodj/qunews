def get_serial():
    cpu_serial = '00000000'

    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[18:26]
        f.close()
    except:
        cpu_serial = '00000000'

    return cpu_serial
