import socket
import time 
import threading 
from queue import Queue


#Defenição de classes
class spaceship:
    row = 19
    col = [4,5,6]
    def move(self, g ,direction):
            #Se já tiver nos extremos não faz nada
            if self.col[0]==0 and self.col[2]==9:
                return

            if(direction>0):
                g.matrix[self.row][self.col[0]]=0
                g.matrix[self.row][self.col[2]+1]=1
                self.col = [x+1 for x in self.col]

            if(direction<0):
                g.matrix[self.row][self.col[2]]=0
                g.matrix[self.row][self.col[0]-1]=1
                self.col = [x-1 for x in self.col]


    def fire(self, g, row, col):
        #Apagar tiro anterior caso não seja o primeiro
        if row != 19:
            g.matrix[row][col]=0
        #Se encontrar um alien matá-lo
        if g.matrix[row-1][col] == 2:
            g.matrix[row-1][col] == 0
            y = 0
            x = 4
            aux = g.enemy.pos[1]
            while aux != col:
                y += 1
                aux += 2
            while g.enemy.lives[x][y] != 1:
                x-=1
            g.enemy.lives[x][y]=0
            return
        #Desenhar o novo tiro
        g.matrix[row-1][col]=3
        #Se chegarmos ao fim da matriz, o tiro desapareces
        if row-1 == 0:
            g.matrix[row-1][col]=0
            return
        #Propagar o tiro:
        t = Timer(1/5, self.fire, [g, row-1, col])
        t.start()



class aliens:
    def __init__(self):
        self.lives = [[1 for x in range(4)] for y in range(5)]
        self.pos = [0,0]
        self.direction = 1  #Quando positivo anda da esquerda para a direita

    def move(self, g):
        #Apagar Anteriores
        x=self.pos[0]-2
        for i in range(5):
            x+=2
            y=self.pos[1]
            for j in range(4):
                    g.matrix[x][y]=0
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
                        g.matrix[x][y]=2
                    y += 2
        #Continuar a andar
        t = Timer(1,self.move,[g])
        t.start()





class Space_invaders:
    def __init__(self,matrix_s, input_queue):
        self.socket = matrix_s
        self.input_queue = input_queue
        self.ship = spaceship()
        self.enemy = aliens()
        #Iniciar matriz que simula a matriz de leds
        #self.matrix = [[0 for x in range(10)] for y in range(20)]
        self.matrix = [[BLACK]*WIDTH for x in range(HEIGHT)]
        #Desenhar a nave espacial na sua posição inicial
        for n in self.ship.col:
            self.matrix[self.ship.row][n]=1
        #Desenhar aliens na sua posição inicial
        y=-2
        for i in range(5):
            y+=2
            x=0
            for j in range(4):
                    self.matrix[x][y]=2
                    x +=2
        self.loop()

    def check_win(self):
        for i in range(5):
            for j in range(4):
                if self.lives[i][j] != 0:
                    #Se existir algum inimigo vivo não acaba
                    return 0
        #Caso contrário o jogo acaba
        return 1
        
    def update_screen(self):
        screen = b''
        for i in range(WIDTH):
            for j in range(HEIGHT):
                screen += bytes(self.matrix[j][i])
        
        self.socket.sendall()
    
    def loop(self):
        while True:

            if not self.input_queue.empty():
                btn = self.input_queue.get()

                if btn == 'Left':
                    self.ship.move(self,-1)
                elif btn == 'Right':
                    self.ship.move(self,1)
                elif btn == 'A':
                    self.ship.fire(self,self.ship.row,self.ship.col[1])
                
                self.update_screen()
                
            
                







