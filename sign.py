import hashlib


def get_md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def sign(params):
    sorted_params = sorted(params.items(), key=lambda d: d[0])
    strData = ''
    for item in sorted_params:
        if str(item[0]) != 'signCode':
            strData = strData + str(item[0]) + str(item[1])
    raw = "CB5674****5D4F5" + strData + "CB5674****5D4F5"
    raw = raw.upper()
    print('raw---->%s' % raw)
    return get_md5(raw.encode('utf-8'))


params = {
    'client': '2.4.0',
    'id': '102690880',
    'fund': '1000'
}

print(sign(params))

# sign=e162fb5a545bd658333b2080a446b792
