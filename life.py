import pygame
import time
from pygame.constants import K_LEFT, K_UP

class grid(object):
    def __init__(self,l_cells):
        self.dic = l_cells

    def get_grid(self):
        return self.dic

    def set_grid(self,new_cells):
        self.dic = new_cells

    def ajout_suppr_cell(self,cell):
        if cell in self.dic.keys():
            del self.dic[cell]
        else:
            self.dic[cell] = [0,True]

    def dic_access_test(self):
        for cell in self.dic.keys():
            print("cell=",cell,"    cell[0] : cell[1]=>",cell[0],":",cell[1],"     dic[cell]=",self.dic[cell],"   cell in dic.keys()=",cell in self.dic.keys(),"\n dic[cell][0] : dic[cell][1]=>",self.dic[cell][0],":",self.dic[cell][1])

    def reset_voisins(self):
        #reset du nombre de voisins
        for cell in self.dic.keys():
            self.dic[cell][0] = 0

    def calc_voisins(self):
        #calcul du nombre de voisins a la prochaine itération
        new_cells = {}
        for cell in self.dic.keys():
            #print("voisins de",cell)
            voisins = [(cell[0]-1,cell[1]),(cell[0]+1,cell[1]),
                (cell[0],cell[1]-1),(cell[0],cell[1]+1),
                (cell[0]-1,cell[1]-1),(cell[0]-1,cell[1]+1),
                (cell[0]+1,cell[1]-1),(cell[0]+1,cell[1]+1)]
            for v in voisins:
                #print("     v=",v,"  v in dic=",v in self.dic.keys(),end="\n")
                if v in self.dic.keys():
                    self.dic[v][0] += 1
                elif v in new_cells.keys():
                    new_cells[v][0] += 1
                elif v not in self.dic.keys() and v not in new_cells.keys():
                    new_cells[v] = [1,False]
        #on ajoute les nouvelles cells au dic
        for cell in new_cells.keys():
            self.dic[cell] = new_cells[cell]

    def calc_alive(self):
        #on détermine quelles cellules seront en vie a la prochaine itération
        dead_cells = []
        for cell in self.dic.keys():
            if self.dic[cell][1]:
                if self.dic[cell][0] == 2 or self.dic[cell][0] == 3:
                    self.dic[cell][1] = True
                else:
                    dead_cells.append(cell)
            else:
                if self.dic[cell][0] == 3:
                    self.dic[cell][1] = True
                else:
                    dead_cells.append(cell)

        #on delete les cellules mortes du dic
        for d in dead_cells:
            del self.dic[d]

    def calc_next_iteration(self):
        #on fait les appel des fonctions ici
        self.reset_voisins()
        self.calc_voisins()
        self.calc_alive()

    def move_down(self,step):
        new_dic = {}
        for case in self.dic.keys():
            new_dic[(case[0],case[1]+step)] = self.dic[case]
        self.dic = new_dic

    def move_up(self,step):
        new_dic = {}
        for case in self.dic.keys():
            new_dic[(case[0],case[1]-step)] = self.dic[case]
        self.dic = new_dic

    def move_left(self,step):
        new_dic = {}
        for case in self.dic.keys():
            new_dic[(case[0]-step,case[1])] = self.dic[case]
        self.dic = new_dic

    def move_right(self,step):
        new_dic = {}
        for case in self.dic.keys():
            new_dic[(case[0]+step,case[1])] = self.dic[case]
        self.dic = new_dic

def draw_alive_cell(dic,cell_size):
    for cell in dic.keys():
        pygame.draw.rect(screen,"white", pygame.Rect(cell[0]*cell_size,cell[1]*cell_size,cell_size,cell_size))

def draw_lines(w,h,cell_size):
    for i in range(cell_size,w,cell_size):
        pygame.draw.line(screen,"grey",(i,0),(i,h))

    for i in range(cell_size,h,cell_size):
        pygame.draw.line(screen,"grey",(0,i),(w,i))

def on_button(pos,button_top_left,button_size):
    if pos[0] >= button_top_left[0] and pos[0] <= button_top_left[0] + button_size[0]:
        if pos[1] >= button_top_left[1] and pos[1] <= button_top_left[1] + button_size[1]:
            return True
    return False

initial_state = {(42,22):[0,True],(42,23):[0,True],(42,24):[0,True],(41,23):[0,True],(43,23):[0,True]}
init_copy = {}
for case in initial_state.keys():
    init_copy[case] = initial_state[case]
p = grid(init_copy)

WITDH = 1280
HEIGHT = 720
CELL_SIZE = 15
pygame.init()
screen = pygame.display.set_mode((WITDH,HEIGHT))
clock = pygame.time.Clock()

back_color = (39,47,104)

font = pygame.font.Font(None,35)

button_size = (150,40)
button_couleur = (47,36,36)

text_color = "white"

button_pause_top_left = (WITDH-160,HEIGHT-50)
button_pause_rect = pygame.Rect(button_pause_top_left[0],button_pause_top_left[1],button_size[0],button_size[1])
pause_text = font.render("Play/Pause", True, text_color)

button_speed_plus_top_left = (button_pause_top_left[0]-160,HEIGHT-50)
button_speed_plus_rect = pygame.Rect(button_speed_plus_top_left[0],button_speed_plus_top_left[1],button_size[0],button_size[1])
speed_plus_text = font.render("Speed +", True, text_color)

button_speed_minus_top_left = (button_speed_plus_top_left[0]-160,HEIGHT-50)
button_speed_minus_rect = pygame.Rect(button_speed_minus_top_left[0],button_speed_minus_top_left[1],button_size[0],button_size[1])
speed_minus_text = font.render("Speed -", True, text_color)

