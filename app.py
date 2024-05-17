import subprocess
import pyautogui
from time import sleep

def open_app(file):
    try:
        subprocess.Popen(file)
    except Exception:
        raise AttributeError

def click(x, y):
    pyautogui.click(x,y, duration=0.5)

def modelo_ponto(mes, nome, cargo):
    modelo_ponto = f"{mes}.{nome}_{cargo}_{dict_mes[mes]}2023"
    return modelo_ponto

def modelo_cheque(mes, nome, cargo):
    modelo_cheque = f"{mes}.{nome}_{cargo}_REC PAG_{dict_mes[mes]}2023"
    return modelo_cheque

def get_first_name(list_name):
    nome = list_name.split(" ")[0]#Pega só o primeiro nome
    return nome

def check_type(type, mes, nome, cargo):
    if type == "s":
        modelo_pont = modelo_ponto(mes,nome,cargo)
        return modelo_pont
    elif type == "n":
        modelo_chequ = modelo_cheque(mes,nome,cargo)
        return modelo_chequ
    raise ValueError

def click_and_write( type, model):
    if type == "s":
        click(543,1070)
        click(838,537)
        pyautogui.write(model)

    elif type == "n":
        click(543,1070)
        click(838,537)
        pyautogui.write(model)

    else:
        raise ValueError
    
#dicionario com o mês
dict_mes = {
    "01":"JAN",
    "02":"FEV",
    "03":"MAR",
    "04":"ABR",
    "05":"MAI",
    "06":"JUN",
    "07":"JUL",
    "08":"AGO",
    "09":"SET",
    "10":"OUT",
    "11":"NOV",
    "12":"DEZ",
}

contador = 0 #Variavel para controlar quantas vezes vai ser escaneado
validador_pasta = False #Variavel para validar se a pasta com o nome do funcionário já foi criada
modelo_pont = '' #Modelo para folha de ponto
modelo_chequ = '' #Modelo para contra-cheque
nome_fun = '' #Nome do funcionario
cargo = '' #Cargo
nome_mesmo = 'n' #Começou com "n" para ser usado na primeira execução do código
valida_nome = False
#1- Abrir o aplicativo para escanear
file = "C:\Program Files (x86)\Brother\BrLauncher\BrLauncher.exe"
open_app(file)

#2- Clicar no programa de escanear
click(1023,389)

click(484,1006)
quantidade = int(input("Quantos Escaneamentos? "))#Quantas vezes vai escanear
click(543,1070)#Tira a janela que está minimizada


#Escanea quantas vezes você pediu
for contador in range(quantidade):
    #3- Clicar em escanear
    click(644,607)
    sleep(9)

    #5- Clicar em Ok
    click(1014,626)
    
    #Tira a janela que está minimizada
    click(543,1070)

    #6- Salvar arquivo
    click(1422,384)

    #Clica campo do nome do arquivo
    click(838,537)

    pyautogui.hotkey("ctrl", "a")#Seleciona tudo do campo
    pyautogui.press("delete")#Apaga tudo do campo
    click(484,1006)
    #Se for a primeira vez executando o código ele pede o nome só uma vez
    if contador < 1:
        nome_fun = input("Nome Completo: ").upper()
        cargo = input("Cargo: ").upper()
    else:
        nome_mesmo = input("O nome é o mesmo?\nSe for digite 's'(sim)\nSe não for digite 'n'(não)\n: ")#Se for digita "s" se não for "n"
        if nome_mesmo == "n":
            valida_nome = True
        else:
            valida_nome = False

    mes = input("Mês: ")
    tipo = input("Folha de ponto? ")#Se for digita "s" se não for "n"
    
    #Na primeira vez executando sempre vai cair aqui
    if nome_mesmo == "n":
        #Se não for a primeira vez executando ele não pede o nome novamente
        if contador > 0 and valida_nome == True:    
            nome_fun = input("Nome completo: ").upper()
            cargo = input("Cargo: ").upper()

        
        
        nome = get_first_name(nome_fun)#Pega só o primeiro nome
        modelo = check_type(tipo, mes, nome, cargo)
        nome_na_lista = input("Esse nome já está no arquivo 'Funcionários'? ")#"s"(sim) "n"(não)

        #Se o nome não estiver na lista ele adiciona
        if nome_na_lista == "n":
            with open("funcionarios.txt", "a") as arq:
                arq.write(f"\n{nome_fun}")
            validador_pasta = True   
        elif nome_na_lista == "s":
            print("Ok!")
        else:
            raise ValueError

    elif nome_mesmo == "s":
        with open("funcionarios.txt", "r") as arq:
            linhas = arq.readlines()

            for linha in linhas:
                nome_s = linha.rstrip()
                nome = get_first_name(nome_fun)
                if nome_s == nome_fun:
                    modelo = check_type(tipo, mes, nome, cargo)

    else:
        raise ValueError

    click_and_write(tipo, modelo)
    if nome_mesmo == "n":
        click(858,587)#Clica no lugar da pasta de destino
        modelo_pasta = f"G:\Meu Drive\scanner\{nome_fun}"
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        pyautogui.write(modelo_pasta)

    #9- Clicar em ok
    click(1087,632)
    #Se não a pasta não foi criada ele clica em "sim"
    if validador_pasta:
        click(1000,598)
    
    sleep(0.5)
    #10- Clicar em limpar
    click(657,654)