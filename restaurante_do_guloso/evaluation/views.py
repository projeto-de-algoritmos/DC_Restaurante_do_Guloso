from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from copy import deepcopy
import csv

class receita:
    def __init__(self, nota, nome):
        self.nota = nota
        self.nome = nome

    def __repr__(self):
        return self.nome + ' --> ' + str(self.nota)

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
        return
    
    middle = (left + right) // 2
    merge_sort(cardapio, left, middle, tipo)
    merge_sort(cardapio, middle + 1, right, tipo)
    merge(cardapio, left, middle, right, tipo)

def read_csv(cardapio):
    with open('./evaluation/recipes.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            cardapio.append(receita(len(row['Rating']), row['Name']))

def menu(request):
    # ler csv
    cardapio = []
    read_csv(cardapio)
    # ordenar (avaliação, nome) [mergesort]
    merge_sort(cardapio, 0, len(cardapio) - 1, 1)
    # receber recomendação
    return HttpResponse(f"{cardapio}")
