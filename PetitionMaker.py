from num2words import num2words
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import date
from time import sleep


#Este código foi feito, no decorrer do ano de 2023, então muitas funções que eu criei estão desorganizadas e, possivelmente, maiores do que
#o necessário, devido a minha falta de experiência no momento em questão. As mesmas não foram reorganizadas, ou refeitas por mim, por conta
#de eu não usar mais esse código, só usei ele no decorrer do meu estágio informal de 2023.


def SelecionarOpcao():
    global Selecao
    Selecao = Tk()

    Selecao.title('Selecione o que você deseja preencher')

    InfoReu = Button(Selecao, text='Informações do Réu', command=OpcaoReu)
    InfoReu.grid(column=0, row=0)

    InfoCliente = Button(Selecao, text='Informações do Cliente', command=OpcaoCliente)
    InfoCliente.grid(column=0, row=1)

    InfoAll = Button(Selecao, text='Informações do Réu e do Cliente', command=OpcaoDois)
    InfoAll.grid(column=0, row=2)

    Selecao.mainloop()


def OpcaoReu():
    global Reu, Cliente
    Reu = True
    Cliente = False
    Selecao.destroy()


def OpcaoCliente():
    global Reu, Cliente
    Reu = False
    Cliente = True
    Selecao.destroy()


def OpcaoDois():
    global Reu, Cliente
    Reu = True
    Cliente = True
    Selecao.destroy()


def main():
    global LinkPeticao
    SelecionarOpcao()
    LinkPeticao = input('informe o link da petição\n')

    if Cliente:
        ClienteInfo()

        open_chrome()
        substituir('CEPCliente', f'CEP: {NewCEP}')
        substituir('NomeCliente', NewNOME)
        substituir('RGCliente', f'RG nº {NewRG}')
        substituir('CPFCliente', f'CPF/MF sob o nº {NewCPF}')
        substituir('CARACTERISTICASCliente', NewCaracteristicasCliente)
        substituir('TRABALHOCliente', NewTrabalho)
        substituir('FORO', NewFORO)
        substituir('DATAHOJE', NewDataHoje)
        close_chrome()

    if Reu:
        global Importe, DivTexto, DivQuant
        Importe = 0
        DivTexto = ''
        DivQuant = int(input('Quantas dívidas deveram ser protocoladas?\n'))
        MakeText()
        NewANODIVIDA = input('Insira os anos de vencimento das dívidas:\n')

        open_chrome()
        substituir('DívidaInfo', DivTexto)
        substituir('VALORDIVIDA', DivImporte)
        substituir('ANODIVIDA', NewANODIVIDA)
        close_chrome()


def ClienteInfo():
    global NewCEP, NewNOME, NewRG, NewCPF, NewCaracteristicasCliente, NewTrabalho, NewFORO, NewDataHoje

    NewCEP = input('Informe o CEP do(a) cliente, formato(00000-000, São Paulo-SP)\n')
    NewNOME = input('Informe o nome do(a) cliente, formato(FULANO DE TAL)\n')
    NewRG = input('Informe o RG do(a) cliente, formato(00.000.000-A)\n')
    NewCPF = input('Informe o CPF do(a) cliente, formato(000.000.000-00)\n')
    NewCaracteristicasCliente = input('Informe as características do(a) cliente, formato(nacionalidade, estado civil)\n')
    NewTrabalho = input('Informe o vínculo empregatício do(a) cliente, formato(função/desempregado)\n')
    NewFORO = input('Informe o FORO do(a) cliente, formato(DO FORO REGIONAL I - BAIRRO DA COMARCA DE CIDADE-SP)\n')

    dia = date.today().strftime('%d')
    mes = date.today().strftime('%m')
    ano = date.today().strftime('%Y')
    NomesMeses = {
        '01': 'janeiro',
        '02': 'fevereiro',
        '03': 'março',
        '04': 'abril',
        '05': 'maio',
        '06': 'junho',
        '07': 'julho',
        '08': 'agosto',
        '09': 'setembro',
        '10': 'outubro',
        '11': 'novembro',
        '12': 'dezembro'}
    mes = NomesMeses[mes]

    NewDataHoje = f'{dia} de {mes} de {ano}'


def valores():
    global DivID, DivData, Valor, BRL, Extenso, DivValor

    DivID = input('Informe o número do contrato do processo, formato(0000000000000000)\n')
    DivData = input('Informe a data de vencimento da dívida do processo, formato(00/00/0000)\n')

    Valor = float(
        input('Informe o valor da dívida do processo, formato(00,00)\n').replace('.', '').replace(',', '.'))
    BRL = f'R$ {Valor:_.2f}'.replace('.', ',').replace('_', '.')
    Extenso = num2words(Valor, lang='pt_BR', to='currency')

    DivValor = f'{BRL} ({Extenso})'


def MakeText():
    global DivTexto, Importe, DivImporte

    if DivQuant == 1:
        valores()
        DivTexto = f"n° {DivID}, vencida desde {DivData}, no valor de {DivValor}"
        DivImporte = DivValor

    else:
        for i in range(DivQuant):
            valores()
            Importe = Importe + Valor

            if i == 0:
                DivTexto = f"n° {DivID}, vencida desde {DivData}, no valor de {DivValor}"

            elif i != DivQuant - 1:
                DivTexto = f"{DivTexto}, n° {DivID}, vencida desde {DivData}, no valor de {DivValor}"

            else:
                ImporteBRL = f'R$ {Importe:_.2f}'.replace('.', ',').replace('_', '.')
                ImporteExtenso = num2words(Importe, lang='pt_BR', to='currency')
                DivImporte = f'{ImporteBRL} ({ImporteExtenso})'

                DivTexto = f"{DivTexto}, e n° {DivID}, vencida desde {DivData}, no valor de {DivValor}, totalizando o importe de {DivImporte}"


def open_chrome():
    global navegador, LinkPeticao
    navegador = webdriver.Chrome()


def close_chrome():
    navegador.quit()


def substituir(OldText, NewText):
    navegador.get(LinkPeticao)
    ActionChains(navegador).key_down(Keys.LEFT_CONTROL).perform()
    ActionChains(navegador).send_keys('f').perform()
    ActionChains(navegador).key_up(Keys.LEFT_CONTROL).perform()
    navegador.find_element('xpath', '//*[@id="docs-findbar-button-more-options"]').click()
    navegador.find_element('xpath', '//*[@id="docs-findandreplacedialog-input"]').send_keys(OldText)
    navegador.find_element('xpath', '//*[@id="docs-findandreplacedialog-replace-input"]').send_keys(NewText)
    navegador.find_element('xpath', '//*[@id="docs-findandreplacedialog-button-replace-all"]').click()
    sleep(3)


main()
