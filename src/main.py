# Autor: Gabriel Oliveira de Freitas
# Componente Curricular: MI Algoritmos
# Concluído em: 26/10/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

import random
import os
import time
import keyboard

#Inicializar tabuleiro.
tabuleiro = []  #Inicializa a lista do tabuleiro.
for l in range(20):  #Loop para as linhas.
    linha = []  #Inicializa a linha atual.
    for c in range(10):  #Loop para as colunas.
        linha.append('⬛')  #Adiciona um espaço vazio à linha.
    tabuleiro.append(linha)  #Adiciona a linha completa ao tabuleiro.

#Lista de peças do jogo com a bomba.
peças = [
    [['🟦', '🟦', '🟦', '🟦']],  #Linha (azul).
    [['🟨', '🟨'], ['🟨', '🟨']],  #Quadrado (amarelo).
    [['⬛', '🟪', '⬛'], ['🟪', '🟪', '🟪']],  #T (roxo).
    [['🟥', '🟥', '⬛'], ['⬛', '🟥', '🟥']],  #Z (vermelho).
    [['⬛', '🟩', '🟩'], ['🟩', '🟩', '⬛']],  #S (verde).
    [['🟧', '🟧', '🟧'], ['🟧', '⬛', '⬛']],  #L (laranja).
    [['🟫', '🟫', '🟫'], ['⬛', '⬛', '🟫']],  #J (marrom).
    [['💣']]  #Bomba.
]

pontuação_total = 0  #Variável global para armazenar a pontuação total.

#Função para imprimir o tabuleiro.
def mostrar_tabuleiro():
    limpar_tela()  #Limpa a tela antes de atualizar o tabuleiro.
    for linha in tabuleiro:
        for bloco in linha:
            print(bloco, end='')  #Imprime cada bloco na linha.
        print()  #Pula para a próxima linha após imprimir todos os blocos da linha atual.
    print(f'Pontuação: {pontuação_total}') #Mostrar pontuação atual.
    
#Limpar a tela para atualizar o tabuleiro.
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')  #Comando para limpar a tela.

#Inserir peça no tabuleiro.
def inserir_peça(peça, linha, coluna):
    for l in range(len(peça)):
        for c in range(len(peça[l])):
            if peça[l][c] != '⬛':  #Ignora partes vazias.
                tabuleiro[linha + l][coluna + c] = peça[l][c]  #Insere a peça no tabuleiro na posição especificada.

#Remover peça do tabuleiro (usado para mover a peça).
def remover_peça(peça, linha, coluna):
    for l in range(len(peça)):
        for c in range(len(peça[l])):
            if peça[l][c] != '⬛':
                tabuleiro[linha + l][coluna + c] = '⬛'  #Remove a peça do tabuleiro, substituindo por espaços vazios.

#Verificar colisão com outras peças ou bordas do tabuleiro.
def verificar_colisao(peça, linha, coluna):
    for l in range(len(peça)):
        for c in range(len(peça[l])):
            if peça[l][c] != '⬛':
                if linha + l >= 20 or coluna + c < 0 or coluna + c >= 10 or tabuleiro[linha + l][coluna + c] != '⬛':
                    return True  #Se houver colisão com outra peça ou com as bordas, retorna True.
    return False  #Retorna False se não houver colisão.

#Função para girar peça.
def girar_peça(peça):
    #Define altura e largura da peça.
    altura = len(peça)
    largura = len(peça[0])
    
    #Inicializa matriz rotacionada.
    peça_rotacionada = []
    for coluna in range(largura):
        peça_rotacionada.append(['⬛'] * altura)
        
    #Rotaciona a peça 90 graus.
    for l in range(altura):
        for c in range(largura):
            peça_rotacionada[c][altura - l - 1] = peça[l][c]
    
    return peça_rotacionada  #Retorna peça rotacionada.

#Função para explodir a bomba e limpar uma área de 3x3 ao redor.
def explodir_bomba(linha, coluna):
    for l in range(linha - 1, linha + 2):
        for c in range(coluna - 1, coluna + 2):
            if 0 <= l < 20 and 0 <= c < 10:  #Verificar limites do tabuleiro.
                tabuleiro[l][c] = '⬛'  #Limpar a área ao redor da bomba.

#Funcão para remover linhas completadas e somar pontuação.
def quebrar_linhas():
    global pontuação_total
    linhas_quebradas = 0
    l = 19  #Começa a checar da última linha.

    while l >= 0:
        if '⬛' not in tabuleiro[l]:  #Verifica se a linha foi completada.
            del tabuleiro[l]  #Remove linha completa.
            tabuleiro.insert(0, ['⬛'] * 10)  #Insere nova linha vazia no topo.
            linhas_quebradas += 1  #Contador de linhas quebradas.
        else:
            l -= 1  #Passa para a linha de cima se não quebrou nenhuma.

    #Pontuação baseada no número de linhas quebradas.
    if linhas_quebradas == 1:
        pontuação_total += 100
    elif linhas_quebradas == 2 or linhas_quebradas == 3:
        pontuação_total += 200
    elif linhas_quebradas > 3:
        pontuação_total += linhas_quebradas * 100

