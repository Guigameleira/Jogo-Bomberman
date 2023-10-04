import pygame, sys
from pygame.locals import QUIT
import os
import time

pygame.init()

largura = 800
altura = 600
screen = pygame.display.set_mode((largura, altura))
contador = 0
explosão = False
vidas = 3
hitbox = False

tela_inicial = True
jogando = False
game_over = False
contadorPonto = 0
vitoria = False

#Variaveis do Bomberman
vel = 0.08
Bomberframe = 3
pos_x = 48
pos_y = 48
left = True
right = False
Bombframe = 0
bomba = False

#Clock
clock = pygame.time.Clock()
timer_started = False
timer_duration = 2000  
timer_elapsed = 0



#colliders
colliders = []
colliders_terreno = []
colliders_bloco = []
colliders_explosões = []
lista_danos = []
colliders_armadilha = []



morreu = False




start_ticks=pygame.time.get_ticks() #starter tick
seconds=(pygame.time.get_ticks()-start_ticks)/1000

lista_space = []
lista_tempo = []
lista_tempo.append(seconds)
lista_delbomba = []


lista_tempo2 = []
lista_tempo2.append(seconds)

#Função de Carregar
def load():
  global Start,font,tileset,Final,collider_mapa,collider_mapa2,Bomber,collider_jogador,telaInicial,nome_arquivo_fonte,tamanho_fonte,fonte,mapa,colliders_bloco,posx_inimigo,posy_inimigo,gameover,vit,colliders_vitoria,mapax
  tileset = pygame.image.load("mapa1.png")
  vit = pygame.image.load("vitoria.jpg")


  #Carrengando o mapa
  arquivo = open("mapa")
  mapa = []
  for line in range (0, 11):
    mapa.append((arquivo.readline()).replace("\n", ""))


  mapax = mapa
  
  print(mapa)


  
  #carregando a fonte
  nome_arquivo_fonte = 'fonte.ttf'
  caminho_fonte = os.path.join(os.path.dirname(__file__), nome_arquivo_fonte)
  tamanho_fonte = 20
  fonte = pygame.font.Font(caminho_fonte, tamanho_fonte)

  
  telaInicial = pygame.image.load("tel.png")
  Bomber = pygame.image.load("Bomber1.png")
  gameover = pygame.image.load("gameover.png")
  #Construindo o mapa
  for i, linha in enumerate(mapa):
    for j, char in enumerate(linha):
        
        
      if char == "A":
        collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
        colliders.append(collider_mapa)
        
      elif char == "P":
        collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
        #colliders.append(collider_mapa)
        colliders_bloco.append(collider_mapa)
      elif char == "G":
        collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
        colliders_terreno.append(collider_mapa)
      elif char == "E":
        collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
        colliders_armadilha.append(collider_mapa)

      elif char == 'V':
        colliders_vitoria = pygame.Rect(j*48, i*48, 48, 48)
        
load()



def atualizamapa(x,y):
  global mapa
  
  if morreu == False:
  
    mud = mapa[y]
    lista = []
    for i in mud:
      lista.append(i)
    lista[x] = "G"
    mud = ""
    for i in lista:
      mud += i
    mapa[y] = mud
  """ 
  if morreu == True:
    mapa = mapax
    mud = mapa[y]
    lista = []
    for i in mud:
      lista.append(i)
    lista[x] = "G"
    mud = ""
    for i in lista:
      mud += i
    mapa[y] = mud
    """
#Função de Gradiente de cor
def criar_gradiente(largura, altura, cor1, cor2):
    gradiente = pygame.Surface((largura, altura))
    for y in range(altura):
        # Interpolação linear entre as cores
        r = int((cor2[0] - cor1[0]) * (y / altura) + cor1[0])
        g = int((cor2[1] - cor1[1]) * (y / altura) + cor1[1])
        b = int((cor2[2] - cor1[2]) * (y / altura) + cor1[2])
        linha = pygame.Surface((largura, 1))
        linha.fill((r, g, b))
        gradiente.blit(linha, (0, y))
    return gradiente

