from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from copy import copy
import csv
from random import shuffle

class receita:
    def __init__(self, nota, nome, imagem):
        self.nota = nota
        self.nome = nome
        self.imagem = imagem

    # def __repr__(self):
    #     #  return self.nome + ' --> ' + str(self.nota)
    #     return self.imagem

# tipo = 0 (avaliação), tipo = 1 (nome)
def lesseq(i, j, tipo):
    if tipo == 0 and i.nota > j.nota:
        return True
    elif tipo == 1 and i.nome.lower() < j.nome.lower():
        return True
    return False

def merge(cardapio, left, middle, right, tipo):
    tmp = []
    i, j = left, middle + 1

    while i <= middle and j <= right:
        if lesseq(cardapio[i], cardapio[j], tipo):
            tmp.append(cardapio[i])
            i += 1
        else:
            tmp.append(cardapio[j])
            j += 1

    while i <= middle:
        tmp.append(cardapio[i])
        i += 1
    
    while j <= right:
        tmp.append(cardapio[j])
        j += 1

    k = 0
    for i in range(left, right + 1):
        cardapio[i] = tmp[k]
        k += 1

def merge_sort(cardapio, left, right, tipo):
    if left >= right:
        return 0
    
    middle = (left + right) // 2
    merge_sort(cardapio, left, middle, tipo)
    merge_sort(cardapio, middle + 1, right, tipo)
    merge(cardapio, left, middle, right, tipo)

def read_csv(cardapio):
    with open('./evaluation/recipes.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row['Photo'] != '':
                cardapio.append(receita(len(row['Rating']), row['Name'], row['Photo']))
            #  cardapio.append(receita(len(row['Rating']), row['Name'], row['Photo']))

def menu(request):
    cardapio = []
    read_csv(cardapio)
    if request.GET.__contains__('nome'):
        merge_sort(cardapio, 0, len(cardapio) - 1, 1)
        return render(request, 'evaluation.html', {'evaluations': cardapio, 'qtd_evaluation': len(cardapio)})
    else:
        merge_sort(cardapio, 0, len(cardapio) - 1, 0)
        return render(request, 'evaluation.html', {'evaluations': cardapio, 'qtd_evaluation': len(cardapio)})

