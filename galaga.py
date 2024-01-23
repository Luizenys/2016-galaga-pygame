

__author__ = 'Luiza'

from PPlay.window import *
from PPlay.keyboard import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.sound import *
from PPlay.collision import *
import time
import random
random.seed()

GAME_SPEED = 1
GAME_STATE = 0


LARGURA_JANELA = 512
ALTURA_JANELA = 512

VEL  = 250
VEL_TIRO = 500
VEL_TIRO_INIMIGO = 450
VEL_ONDA = 150
INTERVALO_TIRO = 250
INTERVALO_TIRO_INIMIGO = 300
INTERVALO_KAMIKAZE = 1000
INTERVALO_ONDA = 5000
VEL_KAMIKAZE = 350

janela  = Window(LARGURA_JANELA,ALTURA_JANELA)
janela.set_background_color((0,0,0))

janela.set_title("Galaga")
inimigo1 = Sprite("inimigo1.png")

teclado = Keyboard()

background_01 = GameImage("starfield.gif")
background_02 = GameImage("starfield.gif")
background_01.y = 0
background_02.y = -background_02.height
background_roll_speed = 80

spriteNaveGrande = Sprite("navegrande.png")
spriteNave = Sprite("nave.png")
nave = dict(sprite = spriteNave , posX = LARGURA_JANELA/2-spriteNave.width/2,
            posY = ALTURA_JANELA-spriteNave.height )

vel_inimigo = 200
tiros = []
tirosInimigos = []
tempoUltimoTiro = janela.last_time
tempoUltimoTiroIni = janela.last_time
ultimoSorteio = janela.last_time
tempoUltimaOnda = janela.last_time
spriteNave.score = 0
spriteNave.direction = -1
bullets = []
ondas = []

posxBlocoInimigos = 0
posyBlocoInimigos = 0

VEL_BLOCO_X = 150
VEL_BLOCO_Y = 50

somTiro = Sound("laser_widebeam.wav")


def criarInimigos(nomeArq, nLin, nCol,posxBloco, posyBloco):

    inimigos = []
    for i in range(0,nLin):
        linhaInimigos = []
        for j in range (0,nCol):
            inimigo = Sprite(nomeArq)
            inimigo.direction = 1
            inimigo.posx = j*(inimigo.width+inimigo.width/2)
            inimigo.posy = i*inimigo.height
            linhaInimigos.append(inimigo)
        inimigos.append(linhaInimigos)
    desenharInimigos(inimigos, posxBloco, posyBloco,VEL_BLOCO_X)

    return inimigos

def desenharInimigos(inimigos, posxBloco, posyBloco,VEL_BLOCO_X):
    for i in range (0,len(inimigos)):
        for j in range (0, len(inimigos[i])):
            if (inimigos[i][j])!= 1:
               inimigos[i][j].draw()
               x = inimigos[i][j].posx
               y = inimigos[i][j].posy
               inimigos[i][j].set_position(x + posxBloco, y + posyBloco)
            else:
                pass
    movimentarInimigos(inimigos, posxBloco, posyBloco, VEL_BLOCO_X)


def movimentarInimigos(inimigos, posxBloco,posyBloco, VEL_BLOCO_X):
    width = inimigo1.width

    if (posxBloco + 1.2*width*len(inimigos[0])>=LARGURA_JANELA) or posxBloco<0:
        VEL_BLOCO_X *= -1

    deltaT = janela.delta_time()

    posxBloco += VEL_BLOCO_X*deltaT


    return posxBloco, posyBloco, VEL_BLOCO_X

