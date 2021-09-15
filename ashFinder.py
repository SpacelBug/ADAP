'''*******************************************
|Скрипт должен выделять пепловые выбросы     | 
|(явл. лишь частью ADAP)                     |
*******************************************'''

import cmath 
import time
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
def ash_finder(name):

	st=pass_filter(read(f'mseeds/20210825-00-00-00({name}).msd'))

	listOfAshActs=[] # Словарик для тектонических событий

	ampId=0 # id текущего значения амплитуды
	ampOldId=-1 # id предыдущего значения амплитуды

	logger.info(f"Start {name} cycle")
	for amp in st[0].data:

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

				if (Fi>stationsFiRanges[name][0])and(Fi<stationsFiRanges[name][1]):

                    
					listOfAshActs.append(str(st[0].stats.starttime+ampId/st[0].stats.sampling_rate))

		ampId+=1
		ampOldId+=1

	logger.info(f"Lenght listOfAshActs for {name} = {len(listOfAshActs)}")
	logger.info(f"End {name} cycle")

	return(listOfAshActs)

def main():

	listOfAshs=[]

	logger.info('Prog Started')

	stationsNames={"BKI":0,"KBG":1,"KBT":2,"KDT":3,"MKZ":4} # Листик для записи потоков
    stationsFiRanges={"BKI":[,],"KBG":[,],"KBT":[,],"KDT":[,],"MKZ":[,]} # Хранит диапозоны в которых должен лежать Fi
    heightOfVolcanos={"BKI":,"KBG":,"KBT":,"KDT":,"MKZ":}

	threads=[] 

	for name in stationsNames:

		listOfAshs=(threads.append(Thread(target=tect_finder, args=(name,stationsFiRanges,))))
		logging.info(f'Treads list = {threads}')
		threads[stationsNames[name]].start()

	for name in stationsNames:
		threads[stationsNames[name]].join()


main()