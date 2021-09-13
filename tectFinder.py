import cmath 
import time
from threading import Thread

from obspy import read
from obspy import Stream
from obspy import Trace
from obspy.core import UTCDateTime

def passFilter(st):

	st.resample(200)

	dictOFPassFilterValues={6:[0.75,1.5],7:[1,2],15:[0.1,18],13:[8,16],14:[12,18],}
	newTr=st[0]
	newTr.write('newSt.mseed')
	newSt=Stream()
	for i in dictOFPassFilterValues:
		newSt.append(read('newSt.mseed').filter('bandpass', freqmin=dictOFPassFilterValues[i][0], freqmax=dictOFPassFilterValues[i][1]))
	return(newSt)

def main():

	print(read("mseeds/20210825-00-00-00(MKZ).msd"))

main()