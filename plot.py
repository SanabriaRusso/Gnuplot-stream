import subprocess
import threading
import time
import os
import math

"""Example of feedgnuplot"""
class myGenThread (threading.Thread):
    """Generating data"""
    def __init__(self, filename, limit, sleep_time=1, name="GenThread"):
        threading.Thread.__init__(self)
        self.name = name
        self.filename = filename
        self.range = range(0, limit)
        self.sleep_time = sleep_time
    
    def run(self):
        """This function is called by myGenThread.start()"""
        print("Starting %s" % self.name)
        genRun(self.filename, self.range, self.sleep_time)
        print("Finished %s" % self.name)

class myPlotThread (threading.Thread):
    """Plotting with feedgnuplot"""
    def __init__(self, filename, name="PlotThread"):
        threading.Thread.__init__(self)
        self.name = name
        self.filename = filename
    
    def run(self):
        """Calling the function to plot"""
        print("Starting %s" % self.name)
        plotRun(self.filename)

def genRun(filename, range_of_values, sleep_time=1):
    """Generate data to filename"""
    
    f = open(str(filename), 'w', 0)
    for n in range_of_values:
        f.write(str(n) + ' ' + str(math.sin(n)) + '\n')
        print("\tWriting: %s" % str(n))
        time.sleep(sleep_time)
    return

def plotRun(filename):
    """Calling an external script for firing feedgnuplot"""
    cmd = "while true; do tail " + str(filename) + " | awk '{print $1, $2}'; sleep 1; done | feedgnuplot --domain --lines --stream --xlen 10"
    subprocess.call([str(cmd)], shell=True)
        
        
def main():
    filename = "test.txt"
    limit = 200
    sleep_time = 0.1
    gen = myGenThread(filename, limit, sleep_time)
    plot = myPlotThread(filename)
    thread_list = []
    
    gen.start()
    plot.start()
    
    thread_list.append(gen)
    thread_list.append(plot)
    
    for t in thread_list:
        t.join()
    
    print "Just joined the main thread"
    
if __name__ == "__main__":
    main()

