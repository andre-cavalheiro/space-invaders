"""CORES:
    1-nave espacial
    2-inimigos
    3-Tiros
"""
from threading import Timer

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

            g.print_me()
    def fire(self, g, row, col):
        #Apagar tiro anterior caso não seja o primeiro
        if row != 19:
            g.matrix[row][col]=0

        #Desenhar o novo tiro
        g.matrix[row-1][col]=3

        g.print_me()

        #Se chegarmos ao fim da matriz, para o tiro
        """if row-1 == 0:
            return"""
        #Propagar o tiro:
        t = Timer(1/5, self.fire, [g, row-1, col])
        t.start()

class aliens:
    pos = [0,0]
    direction = 1

    def __init__(self):
        self.lives = [[1 for x in range(4)] for y in range(5)]

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
        g.print_me()
        #Continuar a andar
        t = Timer(3,self.move,[g])
        t.start()

    def fire(self):
        return




class game:
    ship = spaceship()
    enemy = aliens()
    def __init__(self):
        #Iniciar matriz que simula a matriz de leds
        self.matrix = [[0 for x in range(10)] for y in range(20)]
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

    def print_me(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])
        print("----")


#Programa
g = game()
g.print_me()
#g.enemy.move(g)
g.ship.fire(g,g.ship.row,g.ship.col[1])
print("Running")
g.ship.move(g,1)
g.ship.fire(g,g.ship.row,g.ship.col[1])
