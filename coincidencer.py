'''***************************
|Поиск совпадений по временам|
***************************'''

from obspy.core import UTCDateTime

def main():

    stationsName={"BKI":0,"KBG":0,"KBT":0,"KDT":0,"MKZ":0} # Названия станций
    dictOfActs={} # Словарь в который будем записывать события и считать совпадения

    listOfLists=[[],[],[],[],[]]
    i=0
    for name in stationsName:
        f=open(f"tectsActions({name}).txt", "r")
        for line in f:
            listOfLists[i].append(line[0:27])
        i+=1
    
    i=1
    for listOfTimes in listOfLists:
        for time in listOfTimes:
            if (dictOfActs.get(time)==None):
                dictOfActs[time]=1
            else:
                dictOfActs[time]=dictOfActs[time]+1
        i+=1

    '''******************************************
    Учитывая кол-во совпадений выписываем все в |
    отдельный файлик.                           |
    ******************************************'''
    f=open("tectActsCoins.txt",'w+')
    for line in dictOfActs:
        if (dictOfActs[line]>9):
            f.write(f"{line} | {dictOfActs[line]}\n")
    f.close()

main()