#Função principal do jogo para descer, controlar a peça e definir dificuldade.
def descer_peça(dificuldade):
    peça_atual = random.choice(peças)  #Seleciona uma peça aleatória.
    linha, coluna = 0, random.randint(0, 10 - len(peça_atual[0]))  #Define a posição inicial.

    #Define a velocidade com base na dificuldade.
    if dificuldade == '1':
        velocidade = 0.45  #Velocidade fácil.
    elif dificuldade == '2':   
        velocidade = 0.3   #Velocidade média.
    elif dificuldade == '3':
        velocidade = 0.1   #Velocidade difícil.

    while True:
        remover_peça(peça_atual, linha, coluna)  #Remove peça da posição antiga.
        if not verificar_colisao(peça_atual, linha + 1, coluna):
            linha += 1  #Desce a peça se não houver colisão.
        else:
            if peça_atual == [['💣']]:  #Confere se a peça é uma bomba.
                explodir_bomba(linha, coluna)  #Explode bomba e limpa área 3x3.
            else:
                inserir_peça(peça_atual, linha, coluna)  #Fixar peça normal.
            quebrar_linhas()  #Remove linhas completas e pontua.
            mostrar_tabuleiro()  #Atualiza tabuleiro e exibe pontuação.
            peça_atual = random.choice(peças)  #Nova peça após colisão.
            linha, coluna = 0, random.randint(0, 10 - len(peça_atual[0]))
            if verificar_colisao(peça_atual, linha, coluna):
                print("Game Over") #Mensagem de fim de jogo.
                break  #Encerrar o jogo se a nova peça colidir ao surgir.

        #Movimentação da peça.
        if keyboard.is_pressed('left') and not verificar_colisao(peça_atual, linha, coluna - 1) or keyboard.is_pressed('A') and not verificar_colisao(peça_atual, linha, coluna - 1): #Direita.
            coluna -= 1
        elif keyboard.is_pressed('right') and not verificar_colisao(peça_atual, linha, coluna + 1) or keyboard.is_pressed('D') and not verificar_colisao(peça_atual, linha, coluna + 1): #Esquerda.
            coluna += 1
        elif keyboard.is_pressed('up') or keyboard.is_pressed('W'): #Girar peça.
            peça_rotacionada = girar_peça(peça_atual)
            if not verificar_colisao(peça_rotacionada, linha, coluna):
                peça_atual = peça_rotacionada

        inserir_peça(peça_atual, linha, coluna)  #Insere peça na nova posição.
        mostrar_tabuleiro()  #Exibe tabuleiro atualizado.
        
        #Descer a peça mais rápido.
        if keyboard.is_pressed('down') or keyboard.is_pressed('S'):
            time.sleep(0.05)  #Desce mais rápido.
        else:
            time.sleep(velocidade)  #Mantém velocidade normal.

#Reiniciar o tabuleiro.
def reiniciar_jogo():
    global tabuleiro, pontuação_total
    tabuleiro = []  # Inicializa a lista do tabuleiro.
    
    for l in range(20): #Loop para as linhas.
        linha = []
        for c in range(10): #Loop para as colunas.
            linha.append('⬛')
        tabuleiro.append(linha)
        
    pontuação_total = 0  #Reinicia a pontuação.

#Menu para o jogo.
def tetris():
    while True:
        Menu = input('ENTER - INICIAR JOGO\nDigite "2" para ver o manual do jogo\nDigite "3" para fechar o jogo\n').strip().upper() #Menu
        if Menu == '': #Iniciar jogo.
            velocidade = input('Dificuldade:\n(1) Fácil\n(2) Médio\n(3) Difícil\n') #Escolher velocidade.
            while velocidade != '1' and velocidade != '2' and velocidade != '3':
                velocidade = input('Dificuldade:\n(1) Fácil\n(2) Médio\n(3) Difícil\n')
            descer_peça(velocidade)
            print(f'A pontuação final foi de {pontuação_total} pontos.')
            reiniciar_jogo()
        elif Menu == '3': #Fechar o jogo.
            break
        elif Menu == '2': #Manual do jogo.
            print()
            print('W ou ↑ para girar a peça\nA ou ← para mover a peça para a esquerda\nD ou → para mover a peça para a direita')
            print('S ou ↓ para fazer a peça descer mais rápido')
            print()
tetris() #Chamada de função para iniciar o jogo.
