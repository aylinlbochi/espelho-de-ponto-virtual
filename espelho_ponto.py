import csv
import os
import tkinter as tk
from datetime import datetime

arquivo_ponto = 'ponto_virtual.csv'

if not os.path.exists(arquivo_ponto):
    with open (arquivo_ponto, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tipo', 'Data/Hora'])
        
janela = tk.Tk()
janela.title("Espelho de Ponto Virtual")
janela.geometry('400x400')

texto_status = tk.StringVar()
texto_status.set('Aguardando ação...')
texto_registros = tk.StringVar()
texto_resultado = tk.StringVar()

label_status = tk.Label(janela, textvariable=texto_status, fg='green')
label_registros = tk.Label(janela, textvariable=texto_registros, justify='left')
label_resultado = tk.Label(janela, textvariable=texto_resultado, fg='blue')


def registrar_ponto(tipo):
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(arquivo_ponto, mode='a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([tipo, agora])
                print(f'{tipo.capitalize()} registrado às {agora}')
            
            texto_status.set(f'{tipo.capitalize()} registrado às {agora}')
            atualizar_registros()
                

def atualizar_registros():
    with open(arquivo_ponto, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        registros = [f'{row[0]}: {row[1]}' for row in reader]
    texto_registros.set('\n'.join(registros[-5:]))


def calcular_horas_trabalhadas():
    registros = []
    with open(arquivo_ponto, mode='r') as file:
     reader = csv.reader(file)
     next(reader) 
     for row in reader:
        registros.append(row)
        return registros
        
     hoje = datetime.now().strftime('%Y-%m-%d')
     registros_hoje = [r for r in registros if r[1].startswith(hoje)]
     
     if len(registros_hoje) < 2:
        print('\nNão há registros suficientes para calcular as'\
        'horas trabalhadas.\n')
        return
            
    
    horarios = {r[0]: datetime.strftime(r[1], '%Y-%m-%d %H:%M:%S') for r in registros_hoje}


    total_trabalho = 0
    if 'entrada' in horarios and 'saida' in horarios:
        total_trabalho += (horarios['saida'] - horarios['entrada']).seconds
                    
    if 'intervalos' in horarios and 'retorno' in horarios:
        total_trabalho -= (horarios['retorno'] - horarios['intervalos']).seconds


    horas = total_trabalho // 3600
    minutos = (total_trabalho % 3600) // 60

    texto_resultado.set(f'Total trabalhado hoje: {horas}h {minutos}min')


btn_entrada = tk.Button(janela, text='Bater Entrada', command=lambda: registrar_ponto('Entrada'))
btn_intervalo = tk.Button(janela, text='Bater Intervalo', command=lambda: registrar_ponto('Intervalo'))          
btn_retorno = tk.Button(janela, text= 'Bater Retorno', command=lambda: registrar_ponto('Retorno'))      
btn_saida = tk.Button(janela, text='Bater Saida', command=lambda: registrar_ponto('Saida'))
btn_calcular = tk.Button(janela, text='Calcular Horas', command=calcular_horas_trabalhadas)       


btn_entrada.pack(pady=5)
btn_intervalo.pack(pady=5)
btn_retorno.pack(pady=5)
btn_saida.pack(pady=5)
btn_calcular.pack(pady=10)
label_status.pack(pady=10)
label_registros.pack(pady=10)
label_resultado.pack(pady=10)

atualizar_registros()

janela.mainloop()