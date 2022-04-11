import random,sys

imported = True
try:
    import jieba
    import jieba.posseg as pseg
    jieba.setLogLevel(20)
except ImportError:
    imported = False


def chaos (x, y, chaosrate):
    if random.random() > chaosrate:
        return x
    if x in {'[', ']'}:
        return ''
    if x in {'，'}:
        return '…'
    if x in { '!', '！',}:
        return '‼‼‼'
    if x in { '。'}:
        return '❗'
    if len(x) > 1 and random.random() < 0.1:
        if random.random() < 0.2:
            return f'{x[0]}…{x}'
        else:
            return f'{x[0]}～{x}'
    if len(x) > 1 and random.random() < 0.4:
        return f'{x[0]}♥{x}'
    if y == 'n' and random.random() < 0.1:
        if random.random() < 0.4:
            x = '⭕️' * len(x)
        else:
            x = '～' * len(x)
        return f'…{x}'
    if x in { '\……n', '\♥n'}:
        return '\n'
    if x in { '…………'}:
        if random.random() < 0.3:
            return '……'
        else:
            if random.random() < 0.3:
                return '…'
            else:
                return '～'
    else:
        if y == 'n' and random.random() < 0.2:
            x = '⭕' * len(x)
        return f'…{x}'


def chs2yin(s, chaosrate =0.8):
    return ''.join(chaos (x, y, chaosrate) for x, y in pseg.cut(s))

print(chs2yin(sys.argv[1]))
