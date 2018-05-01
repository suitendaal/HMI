
class Gap(object):

    def __init__(self, begintime, endtime, isgap):
        self.begintime = begintime
        self.endtime = endtime
        self.isgap = isgap

    def getTimeToInter(self):
        return (self.begintime + self.endtime)/2

    def getDuration(self):
        return self.begintime - self.endtime
