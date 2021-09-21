'''**********
|Отсеиватель|
**********'''

from obspy.core import UTCDateTime

def main():

    f = open("tectActsCoins.txt", 'r')

    dictOfActs={} # Дублирует словарь из файла
    times=[] # Список со всем временем
    weedOutTimes=[] # Отсеянный список

    for line in f:
        dictOfActs[line[0:28]]=line[31:32]
        t=UTCDateTime(line[0:28])
        times.append(t)

    f.close()

    starttime=times[0]  # Время начала события
    endtime=0  # Время конца события

    i=1 # Счетчик
    for time in times[1:]:
        if ((time-times[i-1])>60): # Если разница более 60с., то сохроняе промежуток
            endtime=times[i-1]
            weedOutTimes.append(f'{starttime}>|<{endtime}')
            starttime=time
        if (i==len(times)-1): # Условие для учета последней записи в списке
            endtime=times[i]
            weedOutTimes.append(f'{starttime}>|<{endtime}')
        i+=1

    print('              START TIME        >|          ENDTIME') # Красивость

    i=0 # Счетчик
    for time in weedOutTimes:
        print('{:0>3})'.format(i), f'{time}')
        i+=1

main()