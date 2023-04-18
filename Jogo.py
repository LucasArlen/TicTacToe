import pygame
import random

pygame.init()

# Tamanho da janela
largura, altura = 600, 600

# Criação da janela
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Velha")

# Matriz do jogo
matriz = [['', '', ''], ['', '', ''], ['', '', '']]

# Dimensões dos quadrados
largura_quadrado = largura // 3
altura_quadrado = altura // 3

# Cor dos quadrados
cor_quadrado = (255, 255, 255)

# Desenhar os quadrados na janela
for i in range(3):
    for j in range(3):
        pygame.draw.rect(janela, cor_quadrado,
                         (i * largura_quadrado,
                          j * altura_quadrado,
                          largura_quadrado, 
                          altura_quadrado), 2)

# Escolha aleatória do jogador que começa jogando
def escolher_jogador():
    return random.choice(['X', 'O'])

    
def fazer_jogada(linha, coluna, jogador):
    matriz[linha][coluna] = jogador
    x = coluna * largura_quadrado + largura_quadrado // 2
    y = linha * altura_quadrado + altura_quadrado // 2
    raio = min(largura_quadrado, altura_quadrado) // 3
    cor = (255, 0, 0) if jogador == 'X' else (0, 0, 255)
    if jogador == 'X':
        pygame.draw.line(janela, cor, (x - raio, y - raio), (x + raio, y + raio), 5)
        pygame.draw.line(janela, cor, (x - raio, y + raio), (x + raio, y - raio), 5)
    else:
        pygame.draw.circle(janela, cor, (x, y), raio, 5)


def verificar_vencedor():
    # Verificar linhas
    for linha in range(3):
        if matriz[linha][0] == matriz[linha][1] == matriz[linha][2] and matriz[linha][0] != '':
            return matriz[linha][0]
        
    # Verificar colunas
    for coluna in range(3):
        if matriz[0][coluna] == matriz[1][coluna] == matriz[2][coluna] and matriz[0][coluna] != '':
            return matriz[0][coluna]
        
    # Verificar diagonais
    if matriz[0][0] == matriz[1][1] == matriz[2][2] and matriz[0][0] != '':
        return matriz[0][0]
    elif matriz[0][2] == matriz[1][1] == matriz[2][0] and matriz[0][2] != '':
        return matriz[0][2]
    
    # Não há vencedor
    return None

# variáveis do loop principal
jogador_atual = escolher_jogador()
jogo_acabou = False
vencedor = None

# loop principal
while not jogo_acabou:
    # loop de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_acabou = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            linha = y // altura_quadrado
            coluna = x // largura_quadrado
            # verifica se a jogada é válida
            if matriz[linha][coluna] == '':
                fazer_jogada(linha, coluna, jogador_atual)
                matriz[linha][coluna] = jogador_atual
                vencedor = verificar_vencedor()
                # verifica se o jogo acabou
                if vencedor is not None:
                    jogo_acabou = True
                elif all(matriz[i][j] != '' for i in range(3) for j in range(3)):
                    jogo_acabou = True
                else:
                    jogador_atual = 'X' if jogador_atual == 'O' else 'O'
    # desenha as jogadas já feitas
    for i in range(3):
        for j in range(3):
            if matriz[i][j] != '':
                fazer_jogada(i, j, matriz[i][j])
    pygame.display.update()

# exibe a mensagem final
if vencedor is not None:
    mensagem = f"O jogador {vencedor} venceu!"
else:
    mensagem = "Empate!"
    

janela.fill((0,0,0))

fonte = pygame.font.Font('fontes/FreeSans.ttf', 50)
texto = fonte.render(mensagem, True, (255, 255, 255))
janela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))

pygame.display.update()
pygame.time.wait(3000)
