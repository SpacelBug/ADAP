'''*******************************************
|Скрипт должен выделять пепловые выбросы     | 
|(явл. лишь частью ADAP)                     |
*******************************************'''

import cmath 
import time
import os
import logging 
from threading import Thread


logger = logging.getLogger("ashFinder.py")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler(f"ashFinder.log")

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

listOfAshesActs=[] # Словарик для тектонических событий

def ash_finder(name, stationsFiRanges, heightOfVolcanos, Coefficient):

	st=pass_filter(read(f'mseedsForAshes/20210825-00-00-00({name}).msd'))

	

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
				logging.info(f'Fi={Fi}, K={Coefficient}, amp={amp}, I={dictOfI[0]}')

				if (Fi>stationsFiRanges[0])and(Fi<stationsFiRanges[1]):

					H=Coefficient*Fi*abs(amp)*(dictOfI[0]-1)

					if (H>heightOfVolcanos):

						listOfAshesActs.append(f'{(st[0].stats.starttime+ampId/st[0].stats.sampling_rate)} | {H}')

		ampId+=1
		ampOldId+=1

	logger.info(f"Lenght listOfAshActs for {name} = {len(listOfAshesActs)}")
	logger.info(f"End {name} cycle")

	return(listOfAshesActs)

def main():

	listOfAshes=[]

	logger.info('Prog Started')

	stationsNames={"SRK":0} # Листик для записи потоков
	stationsFiRanges={"SRK":[-1.1,1.333]} # Хранит диапозоны в которых должен лежать Fi
	heightOfVolcanos={"SRK":3307} # Высоты вулканов
	dictOfCoefficients={"SRK":1.333} # Коэфициенты для расета высоты

	threads=[] 

	for name in stationsNames:

		listOfAshes.append(threads.append(Thread(target=ash_finder, args=(name,stationsFiRanges[name],heightOfVolcanos[name],dictOfCoefficients[name],))))
		threads[stationsNames[name]].start()

	for name in stationsNames:
		threads[stationsNames[name]].join()

	f=open('ashActions.txt','w+')
	for line in listOfAshesActs:
		f.write(f'{line}\n')
	f.close()

main()