import socket
import time 
from threading import Timer
from queue import Queue
from client.const import *
from random import randint


#Argumento 'g' (game) nas funções simboliza o objecto Space_invaders


class spaceship:
    row = 19
    col = [4,5,6]
    def move(self, g ,direction):
            #Se já tiver nos extremos não faz nada
            if self.col[0]==0 and self.col[2]==9:
                return

            if(direction>0):
                g.matrix[self.row][self.col[0]]=BLACK
                g.matrix[self.row][self.col[2]+1]=BLUE
                self.col = [x+1 for x in self.col]

            if(direction<0):
                g.matrix[self.row][self.col[2]]=BLACK
                g.matrix[self.row][self.col[0]-1]=BLUE
                self.col = [x-1 for x in self.col]


    def fire(self, g, row, col):
        #Apagar tiro anterior caso não seja o primeiro
        if row != 19:
            g.matrix[row][col]=BLACK
        #Se encontrar um alien matá-lo
        if g.matrix[row-1][col] == RED:
            g.matrix[row-1][col] == BLACK
            
            y=0
            aux = g.enemy.pos[1]
            while aux != col:
                y += 1
                aux += 2
            x=0
            aux = g.enemy.pos[0]
            while aux != row-1:
                x += 1
                aux += 2

            g.enemy.lives[x][y]=0
            return
        
        #Desenhar o novo tiro
        g.matrix[row-1][col]=WHITE
        #Se chegarmos ao fim da matriz, o tiro desapareces
        if row-1 == 0:
            g.matrix[row-1][col]=BLACK
            return
        #Propagar o tiro:
        t = Timer(1/12, self.fire, [g, row-1, col])
        t.start()







class aliens:
    def __init__(self):
        self.lives = [[1 for x in range(4)] for y in range(5)]
        self.pos = [0,0]
        self.direction = 1  #Quando positivo anda da esquerda para a direita
        self.fire_speed = 1/12
        self.fire_intreval = 1

    def move(self, g):
        #Apagar Anteriores
        x=self.pos[0]-2
        for i in range(5):
            x+=2
            y=self.pos[1]
            for j in range(4):
                    g.matrix[x][y]=BLACK
                    y += 2
        #Alterar coordenadas
        if self.direction > 0:
            if self.pos[1] == 3:
                self.direction = -1
                self.pos[0] +=1
            else:
                self.pos[1] +=1
        else:
            if self.pos[1] == 0:
                self.direction = 1
                self.pos[0] +=1
            else:
                self.pos[1] -=1
        #Escrever os Novos
        x=self.pos[0]-2
        for i in range(5):
            x+=2
            y=self.pos[1]
            for j in range(4):
                    if self.lives[i][j] == 1:
                        g.matrix[x][y]=RED
                    y += 2
        #Continuar a andar
        t = Timer(1,self.move,[g])
        t.start()

    def alien_shoot(self,g):
        #Defenir o alien que vai disparar
        x = 4
        y = randint(0,3)
        while g.enemy.lives[x][y] == 0:
            x -= 1

        #Encontrar a posição da qual vai partir o tiro
        lin=g.enemy.pos[0]+2*x
        col=g.enemy.pos[1]+2*y
        
        #Disparar
        self.fire(g,lin,col,1)

    def fire(self,g,row, col,bool):
        #Apagar tiro anterior caso este nao seja o primeiro
        if bool != 1:
            g.matrix[row][col]=BLACK 
        #Se chocar contra a nave, terminar o jogo
        if g.matrix[row+1][col]==BLUE:
            g.state = -1     
        #Desenhar o novo tiro
        g.matrix[row+1][col]=GREEN
        #Se chegarmos ao fim da matriz, o tiro desapareces
        if row+1 == 19:
            g.matrix[row+1][col]=BLACK
            t = Timer(self.fire_intreval, self.alien_shoot, [g])
            t.start()
            return
        #Propagar o tiro:
        t = Timer(self.fire_speed, self.fire, [g, row+1, col, 0])
        t.start()

        
        
    






class Space_invaders:
    def __init__(self,matrix_s, input_queue):
        self.socket = matrix_s
        self.input_queue = input_queue
        self.ship = spaceship()
        self.enemy = aliens()
        self.state = 0      #0->Durante o jogo    1->Venceu   -1->Perdeu
        #Iniciar matriz que simula a matriz de leds
        self.matrix = [[BLACK]*WIDTH for x in range(HEIGHT)]
        #Desenhar a nave espacial na sua posição inicial
        for n in self.ship.col:
            self.matrix[self.ship.row][n]=BLUE
        #Desenhar aliens na sua posição inicial e iniciar o seu movimento e disparo
        y=-2
        for i in range(5):
            y+=2
            x=0
            for j in range(4):
                    self.matrix[x][y]=RED
                    x +=2
        self.enemy.move(self)
        p = Timer(3, self.enemy.alien_shoot, [self])
        p.start()
        #-------------------------EXPERIENCIAS--------------------------------------
        """
        t = Timer(3, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t1 = Timer(4, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t2 = Timer(5, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t3 = Timer(6, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t4 = Timer(7, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t5 = Timer(8, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t6 = Timer(9, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t7 = Timer(10, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t8 = Timer(10, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t9 = Timer(10, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        t10 = Timer(10, self.ship.fire, [self, self.ship.row, self.ship.col[1]])
        
        t.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()
        """
        
        

        
        #---------------------------------------------------------------------------
        self.loop()

    def check_win(self):
        for i in range(5):
            for j in range(4):
                if self.enemy.lives[i][j] != 0:
                    #Se existir algum inimigo vivo não acaba
                    return 
        #Caso contrário o jogo acaba
        self.state = 1
    
    def check_lost(self):
        bool=0
        level = 4
        dif = 0
        #Verificar qual o nível mais baixo em que existem inimigos
        while bool == 0:
            sum = 0
            for i in range(4):
                sum += self.enemy.lives[level][i]
            if sum != 0:
                break
            diff +=2
         
        #Verificar se o inimigo mais baixo já atingiu a naveingiu a nave   
        if self.enemy.pos[0] + 8 - dif == 19:
            self.state = -1
        return 
        
    def update_screen(self):
        screen = b''
        for i in range(HEIGHT):
            for j in range(WIDTH ):
                screen += bytes(self.matrix[i][j])
        
        self.socket.sendall(screen)
    
    def clear_screen(self):
        screen = b''
        s = [[BLACK]*WIDTH for x in range(HEIGHT)]

        for i in range(HEIGHT):
            for j in range(WIDTH):
                screen += bytes(s[i][j])
        
        self.socket.sendall(screen)


    def loop(self):
        while True:
            self.check_win()
            self.check_lost()

            if self.state != 0:
                self.clear_screen()
                break

            if not self.input_queue.empty():
                btn = self.input_queue.get()

                if btn == 'Left':
                    self.ship.move(self,-1)
                elif btn == 'Right':
                    self.ship.move(self,1)
                elif btn == 'A':
                    self.ship.fire(self,self.ship.row,self.ship.col[1])
            self.update_screen()
            time.sleep(MIN_PERIOD)
    
        
                
            
                