button_reset_top_left = (button_speed_minus_top_left[0]-160,HEIGHT-50)
button_reset_rect = pygame.Rect(button_reset_top_left[0],button_reset_top_left[1],button_size[0],button_size[1])
reset_text = font.render("Reset", True, text_color)

button_zoom_plus_top_left = (button_reset_top_left[0]-160,HEIGHT-50)
button_zoom_plus_rect = pygame.Rect(button_zoom_plus_top_left[0],button_zoom_plus_top_left[1],button_size[0],button_size[1])
zoom_plus_text = font.render("Zoom +", True, text_color)

button_zoom_minus_top_left = (button_zoom_plus_top_left[0]-160,HEIGHT-50)
button_zoom_minus_rect = pygame.Rect(button_zoom_minus_top_left[0],button_zoom_minus_top_left[1],button_size[0],button_size[1])
zoom_minus_text = font.render("Zoom -", True, text_color)

button_grid_top_left = (button_zoom_minus_top_left[0]-160,HEIGHT-50)
button_grid_rect = pygame.Rect(button_grid_top_left[0],button_grid_top_left[1],button_size[0],button_size[1])
grid_text = font.render("Grid", True, text_color)

running = True

step = 1
play = True
reset = True
speed = 1
iter = 0
move_up = False
move_down = False
move_left = False
move_right = False
zoom_plus = False
zoom_minus = False
zoom_buf = 0
threshold = 10
grille = True

while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_UP:
                move_up = True
            if events.key == pygame.K_DOWN:
                move_down = True
            if events.key == pygame.K_LEFT:
                move_left = True
            if events.key == pygame.K_RIGHT:
                move_right = True
        if events.type == pygame.KEYUP:
            if events.key == pygame.K_UP:
                move_up = False
            if events.key == pygame.K_DOWN:
                move_down = False
            if events.key == pygame.K_LEFT:
                move_left = False
            if events.key == pygame.K_RIGHT:
                move_right = False
        if events.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if on_button(pos,button_pause_top_left,button_size):
                play = not play
                reset = False
            elif on_button(pos,button_speed_plus_top_left,button_size):
                speed += 1
            elif on_button(pos,button_speed_minus_top_left,button_size):
                if speed >= 2:
                    speed -= 1
            elif on_button(pos,button_reset_top_left,button_size):
                if play:
                    play = not play
                reset = True
                init_copy = {}
                for case in initial_state.keys():
                    init_copy[case] = initial_state[case]
                p.set_grid(init_copy)
            elif on_button(pos, button_zoom_plus_top_left,button_size):
                zoom_plus = True
                zoom_buf = 0
            elif on_button(pos,button_zoom_minus_top_left,button_size):
                zoom_minus = True
                zoom_buf = 0
            elif on_button(pos, button_grid_top_left, button_size):
                grille = not grille
            else:
                if not play:
                    x = pos[0] //CELL_SIZE
                    y = pos[1] // CELL_SIZE
                    p.ajout_suppr_cell((x,y))
                    if reset:
                        init_tmp = p.get_grid()
                        initial_state = {}
                        for case in init_tmp.keys():
                            initial_state[case] = init_tmp[case]
        if events.type == pygame.MOUSEBUTTONUP:
            zoom_plus = False
            zoom_minus = False

    screen.fill(back_color)
    dic = p.get_grid()
    draw_alive_cell(dic,CELL_SIZE)
    if grille:
        draw_lines(WITDH,HEIGHT,CELL_SIZE)
    if iter == 0 and play:
        p.calc_next_iteration()
    #print("*************************************")
    iter+=speed
    if iter > 60:
        iter = 0

    if move_up:
        p.move_down(step)
    if move_down:
        p.move_up(step)
    if move_left:
        p.move_right(step)
    if move_right:
        p.move_left(step)

    if zoom_plus and CELL_SIZE <= 99:
        zoom_buf+=1
        if zoom_buf >= threshold:
            CELL_SIZE += 1
            zoom_buf = 0

    if zoom_minus and CELL_SIZE >= 2 :
        zoom_buf+=1
        if zoom_buf >= threshold:
            CELL_SIZE -= 1
            zoom_buf = 0

    #ON DESSINE LES BOUTTONS
    pygame.draw.rect(screen,button_couleur,button_pause_rect)
    screen.blit(pause_text, (button_pause_top_left[0]+10,button_pause_top_left[1]+7))

    pygame.draw.rect(screen,button_couleur,button_speed_plus_rect)
    screen.blit(speed_plus_text, ((button_speed_plus_top_left[0]+30,button_speed_plus_top_left[1]+7)))

    pygame.draw.rect(screen,button_couleur,button_speed_minus_rect)
    screen.blit(speed_minus_text, ((button_speed_minus_top_left[0]+30,button_speed_minus_top_left[1]+7)))

    pygame.draw.rect(screen,button_couleur,button_reset_rect)
    screen.blit(reset_text, (button_reset_top_left[0]+43,button_reset_top_left[1]+7))

    pygame.draw.rect(screen,button_couleur,button_zoom_plus_rect)
    screen.blit(zoom_plus_text, (button_zoom_plus_top_left[0]+37,button_zoom_plus_top_left[1]+7))

    pygame.draw.rect(screen,button_couleur,button_zoom_minus_rect)
    screen.blit(zoom_minus_text, (button_zoom_minus_top_left[0]+37,button_zoom_minus_top_left[1]+7))

    pygame.draw.rect(screen,button_couleur,button_grid_rect)
    screen.blit(grid_text, (button_grid_top_left[0]+50,button_grid_top_left[1]+7))

    pygame.display.flip()


    clock.tick(60)

pygame.quit()
