'''***************************
|Поиск совпадений по временам|
***************************'''

from obspy.core import UTCDateTime

def main():

    stationsName={"BKI":0,"KBG":0,"KBT":0,"KDT":0,"MKZ":0} # Названия станций
    dictOfActs={} # Словарь в который будем записывать события и считать совпадения

    '''*****************************************************
    |Читаем поочередной файлы и записываем время в словарь,|
    |если оно присутствует, то к значению ключа прибавляем |
    |единичку.                                             |
    *****************************************************'''
    for name in stationsName:
        f=open(f"tectsActions({name}).txt", 'r')
        for line in f:
            if (dictOfActs.get(line[0:27])==None):
                dictOfActs[line[0:27]]=1
            else:
                dictOfActs[line[0:27]]+=1

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