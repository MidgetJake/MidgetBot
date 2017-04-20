def cmdChecker(msg):
    if msg[0] == '!streamcfg':
        try:
            test = msg[1]
        except:
            return ('```Correct usage:\n'
                    '==============\n\n'
                    '!streamcfg [show/reset/ytGaming/imgThumb/mention/cooldown]\n'
                    '  - ytGaming [true/false]\n'
                    '  - imgThumb [true/false]\n'
                    '  - mention  [everyone/here/none]\n'
                    '  - cooldown [5-60]\n'
                    '```')
        try:
            if msg[1] in ['mention', 'ytGaming', 'imgThumb', 'cooldown']:
                test = msg[2]
                if msg[1] == 'cooldown':
                    try:
                        r = int(float(msg[2]))
                    except ValueError:
                        return ('```Correct usage:\n'
                                '==============\n'
                                '!streamcfg cooldown [5-60]\n'
                                '```')
        except:
            if msg[1] in ['ytGaming', 'imgThumb']:
                return ('```Correct usage:\n'
                        '==============\n'
                        '!streamcfg ' + msg[1] + ' [true/false]\n'
                        '```')
            elif msg[1] == 'mention':
                return ('```Correct usage:\n'
                        '==============\n'
                        '!streamcfg mention [everyone/here/none]\n'
                        '```')
            else:
                return ('```Correct usage:\n'
                        '==============\n'
                        '!streamcfg cooldown [5-60]\n'
                        '```')
    return False
