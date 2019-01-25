import time

class Timer():
    def __init__(self, interval,func):
        self.interval=interval
        self.func=func

    def run(self):
        t = int(time.time())
        self.func()
        while True:
            if int(time.time())<t+self.interval:
                time.sleep(0.5)
                # pass
            else:
                t=int(time.time())
                self.func()

def work1():
    print('work 1')
def work2():
    print('work 2')

if __name__=='__main__':
    timer1=Timer(10,work1)
    timer2=Timer(20,work2)
    timer1.run()
    timer2.run()