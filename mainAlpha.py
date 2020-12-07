#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:59:38 2020

@author: Giulio Iannello
"""

    import json
    import argparse
    import toml
    import numpy as np
    from os.path import join
    import pandas as pd
    import datetime
    import time
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--params", help="Complete path to toml file containing parameters",
                        type=str, default='./parameters.toml')
    
    parser.add_argument("-i", "--input_data", help="Complete path to the file containing data (log)",
                        type=str, default='./file_di_test/Test-risposte date.json')
    
    parser.add_argument("-i1", "--input_data1", help="Complete path to the file containing data (utenti)",
                        type=str, default='./file_di_test/tabellaID.json')
    
    parser.add_argument("-o1", "--Data1", help="Complete path il file input_data.json", 
                        type=str, default='./PythonExport.xlsx')
    
    args = parser.parse_args()
    
    with open(args.params, 'r') as paramsFile:
        params = toml.loads(paramsFile.read())
        print(params)
    
    #Creo il DataFrame
    
    
    # legge la lista dei log in formato json e memorizzarla in una lista di liste
    f1 = open(join(params['input']['InDir'], params['input']['InFile']))
    fin = f1.read()
    data = json.loads(fin)[0]
    f1.close()
    
    # legge la tabella delle corrispondenze (utente, ID unico) già assegnate
    f1 = open(join(params['input']['InDir'], params['input']['IdFile']))
    fin = f1.read()
    d = json.loads(fin)
    start = time.perf_counter_ns()
    # legge la lista dei Quiz
    fin1=open(args.input_data,'r')
    text1=fin1.read()
    data1=json.loads(text1)[0]
    
    finI=open(args.input_data1,'r')
    textI=finI.read()
    dataI=json.loads(textI)

df=pd.DataFrame(data1, columns=['Cognome', 'Nome', ' ', 'INDB_MAT_2020',
                               '!Email', 'Esito Prova', 'Data In', 'Data Out', 'Time', 
                               'Voto', 'Domanda 2', 'Domanda 3',
                               'Domanda 4', 'Domanda 5', 'Domanda 6',
                               'Domanda 7', 'Domanda 8', 'Domanda 9',
                               'Domanda 10'])
DDN=dataI.keys()
DataT=list(DDN)
NC=dataI.values()
DataCripto=list(NC)
df1=pd.DataFrame(DataT, columns=['Nome',])
df2=pd.DataFrame(DataCripto, columns=['UC'])
df['Nome Cognome'] = df['Nome'] + ' ' + df['Cognome']
NomeC= df['Nome Cognome']
df1['UC']=df2['UC']

DataT1=list(NomeC)
#ESPORTARE NOME COGNOME IN LISTA MATCH CON DATAI ANONIMIZZIAMO L'OUTPUT CREIAMO
#DATA FRAME E METTIAMO NELLA COLONNA UC ED ELIMINIAMO LE COLONNE 0 1 20



# assegna un ID unico a ciascun nuovo utente (aggiornando la tabella)
# ed elimina il campo “utente coinvolto”
#cont = max([int(id) for id in d.values()]) + 1

for i in range(len(DataT1)):
    if  DataT1[i]  in dataI:
        dataI[DataT1[i]] = dataI.values()
        #cont += 1
    data1[i][1] = d[data1[i][1]]
    #data[i].pop(2)
    data1[i][2] = 'uc'















utenti=df['ID'].unique()
numero_utenti=df['ID'].unique().size
#Conto numero totale utenti

utenti=df['ID'].unique()
numero_utenti=df['ID'].unique().size

#Assegno indici corrispondenti agli ID degli utenti alle righe di df 

df.index=[df['ID']]

#Conto numero di log per utente (quindi il numero di eventi totali per utente)

numlog_utente=df['ID'].value_counts()
numlog_utente.index=utenti
  
#Creo lista di eventi, del numero di log per evento e conto gli eventi diversi

lista_eventi=list((df['Evento']))
numerolog_evento=df['Evento'].value_counts()
eventi_diversi=numerolog_evento.index


#Calcolo quanti log ci sono per ciascun giorno

dt= pd.to_datetime(df['Data/Ora'])
giorni= dt.dt.day
log_giorno= giorni.value_counts()

tabella_evento=[]
for user in utenti:
    tabella_evento.append((df.loc[user,'Evento'].value_counts()))


#Estraggo dal DataFrame la data del primo e dell'ultimo evento per ciascun utente

data_ultimo_ev=[]
data_primo_ev=[]

for utente in utenti:
    date_utente=df.loc [(df ['ID'] == utente)]  
    prima=date_utente['Data/Ora'].sort_values(ascending=True).iloc[0]  #ordino le date in ordine crescente e prendo la prima
    ultima=date_utente['Data/Ora'].sort_values(ascending=False).iloc[0] #ordino le date in ordine secrescente e prendo la prima
    data_primo_ev.append(prima)
    data_ultimo_ev.append(ultima)  
elapsed = time.perf_counter_ns() - start

#Calcolo giorni tra primo e ultimo evento  e li salvo in una lista (distanza_primo_ultimo)

distanza_primo_ultimo=[]
date_primo=[] #lista contenete date_primo_ev
date_secondo=[] #lista contenete date_ultimo_ev
data=0

for data in range(len(data_primo_ev)):
    date_primo.append(datetime.datetime.strptime(data_primo_ev[data], '%d/%m/%Y %H:%M').date()) #trasformo data da str a obj
for data in range(len(data_ultimo_ev)):
    date_secondo.append(datetime.datetime.strptime(data_ultimo_ev[data], '%d/%m/%Y %H:%M').date())
        
for data in range(len(date_primo)):
  distanza_primo_ultimo.append(abs((date_primo[data]-date_secondo[data]).days)) 
  
tabella_features=[]
j=0
for j in range(len(utenti)):
     tabella_features.append([numlog_utente.index[j],numlog_utente[j], data_primo_ev[j], data_ultimo_ev[j], distanza_primo_ultimo[j], 
                    ])
    
     
user_features=pd.DataFrame(tabella_features, columns= ['ID utente', 'Eventi totali' , 'Data Primo Evento', 
                                                       'Data Ultimo Evento ', 'Distanza Prima-Ultima Data'])

# Inserisco nel DataFrame il numero di volte che ciascun utente ha fatto l'evento specifico 

u=0 #utente
e=0 #evento relativo ad un solo utente

for u in range(len(utenti)):    
    for evento in eventi_diversi:
     for e in range(len(tabella_evento[u])):
         if evento == tabella_evento[u].index[e]: # se l'evento corrisponde all'evento dell'utente...
            user_features.loc[u,evento]=tabella_evento[u].values[e] #...inserisco l'informazione nel DataFrame
            
            #salvo file Excel

user_features.to_excel(args.Data1)

df_temp = pd.DataFrame(0,index=users,columns=eventi)

for i in range(df.shape[0]):
    df_temp.loc[df.loc[i,'ID'],df.loc[i,'evento']] += 1
# salva su file la lista dei log anonimizzata
outstr = json.dumps(data, indent=params['input']['IndentJSON'])
f2 = open(join(params['output']['OutDir'], params['output']['OutFile']), 'w')
f2.write(outstr)
f2.close()

# salva su file la tabella utente-ID man mano che generra gli ID
outstr1 = json.dumps(d, indent=params['input']['IndentJSON'])
f3 = open(join(params['input']['InDir'], params['input']['IdFile']), 'w')
f3.write(outstr1)
f3.close()    

elapsed = time.perf_counter_ns() - start
print('*** elapsed ***', elapsed / 1000000000.0)
#with open('Outfile1.xlsx', 'w') as outfile: 
#    json.dump(outstr1, outfile)

#user_features.to_excel(args.outstr1)