def capturarEntrada(nave, tiros, tempoUltimoTiro):

    x = nave["posX"]
    y = nave["posY"]
    deltaT = janela.delta_time()
    deltaS = VEL*deltaT
    if teclado.key_pressed("ESC"):
        janela.close()
    if teclado.key_pressed("UP"):
        y = y - deltaS
    elif teclado.key_pressed("DOWN"):
        y = y + deltaS

    if teclado.key_pressed("RIGHT"):
        x = x + deltaS
    elif teclado.key_pressed("LEFT"):
        x = x - deltaS

    if (teclado.key_pressed("SPACE")):
        if (janela.last_time-tempoUltimoTiro>INTERVALO_TIRO):
            tiro = Sprite("tiropeq.png")
            somTiro.play()
            tiro.set_position(nave["sprite"].x+nave["sprite"].width/2-tiro.width/2, nave["sprite"].y-tiro.height)
            tiros.append(tiro)
            tempoUltimoTiro = janela.last_time

    nave["posX"] = x
    nave["posY"] = y

    return tempoUltimoTiro

def criarOndas(inimigos,ondas,tempoUltimaOnda):
    x = random.randint(0,2)
    if x==0:
        onda = Sprite("onda.png")
    else:
        onda = Sprite("onda2.png")

    i = random.randint(0,2)
    j = random.randint(0,3)
    if (janela.last_time - tempoUltimaOnda > INTERVALO_ONDA):
        if inimigos[i][j] != 1:
            if i == 2:
                onda.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - onda.width / 2,
                                     inimigos[i][j].y  + inimigos[i][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            elif i == 1 and inimigos[2][j] == 1:
                onda.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - onda.width / 2,
                                  inimigos[i][j].y + inimigos[i][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            elif i == 1 and inimigos[2][j] != 1:
                onda.set_position(inimigos[2][j].x + inimigos[2][j].width / 2 - onda.width / 2,
                                     inimigos[2][j].y + inimigos[2][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            elif i == 0 and inimigos[1][j] == 1 and inimigos[2][j] == 1:
                onda.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - onda.width / 2,
                                  inimigos[i][j].y  + inimigos[i][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            elif i == 0 and inimigos[1][j] != 1 and inimigos[2][j] == 1:
                onda.set_position(inimigos[1][j].x + inimigos[1][j].width / 2 - onda.width / 2,
                                     inimigos[1][j].y  + inimigos[1][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            elif i == 0 and inimigos[2][j] != 1:
                onda.set_position(inimigos[2][j].x + inimigos[2][j].width / 2 - onda.width / 2,
                                  inimigos[2][j].y  + inimigos[2][j].height)
                ondas.append(onda)
                tempoUltimaOnda = janela.last_time
            else:
                pass


        else:
            pass
    return tempoUltimaOnda

def foo(inimigos,bullets,tempoUltimoTiroIni):
    tiroIni = Sprite("sprite_fire.png")
    i = random.randint(0,2)
    j = random.randint(0,3)
    if (janela.last_time - tempoUltimoTiroIni > INTERVALO_TIRO_INIMIGO):
        if inimigos[i][j] != 1:
            if i == 2:
                tiroIni.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - tiroIni.width / 2,
                                     inimigos[i][j].y + tiroIni.height + inimigos[i][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            elif i == 1 and inimigos[2][j] == 1:
                tiroIni.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - tiroIni.width / 2,
                                     inimigos[i][j].y + tiroIni.height + inimigos[i][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            elif i == 1 and inimigos[2][j] != 1:
                tiroIni.set_position(inimigos[2][j].x + inimigos[2][j].width / 2 - tiroIni.width / 2,
                                     inimigos[2][j].y + tiroIni.height + inimigos[2][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            elif i == 0 and inimigos[1][j] == 1 and inimigos[2][j] == 1:
                tiroIni.set_position(inimigos[i][j].x + inimigos[i][j].width / 2 - tiroIni.width / 2,
                                     inimigos[i][j].y + tiroIni.height + inimigos[i][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            elif i == 0 and inimigos[1][j] != 1 and inimigos[2][j] == 1:
                tiroIni.set_position(inimigos[1][j].x + inimigos[1][j].width / 2 - tiroIni.width / 2,
                                     inimigos[1][j].y + tiroIni.height + inimigos[1][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            elif i == 0 and inimigos[2][j] != 1:
                tiroIni.set_position(inimigos[2][j].x + inimigos[2][j].width / 2 - tiroIni.width / 2,
                                     inimigos[2][j].y + tiroIni.height + inimigos[2][j].height)
                bullets.append(tiroIni)
                tempoUltimoTiroIni = janela.last_time
            else:
                pass


        else:
            pass
    return tempoUltimoTiroIni



def limitarMovimento(largura,altura,nave):

    x = nave["posX"]
    y = nave["posY"]

    if (x<0):
        x = 0
    elif (x>=largura-nave["sprite"].width):
        x = largura-nave["sprite"].width

    if (y<int((2.0/3.0)*altura)):
        y = int((2.0/3.0)*altura)
    elif (y>altura-nave["sprite"].height):
        y = altura-nave["sprite"].height

    nave["posX"] = x
    nave["posY"] = y

def desenharTiros(tiros,posxBloco,posyBloco,inimigos):
    for tiro in tiros:
        tiro.draw()
        checarColisaoInimigo(tiro,posxBloco,posyBloco,inimigos)

def desenharTirosInimigos(bullets,nave,GAME_STATE):
    for b in bullets:
        b.draw()
        if (Collision.collided(b,nave["sprite"])):
            bullets.remove(b)
            GAME_STATE = 2
    return GAME_STATE

def desenharOndas(ondas,nave,GAME_STATE):
    for b in ondas:
        b.draw()
        if (Collision.collided(b,nave["sprite"])):
            ondas.remove(b)
            GAME_STATE = 2
    return GAME_STATE



def movimentarTiros(tiros):
    deltaS = VEL_TIRO*janela.delta_time()
    for tiro in tiros:
        posx = tiro.x
        posy = tiro.y-deltaS
        tiro.set_position(posx,posy)

def removerTirosForaDaTela(tiros):
    for tiro in tiros:
        if (tiro.y<=0):
            tiros.remove(tiro)

def removerTirosInimigosForaDaTela(bullets):
    for b in bullets:
        if (b.y>=512):
            bullets.remove(b)


def checarColisaoInimigo(tiro,posxBloco,posyBloco,inimigos):
    for i in range (0,len(inimigos)):
        for j in range (0, len(inimigos[i])):
            if (inimigos[i][j]) != 1:
                if (Collision.collided(tiro, inimigos[i][j])):
                    tiros.remove(tiro)
                    spriteNave.score += 50
                    explosao = Sprite("explosao.png")
                    explosao.set_position(inimigos[i][j].x,inimigos[i][j].y)
                    explosao.draw()
                    explosion = Sound("explosion.wav")
                    explosion.play()
                    inimigos[i][j] = 1
                    desenharInimigos(inimigos, posxBloco, posyBloco,VEL_BLOCO_X)



def desenharTudo(janela,background_01,nave,tiros,inimigos,posxBlocoInimigos,posyBlocoInimigos):

    janela.set_background_color((0,0,0))

    background_01.draw()
    background_02.draw()
    desenharTiros(tiros, posxBlocoInimigos, posyBlocoInimigos, inimigos)
    desenharTirosInimigos(bullets,nave,GAME_STATE)

    desenharInimigos(inimigos, posxBlocoInimigos, posyBlocoInimigos,VEL_BLOCO_X)
    desenharTiros(tiros, posxBlocoInimigos, posyBlocoInimigos, inimigos)


    nave["sprite"].set_position(nave["posX"], nave["posY"])
    nave["sprite"].draw()


def bullet_movement(bullets):
    deltaS = VEL_TIRO_INIMIGO * janela.delta_time()
    for b in bullets:
        posx = b.x
        posy = b.y + deltaS
        b.set_position(posx, posy)

def ondasMovimento(ondas):
    deltaS = VEL_ONDA * janela.delta_time()
    for b in ondas:
        posx = b.x
        posy = b.y + deltaS
        b.set_position(posx, posy)


def recriarInimigos(inimigos,GAME_STATE,posxBlocoInimigos, posyBlocoInimigos):
    sound1 = Sound("powerup.wav")
    sound1.play()
    inimigos = []
    for i in range(0, 3):
        linhaInimigos = []
        for j in range(0, 4):
            inimigo = Sprite("fighter3.png")
            inimigo.direction = 1
            inimigo.posx = j * (inimigo.width + inimigo.width / 2)
            inimigo.posy = i * inimigo.height
            linhaInimigos.append(inimigo)
        inimigos.append(linhaInimigos)
    desenharInimigos(inimigos, posxBlocoInimigos, posyBlocoInimigos, VEL_BLOCO_X)

    return inimigos


inimigos = criarInimigos("fighter4.png", 3, 4,posxBlocoInimigos, posyBlocoInimigos)

def scrolling(bg_bottom, bg_top, roll_speed):
    bg_bottom.y += roll_speed * janela.delta_time()
    bg_top.y += roll_speed * janela.delta_time()
    if bg_top.y >= 0:
        bg_bottom.y = 0
        bg_top.y = -bg_top.height
    bg_bottom.draw()
    bg_top.draw()

def gameintro():
    janela.draw_text("Welcome to Galaga"
               , 50, 100, 50, (255, 255, 255), "Impact")
    janela.draw_text("ENTER para jogar | ESC para sair",
                     70, 0, 28, (255, 255, 255), "Calibri")
    janela.update()
    scrolling(background_01, background_02, background_roll_speed)


while (True):
    if GAME_STATE == 0:
        gameintro()
        #tema.play()
        spriteNaveGrande.set_position(170,200)
        spriteNaveGrande.draw()
        if teclado.key_pressed("enter"):
            GAME_STATE = 1
        if teclado.key_pressed("ESC"):
            janela.close()


    elif GAME_STATE == 1:
        limitarMovimento(janela.width, janela.height, nave)
        movimentarTiros(tiros)
        removerTirosForaDaTela(tiros)
        removerTirosInimigosForaDaTela(bullets)

        posxBlocoInimigos, posyBlocoInimigos, VEL_BLOCO_X = movimentarInimigos(inimigos, posxBlocoInimigos,
                                                                               posyBlocoInimigos, VEL_BLOCO_X)
        desenharTudo(janela, background_01, nave, tiros, inimigos, posxBlocoInimigos, posyBlocoInimigos)
        desenharTiros(tiros, posxBlocoInimigos, posyBlocoInimigos, inimigos)
        desenharTirosInimigos(bullets, nave, GAME_STATE)
        tempoUltimoTiroIni = foo(inimigos, bullets, tempoUltimoTiroIni)
        criarOndas(inimigos, ondas, tempoUltimaOnda)
        tempoUltimaOnda = criarOndas(inimigos,ondas,tempoUltimaOnda)
        desenharOndas(ondas, nave, GAME_STATE)
        ondasMovimento(ondas)

        bullet_movement(bullets)
        tempoUltimoTiro = capturarEntrada(nave, tiros, tempoUltimoTiro)
        foo(inimigos, bullets, tempoUltimoTiroIni)
        if inimigos[0].count(1) == 4 and inimigos[1].count(1) == 4 and inimigos[2].count(1) == 4:
            inimigos = recriarInimigos(inimigos,GAME_STATE,posxBlocoInimigos, posyBlocoInimigos)

        janela.draw_text("Score: " +
                         str(spriteNave.score), 5, 5, 16, (255, 255, 255), "Impact")
        janela.update()
        scrolling(background_01, background_02, background_roll_speed)


        if desenharTirosInimigos(bullets,nave,GAME_STATE)==2:
            GO = Sound("galaga_dive.wav")
            GO.play()
            GAME_STATE = 2

        if desenharOndas(ondas, nave, GAME_STATE)==2:
            GO = Sound("galaga_dive.wav")
            GO.play()
            GAME_STATE = 2



    elif GAME_STATE == 2:
        janela.draw_text("Game Over"
                         , 100, 200, 70, (255, 255, 255), "Impact")
        janela.draw_text("Score: " +
                         str(spriteNave.score), 200,300, 30, (255, 255, 255), "Impact")
        janela.draw_text("ESC para sair",
                         180, 0, 28, (255, 255, 255), "Calibri")
        janela.update()
        scrolling(background_01, background_02, background_roll_speed)
        if teclado.key_pressed("ESC"):
            janela.close()