cor_inicial = (237, 116, 40)  # Azul
cor_final = (255, 255, 255)  # Amarelo
gradiente = criar_gradiente(largura, altura, cor_inicial, cor_final)


#Função de desenhar
def drawscreen(screen):
  
  global Start,font,Bomberframe,Bomber,collider_mapa,collider_mapa2,seconds,posx_bomba,posy_bomba,bomba,contador,explosão,telaInicial,vidas,posx_inimigo,posy_inimigo,collider_inimigo,gameover,game_over,tela_inicial,pos_x,pos_y
  screen.fill((255,255,255))
  if tela_inicial == True:
    screen.fill((255,255,255))
    telaMaior = pygame.transform.scale(telaInicial,(600,400))
    screen.blit(gradiente, (0, 0))
    screen.blit(telaMaior, (100, 50))
    
    # Renderizando o texto com a fonte personalizada
    texto = fonte.render("Pressione Enter para começar", True, (0, 0, 0))
    posicao_texto = (largura // 2 - texto.get_width() // 2, altura // (2) + 400 // 2)
    screen.blit(texto,posicao_texto)
    
  if jogando == True:
    screen.fill((16,120,48))
    
    #Crianção do mapa
    for i, linha in enumerate(mapa):
      for j, char in enumerate(linha):
        
        if char == "A":
         screen.blit(tileset, (j*48, i*48), (48, 0, 48, 48))
         
         
        elif char == "P":
         screen.blit(tileset, (j*48, i*48), (96, 0, 48, 48))
         
        elif char == "E":
         screen.blit(tileset, (j*48, i*48), (336, 336, 48, 48))
         
         
        elif char == "S":
         screen.blit(tileset, (j*48, i*48), (192, 0, 48, 48))

        elif char == 'V':
          screen.blit(tileset,(j*48, i*48),(0,0,48,48))
    #screen.blit(tileset,(48,48), (144 + 48* Bombframe,288,48,48 )) 

    
    

    if bomba == True:
      if contador == 0:
        contador += 1
        posx_bomba = (pos_x+17)//48 *48
        posy_bomba = (pos_y+30)//48 *48
      if len(lista_space) > 0 and lista_tempo[-1] < (lista_delbomba[-1] + 3):
        screen.blit(tileset,(posx_bomba,posy_bomba), (144 + 48* Bombframe,288,48,48 ))
      else:
        bomba = False
        contador = 0
        explosão = True
    #animação Bomberman
    if Bomberframe >= 6 and Bomberframe <= 8:
      screen.blit(Bomber,  (pos_x, pos_y), (((Bomberframe-6)*32, 136,32,51)))

    if Bomberframe >= 9 and Bomberframe <= 11:
        screen.blit(Bomber,  (pos_x, pos_y), (((Bomberframe-9)*32, 12,32,50)))
  
  
    if Bomberframe >= 0 and Bomberframe <= 2:
        screen.blit(Bomber,  (pos_x, pos_y), (0+Bomberframe*32, 200,32,50))
  
    if Bomberframe >= 3 and Bomberframe <= 5:
        screen.blit(Bomber,  (pos_x, pos_y), ((Bomberframe-3)*32,72,32,51))
        

    if explosão == True:
            screen.blit(tileset, (posx_bomba,posy_bomba),(192,144,48,48))
            screen.blit(tileset, (posx_bomba+48,posy_bomba),(192,144,48,48))
            screen.blit(tileset, (posx_bomba-48,posy_bomba),(192,144,48,48))
            screen.blit(tileset, (posx_bomba,posy_bomba+48),(192,144,48,48))
            screen.blit(tileset, (posx_bomba,posy_bomba-48),(192,144,48,48))
            
      
          
    
    #desenho do collider
    

    #pygame.draw.rect(screen, (0, 255, 0), (collider_jogador.x, collider_jogador.y ,collider_jogador.width, collider_jogador.height), 2)
   
   #######
    pygame.draw.rect(screen, (255, 255, 255), (50,540, 180, 50),2,10)
    hearts = pygame.transform.scale(pygame.image.load("heart.png"), (40, 40))
    if vidas >= 1:
      heart1 = screen.blit(hearts,(70,545))
    if vidas >= 2:
      heart2 = screen.blit(hearts,(120,545)) 
    if vidas == 3:
      heart3 = screen.blit(hearts,(170,545))


    texto = fonte.render("Pontuação:", True, (255, 255, 255))
    posicao_texto = (300,550)
    screen.blit(texto,posicao_texto)
    pygame.draw.rect(screen, (255, 255, 255), (500,540, 180, 50),2,10)

    texto2 = fonte.render(str(contadorPonto), True, (255, 255, 255))
    posicao_texto2 = (565,550)
    screen.blit(texto2,posicao_texto2)
    ######
  
  if game_over == True:
    texto = fonte.render("Voce Perdeu", True, (0, 0, 0))
    posicao_texto = (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2)

    screen.blit(gameover, (0,0),(0,0,screen.get_width(),screen.get_height()))
    pygame.display.update()


 
    
  


  
      
  
def update(dt):
  global jogando, tela_inicial,pos_x,pos_y,Bomberframe, Bombframe,collider_jogador,lista_delbomba,lista_space,lista_tempo,bomba,pos_x,pos_y,explosão,colliders_bloco,colliders_explosões,hitbox,vidas,contadorPonto,lista_danos,timer_started,timer_started,timer_elapsed,posy_inimigo,collider_inimigo,posx_inimigo,posy_inimigo,game_over,mapax,mapa
  old_x, old_y = pos_x, pos_y

  
  
  keys = pygame.key.get_pressed()
  
  if keys[pygame.K_RETURN]:
    tela_inicial = False
    jogando = True
  if keys[pygame.K_e]:
    jogando = False
    game_over = True







  if jogando:


  #controle do personagem
    if keys[pygame.K_w] or keys[pygame.K_UP]:
    
    
      if Bomberframe < 9:
        Bomberframe = 9
      Bomberframe+=1
      if Bomberframe > 11:
        Bomberframe = 9
      
      pos_y = pos_y - vel*dt
  
    elif keys[pygame.K_s]or  keys[pygame.K_DOWN]:
 

      if Bomberframe < 6:
        Bomberframe = 6
      Bomberframe+=1
      if Bomberframe > 8:
        Bomberframe = 6
      pos_y = pos_y + vel*dt
 
     
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    
      

      if Bomberframe < 3:
        Bomberframe = 3
      Bomberframe+=1
      if Bomberframe > 5:
        Bomberframe = 3
      
      pos_x = pos_x + vel*dt

   
    
    elif keys[pygame.K_a]or  keys[pygame.K_LEFT]:
      

      if Bomberframe > 2:
        Bomberframe = 0
      Bomberframe+=1
      if Bomberframe > 2:
        Bomberframe = 0
      pos_x = pos_x - vel*dt

    if keys[pygame.K_SPACE]:
      if bomba == False:
        bomba = True
        lista_space.append('1')
        lista_delbomba.append(seconds)




      #collider_bomba = pygame.Rect(posx_bomba,posy_bomba,48,48)
      


       
        
        
        #screen.blit(tileset,(posx_bomba,posy_bomba), (144 + 48* Bombframe,288,48,48 ))

  #
  #
  #
  
  Bombframe += 1 
  if Bombframe > 2:
    Bombframe = 0 

  collider_jogador = pygame.Rect(pos_x+1,pos_y+30,28,20)
  
  for i in colliders_armadilha:
    if collider_jogador.colliderect(i) and i not in lista_danos:


      lista_danos.append(i)
      pos_x = old_x
      pos_y = old_y
      
      vidas -= 1
      
      break
  for i in colliders:
   
    if collider_jogador.colliderect(i):
      pos_x = old_x
      pos_y = old_y
   

  for i in colliders_bloco:
   
    if collider_jogador.colliderect(i):
      pos_x = old_x
      pos_y = old_y
    
  
  if explosão == True:
    
    colliders_explosões.append(pygame.Rect(posx_bomba, posy_bomba, 48, 48))
    colliders_explosões.append(pygame.Rect(posx_bomba + 48, posy_bomba, 48, 48))
    colliders_explosões.append(pygame.Rect(posx_bomba - 48, posy_bomba, 48, 48))
    colliders_explosões.append(pygame.Rect(posx_bomba, posy_bomba + 48, 48, 48))
    colliders_explosões.append(pygame.Rect(posx_bomba, posy_bomba - 48, 48, 48))

    lista_temporaria = colliders_bloco
    colliders_bloco = []
    collider_destruidos = []
    for i in lista_temporaria:
      colidiu_com_explosao = False
      for b in colliders_explosões:
          if b.colliderect(i):
              collider_destruidos.append(i)
              colidiu_com_explosao = True
              atualizamapa(i.x//48,i.y//48)
              contadorPonto += 200
              break

      if not colidiu_com_explosao:
          colliders_bloco.append(i)

      lista_temporaria = []
      explosão = False
    hitbox = True
  


  if hitbox == True:
    timer_started = True
    for i in colliders_explosões:
      
      #pygame.draw.rect(screen, (0, 255, 0), (i.x, i.y ,i.width, i.height), 2)
      if collider_jogador.colliderect(i) and i not in lista_danos:
        vidas -= 1
        lista_danos.append(i)
        break


  if vidas == 0:
    jogando = False
    game_over = True
    vidas += 3

  if collider_jogador.colliderect(colliders_vitoria):
    vitoria = True
    if vitoria == True:
      screen.blit(vit, (0,0),(0,0,screen.get_width(),screen.get_height()))
      pygame.display.update()
      time.sleep(3)
      pygame.display.update()
      vitoria = False
      jogando = False
      tela_inicial = True
      vidas = 3
      pos_x = 48 
      pos_y = 48
      contadorPonto = 0
      colliders_bloco = []
      collider_destruidos = []
      arquivo = open("mapa")
      mapa = []
      for line in range (0, 11):
        mapa.append((arquivo.readline()).replace("\n", ""))

      for i, linha in enumerate(mapa):
        for j, char in enumerate(linha):
          if char == "P":
           collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
           colliders_bloco.append(collider_mapa)




  
  if seconds > lista_tempo2[-1]:
    hitbox = False
    colliders_explosões = []
    lista_danos = []

  if game_over == True:
    morreu = True
    
    game_over = False
    
    screen.blit(gameover, (0,0),(0,0,screen.get_width(),screen.get_height()))
    pygame.display.update()
    time.sleep(3)
    tela_inicial = True
    pygame.display.update()
    pos_x = 48
    pos_y = 48
    contadorPonto = 0
    colliders_bloco = []
    collider_destruidos = []
    arquivo = open("mapa")
    mapa = []
    for line in range (0, 11):
      mapa.append((arquivo.readline()).replace("\n", ""))

    for i, linha in enumerate(mapa):
      for j, char in enumerate(linha):
        if char == "P":
          collider_mapa = pygame.Rect(j*48, i*48, 48, 48)
          
          colliders_bloco.append(collider_mapa)

    """
    
    
    vidas = 3
    #if seconds > listatempo1[-1]:
    """



pygame.display.set_caption('Projeto Bomberman')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            
            pygame.quit()
            sys.exit()
    pygame.display.update()

    seconds=(pygame.time.get_ticks()-start_ticks)/1000
  
    clock.tick(20)
    dt = clock.get_time()
    drawscreen(screen)
    lista_tempo.append(seconds)
    update(dt)
    
  
    #if seconds>10: # if more than 10 seconds close the game
    #  break



  
#start_ticks=pygame.time.get_ticks() #starter tick
#while mainloop: # mainloop
#    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
#    if seconds>10: # if more than 10 seconds close the game
#        break
#    print (seconds) #print how many seconds

