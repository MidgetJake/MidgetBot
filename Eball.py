from random import randrange

def eBall(x):
    return {
        0: 'I would rather not answer that...',
        1: 'It\'s not looking likely...',
        2: 'It\'s looking quite likely!',
        3: 'Look forward to it!',
        4: 'You don\'t understand...',
        5: 'Don\'t count on it',
        6: 'The future doesn\'t look bright',
        7: 'The future looks bright',
        8: 'YES!',
        9: 'Yes',
        10: 'NO!',
        11: 'No',
        12: 'It\'s a 50/50 chance',
        13: 'The chances are as high as you believe!',
        14: 'The chances are about as good as the quality of the code I am written with',
        15: '...'
    }[x]