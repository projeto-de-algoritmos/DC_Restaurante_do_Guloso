from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from random import randint
import heapq as hp
import time

class motoboy:
    def __init__(self, inicio = 0, final = 86400, tamanhoMin = 600, tamanhoMax = 3600):
        self.inicio = inicio
        self.final = final
        self.tamanhoMin = tamanhoMin
        self.tamanhoMax = tamanhoMax
        self.qtd = 0
        # ex.: [(10:30, [a, c, e]), (7:00, [b])]
        self.compatibility = []

    def __convert(self, task):
        return (time.strftime('%H:%M', time.gmtime(task[0])), time.strftime('%H:%M', time.gmtime(task[1])))

    def convertTime(self):
        ret = {}
        for i in range(self.qtd):
            ret[i] = map(self.__convert, self.compatibility[i][1])
        return ret

heapTask = []

def addTask(motoboys, tasks):
    inicioTask = randint(motoboys.inicio, motoboys.final)
    tamanhoTask = randint(motoboys.tamanhoMin, motoboys.tamanhoMax)
    hp.heappush(tasks, (inicioTask, inicioTask + tamanhoTask))

def randomizeTasks(motoboys, tasks, qtd):
    for _ in range(qtd):
        addTask(motoboys, tasks)

def intervalPartitioning (motoboys, tasks):
    while tasks:
        task = hp.heappop(tasks)
        if motoboys.compatibility and motoboys.compatibility[0][0] <= task[0]:
            motoboys.compatibility[0][1].append(task)
            motoboys.compatibility[0] = (task[1], motoboys.compatibility[0][1])
            hp.heapify(motoboys.compatibility)
        else:
            motoboys.qtd += 1
            hp.heappush(motoboys.compatibility, (task[1], [task]))

def validateNumber (number):
    if number <= 0:
        raise Exception
    return number

def menu(request):
    global heapTask
    motoboys = motoboy()

    if request.GET.__contains__('plus'):
        addTask(motoboys, heapTask)
        tasks = heapTask.copy()
        intervalPartitioning(motoboys, tasks)
    elif request.GET.__contains__('qtd'):
        try:
            qtd = validateNumber(int(request.GET['qtd']))
            motoboys = motoboy()
            if request.GET['inicio'] != "":
                motoboys.inicio = validateNumber(int(request.GET['inicio']) * 3600)
            if request.GET['final'] != "":
                motoboys.final = validateNumber(int(request.GET['final']) * 3600)
            if request.GET['tamanhoMin'] != "":
                motoboys.tamanhoMin = validateNumber(int(request.GET['tamanhoMin']) * 60)
            if request.GET['tamanhoMax'] != "":
                motoboys.tamanhoMax = validateNumber(int(request.GET['tamanhoMax']) * 60)
            heapTask = []
            randomizeTasks(motoboys, heapTask, qtd)
            tasks = heapTask.copy()
            intervalPartitioning(motoboys, tasks)
        except:
            messages.error(request, 'Digite um valor maior ou igual a 0')
    return render(request, 'menu.html', {'motoboys': dict(motoboys.convertTime()), 'qtd_motoboys': motoboys.qtd, 'qtd_tasks': len(heapTask)})
