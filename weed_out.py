'''**********
|Отсеиватель|
**********'''

from obspy.core import UTCDateTime

f = open("tectActsCoins.txt", 'r')
dictOfActs={}
times=[]
weedOutTimes=[]
for line in f:
	dictOfActs[line[0:28]]=line[31:32]
	t=UTCDateTime(line[0:28])
	times.append(t)

f.close()

starttime=times[0]
endtime=0

i=1
for time in times[1:]:
	if ((time-times[i-1])>60):
		endtime=times[i-1]
		weedOutTimes.append(f'{starttime}>|<{endtime}')
		starttime=time
	if (i==len(times)-1):
		endtime=times[i]
		weedOutTimes.append(f'{starttime}>|<{endtime}')
	i+=1

print('              START TIME        >|          ENDTIME')

i=0
for time in weedOutTimes:
	print('{:0>3})'.format(i), f'{time}')
	i+=1