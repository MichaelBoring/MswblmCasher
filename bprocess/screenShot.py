#-*-coding:utf-8-*-
__author__ = 'Administrator'
import time
import traceback
import threading
import config
import dao.insiderinfoDao as insiderinfoDao
from PIL import ImageGrab
from PIL import Image
import win32com.client as win32com

class ScreenShot(threading.Thread):
    def __init__(self, t_name, queue=config.cash):
        threading.Thread.__init__(self, name=t_name)
        self.chmap = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'x': 10,
            'X': 10
        }
        self.queue = queue
        self._sysdb = config.sysdb
        self._insiderdb = config.insiderDNS
        self._insiderinfoDao = insiderinfoDao.insiderinfoDao()
        self.insiderNum = ''
        self.count = time.time()
        self.history = {}

    def verify(self, shenfenzheng17):
        x = shenfenzheng17[17]
        shenfenzheng17 = shenfenzheng17[0:17]

        def haoma_validate(shenfenzheng17):
            if type(shenfenzheng17) in [str, list,tuple] and len(shenfenzheng17) == 17:
                return True
        if haoma_validate(shenfenzheng17):
            if type(shenfenzheng17) == str:
                seq = map(int, shenfenzheng17)
            elif type(shenfenzheng17) in [list, tuple]:
                seq = shenfenzheng17
            t = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            s = sum(map(lambda x: x[0] * x[1], zip(t, map(int, seq))))
            b = s % 11
            bd = {
                0: '1',
                1: '0',
                2: 'x',
                3: '9',
                4: '8',
                5: '7',
                6: '6',
                7: '5',
                8: '4',
                9: '3',
                10: '2'
            }
            if bd[b] == 'x' and x == '0':
                return True
            return bd[b] == x

    def run(self):
        while True:
            try:
                insiderNum = ''
                box = config.area
                im = ImageGrab.grab(box)
                tx = 255
                ty = 104
                a = [243, 160, 209, 233, 269, 229, 242, 127, 255, 284]
                for m in range(18):
                    total = 0
                    for n in range(8):
                        sum = 0
                        for l in range(5):
                            x = m * 6 + l
                            if im.getpixel((x + tx - 107, n + ty - 8)) == config.color:
                                sum += (l + 1) * (n + 1)
                        total += sum
                    if total in a:
                        insiderNum = insiderNum + str(a.index(total))
                    else:
                        insiderNum = ''
                        break
                if m != 17:
                    for m in range(20):
                        total = 0
                        for n in range(8):
                            sum = 0
                            for l in range(5):
                                x = m * 6 + l
                                if im.getpixel((x, n)) == config.color:
                                    sum += (l + 1) * (n + 1)
                                    continue
                            total += sum

                        if total in a:
                            insiderNum = insiderNum + str(a.index(total))
                            continue
                        if m not in (18, 19):
                            insiderNum = ''
                            break
                length = len(insiderNum)
                if (length == 18 or length == 20) and self.verify(insiderNum[-18:]):
                    if self.history.has_key(insiderNum) and time.time() - self.history[insiderNum] < 120:
                        self.history[insiderNum] = time.time()
                        continue
                    d = {}
                    d['InsiderNumber'] = insiderNum
                    d['type'] = 'cash'
                    if d:
                        self.history[insiderNum] = time.time()
                        if len(self.history) > 4:
                            self.history.pop(min(self.history.items(),key=lambda x: x[1])[0])
                        config.cash.put(d)
                        self.insiderNum = insiderNum
                        d = {}
            except BaseException:
                config.logger.error(traceback.format_exc())
            finally:
                time.sleep(0.5)

    def analysis_cash(self, record):
        pass


if __name__ == '__main__':
    temp = ScreenShot()
    print temp.verify('51382119910714803x')
