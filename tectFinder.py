'''*******************************************
|Скрипт должен выделять тектонические события| 
|(явл. лишь частью ADAP)                     |
*******************************************'''

import cmath 
import time
from threading import Thread
import os
import logging 

logger = logging.getLogger("tectFinder.py")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler(f"tectFinder.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

from obspy import read
from obspy import Stream
from obspy import Trace
from obspy.core import UTCDateTime

'''****************************
|Фильтрация сигнала по полосам|
****************************'''
def pass_filter(st):

	dictOFPassFilterValues={6:[0.75,1.5],7:[1,2],15:[0.1,18],13:[8,16],14:[12,18],}
	newTr=st[0]
	newSt=Stream().append(newTr)
	for i in dictOFPassFilterValues:
		newSt.append(newTr.copy().filter('bandpass', freqmin=dictOFPassFilterValues[i][0], freqmax=dictOFPassFilterValues[i][1]))
	return(newSt)

'''******************************
|Выделение тектонических событий|
******************************'''
def tect_finder(name):
	logger.info(f'For thread name = {name}')

	st=pass_filter(read(f'mseeds/20210825-00-00-00({name}).msd'))

	ampId=0 # id текущего значения амплитуды
	ampOldId=-1 # id предыдущего значения амплитуды

	logger.info(f"Start {name} cycle")
	for amp in st[0].data:

		dictOfTectActs={}

		dictOfI={0:0,3:0,2:0,1:0,4:0,5:0} # Словарь I где: 3=15 полоса; 2=7 полоса; 1=6 полоса, 4=13 полоса, 5=14 полоса.
		timeOfAction=0 # Время события

		counterTect={"BKI":0,"KBG":0,"KBT":0,"KDT":0,"MKZ":0} # Счетчик событий

		if abs(amp)>90:

			for I in dictOfI:

				if (ampOldId!=-1):
					if ((amp!=0)and(st[I].data[ampOldId]!=0)):
						dictOfI[I]=cmath.log(abs(st[I].data[ampOldId])/abs(st[I].data[ampId])).real
					else:
						dictOfI[I]=0
			
			if ((dictOfI[3]<0)and(dictOfI[1]<0)and(dictOfI[2]<0)):

				Fi=cmath.log10((dictOfI[4]+dictOfI[5])/(dictOfI[1]+dictOfI[2])).real

				if (Fi>0.5):

					timeOfAction=str(st[0].stats.starttime+ampId/st[0].stats.sampling_rate)

					if (dictOfTectActs.get(timeOfAction)==None):
						dictOfTectActs[timeOfAction]=1
					else:
						dictOfTectActs[timeOfAction]+=1

		ampId+=1
		ampOldId+=1

	logger.info(f"dictOfTectActs lenght = {len(dictOfTectActs)}")
	logger.info(f"End {name} cycle")

dictOfTectActs={} # Словарик для тектонических событий

def main():

	logger.info('Prog Started')

	stationsNames={"BKI":0,"KBG":1,"KBT":2,"KDT":3,"MKZ":4} # Листик для записи потоков
	threads=[] 

	for name in stationsNames:

		threads.append(Thread(target=tect_finder, args=(name,)))
		logging.info(f'Treads list = {threads}')
		threads[stationsNames[name]].start()

	for name in stationsNames:
		threads[stationsNames[name]].join()

	print(len(dictOfTectActs))

main()