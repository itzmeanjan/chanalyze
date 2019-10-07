#!/usr/bin/python3

from os.path import abspath, dirname, exists
from os import mkdir
try:
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter
    from model.chat import Chat
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


# checks whether directory of this path already exists or not.
# if not, creates that directory
def directoryBuilder(targetPath: str):
    dirName = dirname(abspath(targetPath))
    if not exists(dirName):
        mkdir(dirName)


# shades last half of characters of Contact by `*`, for sake of privacy
def shadeContactName(name: str) -> str:
    return name[:-(len(name)//2)]+'*'*(len(name)//2)


def plotContributionInChatByUser(chat: Chat, targetPath: str, title: str) -> bool:
    try:
        directoryBuilder(targetPath)
        y = sorted([i.name for i in chat.users],
                   key=lambda e: len(chat.getUser(e).messages))
        y_pos = range(len(y))
        x = [len(chat.getUser(i).messages)/chat.messageCount*100 for i in y]
        y = [shadeContactName(i) for i in y]
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'color': '#000000',
                'weight': 'normal',
                'size': 14
            }
            plt.figure(figsize=(24, 12), dpi=100)
            plt.xlim((0, 100))
            plt.gca().xaxis.set_major_locator(MultipleLocator(10))
            plt.gca().xaxis.set_major_formatter(PercentFormatter())
            plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
            plt.barh(y_pos, x, align='center',
                     color='steelblue', lw=1.6)
            plt.gca().yaxis.set_ticks(y_pos)
            plt.gca().yaxis.set_ticklabels(y)
            plt.xlabel('Percentage of Participation in Chat',
                       fontdict=font, labelpad=16)
            plt.title(title,
                      fontdict=font, pad=16)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight', pad_inches=.5)
            plt.close()
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
