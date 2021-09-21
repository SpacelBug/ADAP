# ADAP
---

Программа для автоматического выделения пепловых выбросов и расчёта их высоты по сейсмологическим данным

---

mseeds/... - хранит станции для выявления тектонических событий

tectFinder.py - отвечает за выявление тектонических событий 

ashFinder.py - отвечает за выделение пепловых выбросов

weed_out.py - скрипт который склеивает временные промежутки до 60с.

coincidencer.py - скрипт который ищет совпадение времени событий.

---

# Справочка по вычисляемым переменным

---

1) I - опр. возрастание или затухание сигнала в заданной частотной полосе.

    I=lg(An-1/An)

    An - амплитуда в n частотной полосе.

2) Fi - частоный индекс испльзуемый для выделения пеплового выброса (диапозон в котором он должен лежать вычесляется эмпирически для каждого вулкана).

    Fi=log10((A13+A14)/(A6+A7))

    An - амплитуда в n частотной полосе.

3) H - высота пеплового выброса.

    H=KFiAn(I-1)

    K-Коэфицент
    
    An – амплитуда в точке n сейсмического сигнала (15-я частотная полоса табл).
