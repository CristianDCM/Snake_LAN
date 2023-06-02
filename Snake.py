import pygame
import random
import time
import Servidor
import threading
import socket

pygame.init()
ventana = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
brown = pygame.Color(165, 42, 42)

class SnakeGame:
    def __init__(self):
        self.nickname = ""
        self.log_direction = ""
        self.game_over = False
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [400, 300]
        self.food_spawn = True
        self.score = 0
        self.direction = "RIGHT"
        self.changeto = self.direction 

    def game_over_screen(self): #Game over screen
        my_font = pygame.font.SysFont('monaco', 72)
        go_surf = my_font.render('Game Over', True, red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (300, 15)
        ventana.blit(go_surf, go_rect)
        pygame.display.flip()
        time.sleep(3)
        self.save_score()
        self.show_menu()

    def show_name(self): #Nickname screen
        ventana.fill(black)
        font = pygame.font.SysFont('monaco', 36)
        text = font.render("Ingrese su nickname", True, white) 
        text_rect = text.get_rect(center=(300, 100))
        ventana.blit(text, text_rect)
        pygame.display.flip()
        while True: # Nickname input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.nickname = self.nickname.strip()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.nickname = self.nickname[:-1]
                    else:
                        self.nickname += event.unicode
            ventana.fill(black)
            text = font.render("Ingrese su nickname", True, white) 
            text_rect = text.get_rect(center=(300, 100))
            ventana.blit(text, text_rect)
            text = font.render(self.nickname, True, white)
            text_rect = text.get_rect(center=(300, 150))
            ventana.blit(text, text_rect)
            pygame.display.flip()

    def show_menu(self): #Menu screen
        menu_options = ['Jugar', 'Tabla de Puntuaciones', 'Salir']
        selected_option = 0
        font = pygame.font.SysFont('monaco', 36)
        while True:
            ventana.fill(black)
            for i, option in enumerate(menu_options): #Menu options
                text = font.render(option, True, white if i == selected_option else red)
                text_rect = text.get_rect(center=(300, 150 + i * 50))
                ventana.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get(): #Menu navigation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Jugar
                            self.show_name()
                            self.start_game()
                        elif selected_option == 1:  # Tabla de Puntuaciones
                            self.show_scores()
                        elif selected_option == 2:  # Salir
                            pygame.quit()
                            quit()

    def show_scores(self): #Scoreboard screen
        scores = [] 
        file = open("d:/Snake_LAN/scores.txt", "r") #Read scores
        for line in file:
            scores.append(line) 
        scores.sort(key=lambda x: int(x.split()[1]), reverse=True)  
        file.close()
        ventana.fill(black) #Show scores
        font = pygame.font.SysFont('monaco', 36)
        for i, score in enumerate(scores):
            text = font.render(str(i + 1) + ". " + score.split()[0] + " " + score.split()[1], True, white)
            text_rect = text.get_rect(center=(300, 150 + i * 50))
            ventana.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(5) #Wait 5 seconds
        self.show_menu()

    def save_score(self):
        file = open("d:/Snake_LAN/scores.txt", "a") #Save score
        file.write(self.nickname + " " + str(self.score) + "\n") 
        file.close()

    def start_game(self): #Game screen
        self.game_over = False
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [400, 300]
        self.food_spawn = True
        self.score = 0
        self.direction = "RIGHT"
        self.changeto = self.direction
        while not self.game_over: # Game loop
            self.mov_log() #Read log LAN <--------------------
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN: #Keyboard input
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.changeto = "RIGHT"
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.changeto = "LEFT"
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.changeto = "UP"
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.changeto = "DOWN"
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            """ 
            Snake movement logic
            direction = up not down -> change direction = up
            """
            if self.changeto == "RIGHT" and not self.direction == "LEFT": #Snake movement
                self.direction = "RIGHT"
            if self.changeto == "LEFT" and not self.direction == "RIGHT":
                self.direction = "LEFT"
            if self.changeto == "UP" and not self.direction == "DOWN":
                self.direction = "UP"
            if self.changeto == "DOWN" and not self.direction == "UP":
                self.direction = "DOWN"
            """
            Snake direction
            direction = up -> snake_pos[1] -= 10
            """
            if self.direction == "RIGHT":
                self.snake_pos[0] += 10
            if self.direction == "LEFT":
                self.snake_pos[0] -= 10
            if self.direction == "UP":
                self.snake_pos[1] -= 10
            if self.direction == "DOWN":
                self.snake_pos[1] += 10
            self.snake_body.insert(0, list(self.snake_pos)) #Snake body
            """
            Snake food logic
            head = food -> score + 1 -> food_spawn = False 
            """
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
            else:
                self.snake_body.pop()
            if not self.food_spawn: #Food spawn
                self.food_pos = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]
            self.food_spawn = True
            ventana.fill(black)
            for pos in self.snake_body:
                pygame.draw.rect(ventana, green, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(ventana, brown, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
            if self.snake_pos[0] > 590 or self.snake_pos[0] < 0: #Game over conditions X and Y 
                self.game_over_screen() 
            if self.snake_pos[1] > 390 or self.snake_pos[1] < 0:
                self.game_over_screen()
            for block in self.snake_body[1:]: 
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]: # Snake body collision
                    self.game_over_screen()
            pygame.display.set_caption("Snake | Score: " + str(self.score))
            pygame.display.flip()
            clock.tick(10)
         
    def read_log(self): #Read log LAN
        archivo = open("d:/Snake_LAN/log.txt", "r")
        msg = archivo.read()
        archivo.close()
        if msg == self.log_direction:
            return None
        return msg
    
    def mov_log(self): #Snake movement LAN
        msg = self.read_log() #<-------------------- 
        if msg == None:
            return
        if msg == "arriba" and not self.direction == "abajo":
            self.changeto = "UP"
        if msg == "abajo" and not self.direction == "arriba":
            self.changeto = "DOWN"
        if msg == "derecha" and not self.direction == "izquierda":
            self.changeto = "RIGHT"
        if msg == "izquierda" and not self.direction == "derecha":
            self.changeto = "LEFT"
        self.log_direction = msg 

def main():
    s =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # asocied to the socket
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0] #ip Local
    port = 7800
    s.close()
    server = threading.Thread(target=Servidor.start_server, args=(host, port)) # Second process
    server.start()
    game = SnakeGame() # First process
    game.show_menu()

if __name__ == "__main__":
    main()