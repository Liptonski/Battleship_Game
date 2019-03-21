import pygame
import time
import random
import sys

# *** Podstawowe parametry ***
pygame.init()
pygame.mixer.music.load('pirat.mp3')
pygame.mixer.music.play(-1, 0.0)
resolution=(1200, 600)
space=int(resolution[0]/24)
clock=pygame.time.Clock()
SCREEN=pygame.display.set_mode(resolution)
pygame.display.set_caption('Statki')

# *** Rozmiary czcionek ***
small = pygame.font.SysFont("comicsansms", 25)
med = pygame.font.SysFont("comicsansms", 50)
large = pygame.font.SysFont("comicsansms", 85)
menu = pygame.font.SysFont("comicsansms", 35)

# *** Klasa do tworzenia statkow ***
class Hull():

    def create_PC(self, size, water_taken):

        # Stworzyć tablice wspolrzednych lini oddzielajacych kwadraty
        lines_list=[]
        for i in range(1, 11):
            lines_list.append(space*i)

        ship_x = lines_list[random.randint(0, 9)]
        ship_y = lines_list[random.randint(0, 9)]
        ship_orient = random.randint(0, 1)  # 0 pionowo 1 poziomo

        ship_list = []  # pola zajete przez statek
        zone = []   # pola na ktorych nie mozna postawic innych statkow
        if ship_orient == 0:
            if ship_y+space*size<=(space*11):   # utworz wspolrzedne pol statku
                for i in range(0, size):
                    ship_list += [(ship_x, ship_y + (i * space))]
                    zone.extend(zone_set(ship_x, ship_y + (i*space), zone))
            elif ship_y+space*size>(space*11):
                for i in range(0, size):    # jezeli wychodzi poza plansze stworz go do tylu
                    ship_list += [(ship_x, ship_y - (i * space))]
                    zone.extend(zone_set(ship_x, ship_y - (i * space), zone))

        elif ship_orient == 1:
            if ship_x+space*size<=(space*11):
                for i in range(0, size):
                    ship_list += [(ship_x + (i * space), ship_y)]
                    zone.extend(zone_set(ship_x + (i * space), ship_y, zone))
            elif ship_x+space*size>(space*11):
                for i in range(0, size):
                    ship_list += [(ship_x - (i * space), ship_y)]
                    zone.extend(zone_set(ship_x - (i * space), ship_y, zone))

        for i in ship_list:
            if i in water_taken:    # Jezeli statek naklada sie z innym lub przykleja wywolaj funkcje jeszcze raz
                x=size
                y=water_taken
                return Hull.create_PC(self, x, y)
        else:   # Jezeli nie powieksz ogolna zajeta przestrzen o przestrzen statku i zworc jego wspolrzedne
            water_taken += list(set(zone))
            return ship_list
    def create_player(self, x, y, orient, size, water_taken):

        lines_list = []
        for i in range(13, 23):
            lines_list.append(space * i)

        ship_list = []
        zone = []
        if orient == 0:
            for i in range(0, size):
                ship_list += [(x, y + (i * space))]
                zone.extend(zone_set(x, y + (i * space), zone))
        elif orient == 1:
            for i in range(0, size):
                ship_list += [(x + (i * space), y)]
                zone.extend(zone_set(x + (i * space), y, zone))
        water_taken+=list(set(zone))
        return ship_list

# *** Klasa, zmienne i funkcje do tworzenia tla ***
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, resolution) # Dopasowuje rozdzielczosc tla
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
background=Background('Tlogra.jpg', [0,0])
background_game=Background('Tlo1.jpg', [0,0])
def screen_background():
    SCREEN.fill((255,255,255))
    SCREEN.blit(background.image, background.rect)
def game_background():
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(background_game.image, background.rect)
# *** Funkcje do wyznaczania obszarow ***
def zone_set(x, y, field):  # Funkcja tworzaca przestrzen wokol statkow aby sie nie sklejaly
    field += (x, y), (x+space, y), (x-space, y), (x, y-space), (x, y+space)
    return list(set(field))
def nearby(x, y):   # funkcja zwracajaca mozliwa przestrzen wokol strzalu PC (niweluje strzelanie poza plansze)
    field=[]
    if x==space*13:
        if y==space:
            field += (x+space, y), (x, y+space)
        elif y==space*10:
            field += (x+space, y), (x, y-space)
        else:
            field += (x+space, y), (x, y-space), (x, y+space)
    elif x==space*22:
        if y==space:
            field += (x-space, y), (x, y+space)
        elif y==space*10:
            field += (x-space, y), (x, y-space)
        else:
            field += (x-space, y), (x, y-space), (x, y+space)
    else:
        if y==space:
            field += (x+space, y), (x-space, y), (x, y+space)
        elif y==space*10:
            field += (x+space, y),(x-space, y), (x, y-space)
        else:
            field += (x+space, y), (x-space, y), (x, y-space), (x, y+space)
    return field
# *** Rysowanie Dwóch plansz ***
def board_1():
    x = space
    y = space
    for i in range(11):
        pygame.draw.line(SCREEN, (255, 255, 255), (space, y), (space*11, y), 2)
        pygame.draw.line(SCREEN, (255, 255, 255), (x, space), (x, space*11), 2)
        x += space
        y += space
                    # tworzenie tablic komputera i gracza
def board_2():
    x = space*13
    y = space
    for i in range(11):
        pygame.draw.line(SCREEN, (255, 255, 255), (space*13, y), (space*23, y), 2)
        pygame.draw.line(SCREEN, (255, 255, 255), (x, space), (x, space*11), 2)
        x += space
        y += space

# *** funkcje do pisania tekstu ***
def Text(text, color, size='small'):
    msg=""
    if size == "small":
        msg = small.render(text, True, color)
    elif size == "medium":
        msg = med.render(text, True, color)
    elif size == "large":
        msg = large.render(text, True, color)
    elif size == "menu":
        msg = menu.render(text, True, color)
    return msg, msg.get_rect()  # Dzieki zwracaniu get_rect() mozna wywolac pozniej rect.center
def messege(text, color, y_place=0, size='small'):
    msg, rect = Text(text, color, size)
    rect.center = (int(resolution[0]/2), int(resolution[1]/2)+y_place)
    SCREEN.blit(msg, rect)
def button_text(text, color, x, y, widht, height, size='small'):
    msg, rect = Text(text, color, size)
    rect.center = (x + (widht/2), y + (height/2))
    SCREEN.blit(msg, rect)

# *** Funkcje rysuja kolejno plansze z tlem, trafienia, pudla ***
def screen():
    game_background()
    board_1()
    board_2()
def Shots_draw(Shots):
    if Shots!=None:
        for i in Shots:
            pygame.draw.rect(SCREEN, (163, 194, 194), (i[0], i[1], space, space))
            pygame.draw.line(SCREEN, (255, 51, 0), (i[0]+3, i[1]+3), (i[0]+space-3, i[1]+space-3), 5)
            pygame.draw.line(SCREEN, (255, 51, 0), (i[0]+3, i[1]+space-3), (i[0]-3 + space, i[1]+3), 5)
def Misses_draw(Misses):
    if Misses!=None:
        for i in Misses:
            pygame.draw.circle(SCREEN, (0,0,0), (i[0]+space//2, i[1]+space//2), 10)
            #pygame.draw.rect(SCREEN, (0, 0, 0), (i[0], i[1], space, space))

def Menu():
    #pygame.draw.rect(SCREEN, (34,177,76), ((resolution[0]/2)-100, (resolution[1]/2)-50, 200, 50))
    buttons=[((resolution[0] / 2) - 400, (resolution[1] / 2) - 100, 200, 50),
            ((resolution[0] / 2) - 100, (resolution[1] / 2) - 100, 200, 50),
            ((resolution[0] / 2) + 200, (resolution[1] / 2) - 100, 200, 50),
            ((resolution[0] / 2) - 250, (resolution[1] / 2) + 50, 200, 50),
            ((resolution[0] / 2) + 50, (resolution[1] / 2) + 50, 200, 50)]
    i=0
    j=0
    exit=0
    dif=0
    exiting=False
    Dificulty = "Easy"
    # *** rysuje menu glowne z przyciskami ***
    def draw_menu():
        screen_background()
        messege("Witamy w grze Statki", (255, 187, 51), -200, size='large')
        pygame.draw.rect(SCREEN, (255, 117, 26), ((resolution[0] / 2) - 400, (resolution[1] / 2) - 100, 200, 50))
        pygame.draw.rect(SCREEN, (255, 117, 26), ((resolution[0] / 2) - 100, (resolution[1] / 2) - 100, 200, 50))
        pygame.draw.rect(SCREEN, (255, 117, 26), ((resolution[0] / 2) + 200, (resolution[1] / 2) - 100, 200, 50))
        pygame.draw.rect(SCREEN, (255, 117, 26), ((resolution[0] / 2) - 250, (resolution[1] / 2) + 50, 200, 50))
        pygame.draw.rect(SCREEN, (255, 117, 26), ((resolution[0] / 2) + 50, (resolution[1] / 2) + 50, 200, 50))
        button_text("PvE", (0, 102, 255), (resolution[0] / 2) - 400, resolution[1] / 2 - 100, 200, 50, size='menu')
        button_text("PvP", (0, 102, 255), (resolution[0] / 2) - 100, resolution[1] / 2 - 100, 200, 50, size='menu')
        button_text("Zasady", (0, 102, 255), (resolution[0] / 2) + 200, resolution[1] / 2 - 100, 200, 50, size='menu')
        button_text("Trudność", (0, 102, 255), (resolution[0] / 2) - 250, resolution[1] / 2 + 50, 200, 50, size='menu')
        button_text("Wyjście", (0, 102, 255), (resolution[0] / 2) + 50, resolution[1] / 2 + 50, 200, 50, size='menu')
    while True:
        draw_menu()
        pointer = buttons[i]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # *** Poruszanie sie po przyciskach ***
            if not exiting:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if i==0:
                            i=4
                        else:
                            i-=1
                    elif event.key == pygame.K_RIGHT:
                        if i==4:
                            i=0
                        else:
                            i+=1
                    elif event.key == pygame.K_UP:
                        if i==3:
                            i=0
                        elif i==4:
                            i=1
                    elif event.key == pygame.K_DOWN:
                        if i==0:
                            i=3
                        elif i in [1,2]:
                            i=4
                    elif event.key == pygame.K_RETURN:
                        if i==0:
                            Single_Player(Dificulty)
                        elif i==1:
                            Multi_Player()
                        elif i==2:
                            Rules()
                        elif i==3:
                            dif=1
                        elif i==4:
                            exit=1
            # *** Wyswietlanie komunikatu o wyjsciu badz trudnosci ***
            if exiting:
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        if j==0:
                            j=1
                        else:
                            j=0
                    elif event.key==pygame.K_RIGHT:
                        if j==1:
                            j=0
                        else:
                            j=1
                    elif event.key==pygame.K_RETURN:
                        if exit:
                            if j==0:
                                pygame.quit()
                                sys.exit()
                            else:
                                exiting=False
                                exit=0
                        elif dif:
                            if j==0:
                                Dificulty="Easy"
                                exiting = False
                                dif = 0
                            else:
                                Dificulty="Hard"
                                exiting = False
                                dif = 0
        # *** zajmuje sie poczatkowym polozeniem przycisku aby mozna bylo rysowac obramowki ***
        button=[(pointer[0], pointer[1]), (pointer[0]+200, pointer[1]), (pointer[0]+200,pointer[1]+50), (pointer[0], pointer[1]+50)]
        pygame.draw.lines(SCREEN, (255,255,255), True, button, 5)
        # *** Pytanie o wyjscie ***
        if exit==1:
            exit_p=[((resolution[0] / 2) - 130, (resolution[1] / 2) +10), ((resolution[0] / 2) + 30, (resolution[1] / 2) + 10)]
            p=exit_p[j]
            exit_button=[(p[0], p[1]), (p[0]+100, p[1]), (p[0]+100,p[1]+25), (p[0], p[1]+25)]
            messege("Czy na pewno chcesz wyjść?", (255, 255, 255),-25, size='medium')
            exiting=True
            pygame.draw.rect(SCREEN, (0, 57, 230), ((resolution[0] / 2) - 130, (resolution[1] / 2) +10, 100, 25))
            pygame.draw.rect(SCREEN, (0, 57, 230), ((resolution[0] / 2) + 30, (resolution[1] / 2) + 10, 100, 25))
            button_text("Tak", (255, 255, 0), (resolution[0] / 2) - 130, (resolution[1] / 2) +10, 100, 25)
            button_text("Nie", (255, 255, 0), (resolution[0] / 2) + 30, (resolution[1] / 2) + 10, 100, 25)
            pygame.draw.lines(SCREEN, (255, 255, 255), True, exit_button, 3)
        # *** Pytanie o trudnosc ***
        if dif==1:
            dif_p=[((resolution[0] / 2) - 300, (resolution[1] / 2) +200), ((resolution[0] / 2) + 100, (resolution[1] / 2) + 200)]
            d=dif_p[j]
            dif_button=[(d[0], d[1]), (d[0]+200, d[1]), (d[0]+200,d[1]+50), (d[0], d[1]+50)]
            messege("Wybierz poziom trudności?", (255, 255, 255),150, size='medium')
            exiting=True
            pygame.draw.rect(SCREEN, (0, 57, 230), ((resolution[0] / 2) - 300, (resolution[1] / 2) +200, 200, 50))
            pygame.draw.rect(SCREEN, (0, 57, 230), ((resolution[0] / 2) + 100, (resolution[1] / 2) + 200, 200, 50))
            button_text("Łatwy", (255, 255, 0), (resolution[0] / 2) - 300, (resolution[1] / 2) +200, 200, 50, size='menu')
            button_text("Trudny", (255, 255, 0), (resolution[0] / 2) + 100, (resolution[1] / 2) + 200, 200, 50, size='menu')
            pygame.draw.lines(SCREEN, (255, 255, 255), True, dif_button, 5)
        pygame.display.update()
def Rules():
    j=0
    while True:
        SCREEN.fill((31, 72, 210))
        messege("ZASADY", (255, 187, 51), -250, size='large')
        messege("Celem gry jest zatopienie wszystkich okrętów przeciwnika", (255, 187, 51), -200, size='medium')
        messege("Poruszasz się strzałkami, na początku ustaw swoje okręty: SPACE aby obrócić ENTER aby ustawić", (255, 187, 51), -140, size='menu')
        messege("Statki nie mogą się ze sobą sklejać (na ukos możliwe), gra nie informuje cię o zatopieniu", (255, 187, 51), -80, size='menu')
        messege("Strzał zatwierdzasz ENTER po trafieniu masz kolejną szansę, przy pudle zamiana tur",
                (255, 187, 51), -40, size='menu')
        messege("Czarna kropka oznacza pudło, czerwony krzyżyk oznacza trafienie",
                (255, 187, 51), 0, size='menu')
        messege("Floty graczy liczą:  jeden 5-masztowiec, dwa 4-masztowce",
                (255, 187, 51), 60, size='menu')
        messege("trzy 3-masztowce, cztery 2-masztowce, pięć 1-masztowcow",
                (255, 187, 51), 100, size='menu')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # *** Poruszanie sie po przyciskach ***
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if j == 0:
                        j = 1
                    else:
                        j = 0
                elif event.key == pygame.K_RIGHT:
                    if j == 1:
                        j = 0
                    else:
                        j = 1
                elif event.key == pygame.K_RETURN:
                    if j==0:
                        Menu()
                    if j==1:
                        Single_Player("Easy")
        # *** analogicznie do sytuacji w menu glownym rysuje przyciski i ramke na obecnym ***
        return_p = [((resolution[0] / 2) - 450, (resolution[1] / 2) + 150),
              ((resolution[0] / 2) + 150, (resolution[1] / 2) + 150)]
        r = return_p[j]
        return_button = [(r[0], r[1]), (r[0] + 300, r[1]), (r[0] + 300, r[1] + 100), (r[0], r[1] + 100)]
        pygame.draw.rect(SCREEN, (34, 177, 76), ((resolution[0] / 2) - 450, (resolution[1] / 2) + 150, 300, 100))
        pygame.draw.rect(SCREEN, (34, 177, 76), ((resolution[0] / 2) + 150, (resolution[1] / 2) + 150, 300, 100))
        button_text("Powrót do menu", (102, 0, 51), (resolution[0] / 2) - 450, (resolution[1] / 2) + 150, 300, 100, size='medium')
        button_text("Graj", (102, 0, 51), (resolution[0] / 2) + 150, (resolution[1] / 2) + 150, 300, 100, size='medium')
        pygame.draw.lines(SCREEN, (255, 255, 255), True, return_button, 5)
        pygame.display.update()
def Single_Player(Dificulty):
    delta = 0.0

    size = 5
    count = 0
    change = 1
    pointer_x = space  # wspolrzedne celownika gracza
    pointer_y = space
    start_x = space * 13  # wspolrzedne wskaznika ustawiajacego statki
    start_y = space
    set_orient = 1  # 0 pionowa orientacja wskaznika ustawiajacego, 1 pozioma

    Player_Turn = False
    PC_Turn = False
    Setting_Phase = True
    quick_menu=False
    PC_Ship = Hull()
    PC_Ships = []
    PC_shots = []
    PC_misses = []
    PC_water_taken=[]
    Player_Ship = Hull()
    Player_Shots = []
    Player_Misses = []
    Player_water_taken = []
    Player_Ships = []
    Possible_shots = []
    lines_list = []

    def setting_pointer(x, y, orient, size, color):
        if orient == 1:
            for i in range(size):
                pygame.draw.rect(SCREEN, color, (start_x + (i * space), start_y, space, space))
        elif orient == 0:
            for i in range(size):
                pygame.draw.rect(SCREEN, color, (start_x, start_y + (i * space), space, space))
    def adding(s, Ships):
        if s == 0:  # warunek stopu
            return Ships
        else:
            size = s
            z = s
            while z < 6:  # Kolejno tworzymy jednego 5-masztowy, dwa 4-mastowe itd.
                Ships.extend(PC_Ship.create_PC(size, PC_water_taken))
                z += 1
            return adding(s - 1, Ships)

    PC_Ships = adding(5, PC_Ships)
    near=[]
    searching = 1
    hits=0
    hit=0
    previous=(0,0)
    orient=""
    def shot_direction(x, y, orient):
        if x[0]==y[0]-space:
            orient="left"
            return (x[0]-space, x[1])
        if x[0]==y[0]+space:
            orient="right"
            return (x[0]+space, x[1])
        if x[1]==y[1]-space:
            orient="up"
            return (x[0], x[1]-space)
        if x[1]==y[1]+space:
            orient="down"
            return (x[0], x[1]+space)
    def other_side(x, orient, size):
        if orient=="left":
            return (x[0] + size*space, x[1])
        elif orient=="right":
            return (x[0]-size*space, x[1])
        elif orient=="up":
            return (x[0], x[1]+size*space)
        elif orient=="down":
            return (x[0], x[1]-size*space)

    for i in range(13, 23):
        lines_list.append(space * i)
    for i in lines_list:
        for j in range(0, 10):
            Possible_shots += [(i, lines_list[j] - 12 * space)]
    l=0
    quick=0
    while True:
        screen()
        button_text("komputer ", (0, 0, 153), (resolution[0] / 2) - 345, (resolution[1] / 2) + 265, 100, 25,
                    size='medium')
        button_text("gracz", (0, 0, 153), (resolution[0] / 2) + 251, (resolution[1] / 2) + 265, 100, 25,
                    size='medium')
        #messege("This might be the best pirate I've ever seen", (255, 187, 51), -275, size='medium')
        """
        for i in PC_Ships:
            Ships_x = i[0]
            Ships_y = i[1]
            SCREEN.fill((0, 0, 255), rect=(Ships_x, Ships_y, space, space))
        """
        if len(Player_Shots)==35:
            messege("Wygrywasz", (0, 204, 0), -275, size='medium')
            Setting_Phase = False
            Player_Turn = False
            PC_Turn = False
        if len(PC_shots)==35:
            messege("Przegrywasz!", (0, 204, 0), -275, size='medium')
            Setting_Phase = False
            Player_Turn = False
            PC_Turn = False
        if Player_Ships!=None:
            for j in Player_Ships:
                x=j[0]
                y=j[1]
                SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
        Shots_draw(list(set(PC_shots)))
        Misses_draw(list(set(PC_misses)))
        Shots_draw(list(set(Player_Shots)))
        Misses_draw(list(set(Player_Misses)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Setting_Phase:

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        start_x-=space
                    elif event.key == pygame.K_RIGHT:
                        start_x+=space
                    elif event.key == pygame.K_UP:
                        start_y-=space
                    elif event.key == pygame.K_DOWN:
                        start_y+=space
                    elif event.key == pygame.K_ESCAPE:
                        Setting_Phase=False
                        quick_menu=True
                        quick=1
                    elif event.key == pygame.K_SPACE:   # Zmiana orientacji wskaznika
                        if set_orient!=0:
                            set_orient=0
                        elif set_orient!=1:
                            set_orient=1

                    if event.key == pygame.K_RETURN and size>0:
                        if set_orient==0:
                            for i in range(0, size):
                                if (start_x, start_y + i*space) in Player_water_taken:
                                    break # msg
                            else:
                                Player_Ships += Player_Ship.create_player(start_x, start_y, set_orient, size, Player_water_taken)
                                count+=1

                        elif set_orient==1:
                            for i in range(0, size):
                                if (start_x + i*space, start_y) in Player_water_taken:
                                    break # msg
                            else:
                                Player_Ships += Player_Ship.create_player(start_x, start_y, set_orient, size, Player_water_taken)
                                count+=1

                        if count==6-size:
                            size-=1
                            count=0
                        if size==0:
                            Setting_Phase=False
                            Player_Turn=True
                # Ustawianie granic wskaznika
                if set_orient==0:
                    if start_x<space*13:
                        start_x=space*13
                    elif start_y<space:
                        start_y=space
                    elif start_x>=space*23:
                        start_x=space*22
                    elif start_y+((size-1)*space)>=space*11:
                        start_y=(space*10)-((size-1)*space)
                elif set_orient==1:
                    if start_x<space*13:
                        start_x=space*13
                    elif start_y<space:
                        start_y=space
                    elif start_y>=space*11:
                        start_y=space*10
                    elif start_x + ((size - 1) * space) >= space * 23:
                        start_x = (space * 22) - ((size - 1) * space)
            elif Player_Turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pointer_x-=space
                    elif event.key == pygame.K_RIGHT:
                        pointer_x+=space
                    elif event.key == pygame.K_UP:
                        pointer_y-=space
                    elif event.key == pygame.K_DOWN:
                        pointer_y+=space
                    elif event.key == pygame.K_ESCAPE:
                        Player_Turn = False
                        PC_Turn = False
                        quick_menu=True
                        quick=1
                    elif event.key==pygame.K_RETURN:
                        if (pointer_x, pointer_y) in Player_Shots or (pointer_x, pointer_y) in Player_Misses:
                            messege("Już tam strzelaleś!", (255, 204, 0), -275, size='medium')
                            pygame.display.update()
                            time.sleep(1)
                        elif (pointer_x, pointer_y) not in Player_Shots and (pointer_x, pointer_y) not in Player_Misses:
                            if (pointer_x, pointer_y) in PC_Ships:     # Zatwierdzanie trafien
                                Player_Shots += [(pointer_x, pointer_y)]
                                Player_Turn = True
                                PC_Turn = False
                                P_hit=1
                            else:   # Zatwierdzanie Pudel
                                Player_Misses += [(pointer_x, pointer_y)]
                                Player_Turn = False
                                PC_Turn = True
                                P_hit=0

                            start = 0.0
                            counter = 0
                            while start < 1.5:
                                start += clock.tick() / 1000.0
                                if start < 1.5:
                                    if counter == 0 and P_hit==1:
                                        messege("Trafiony!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1
                                    elif counter == 0 and P_hit==0:
                                        messege("Pudło!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1
                                elif start>1.5:
                                    #SCREEN.fill((32, 178, 170), rect=(0, 0, resolution[0], space))
                                    game_background()
                                    screen()
                                    button_text("komputer ", (0, 0, 153), (resolution[0] / 2) - 345,
                                                (resolution[1] / 2) + 265, 100, 25, size='medium')
                                    button_text("gracz", (0, 0, 153), (resolution[0] / 2) + 251,
                                                (resolution[1] / 2) + 265,
                                                100, 25, size='medium')
                                    if Player_Ships != None:
                                        for j in Player_Ships:
                                            x = j[0]
                                            y = j[1]
                                            SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
                                    Shots_draw(list(set(PC_shots)))
                                    Misses_draw(list(set(PC_misses)))
                                    Shots_draw(list(set(Player_Shots)))
                                    Misses_draw(list(set(Player_Misses)))
                                    pygame.display.update()

                # Ustawianie granic
                if pointer_x<space:
                    pointer_x=space
                elif pointer_x>=space*11:
                    pointer_x=space*10
                if pointer_y<space:
                    pointer_y=space
                elif pointer_y>=space*11:
                    pointer_y=space*10
            elif PC_Turn:
                if Dificulty=="Easy":
                    while not Player_Turn:

                        rand_shot=Possible_shots.pop(random.randint(0, len(Possible_shots)-1))

                        if rand_shot in Player_Ships:
                            PC_shots += [rand_shot]
                            hit = 1
                            Player_Turn = False
                            PC_Turn = True

                        else:
                            PC_misses += [rand_shot]
                            hit = 0
                            Player_Turn = True
                            PC_Turn = False
                        if len(PC_shots) == 35:
                            break
                        start=0.0
                        counter=0
                        while start<2.0:
                            start+=clock.tick()/1000.0
                            if start>0.5 and start<1.0:
                                Shots_draw(PC_shots)
                                Misses_draw(PC_misses)
                                pygame.display.update()
                            elif start>1.0 and start<2.0:
                                if hit and counter==0:
                                    messege("Dostaliśmy!", (255, 102, 0), -275, size="medium")
                                    pygame.display.update()
                                    counter=1
                                if not hit and counter==0:
                                    messege("Spudłowali!", (255, 102, 0), -275, size="medium")
                                    pygame.display.update()
                                    counter=1
                            elif start>2.0:
                                #SCREEN.fill((32, 178, 170), rect=(0, 0, resolution[0], space))
                                game_background()
                                screen()
                                button_text("komputer", (0, 0, 153), (resolution[0] / 2) - 345,
                                            (resolution[1] / 2) + 265, 100, 25, size='medium')
                                button_text("gracz", (0, 0, 153), (resolution[0] / 2) + 251, (resolution[1] / 2) + 265,
                                            100, 25, size='medium')
                                if Player_Ships != None:
                                    for j in Player_Ships:
                                        x = j[0]
                                        y = j[1]
                                        SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
                                Shots_draw(list(set(PC_shots)))
                                Misses_draw(list(set(PC_misses)))
                                Shots_draw(list(set(Player_Shots)))
                                Misses_draw(list(set(Player_Misses)))
                                pygame.display.update()

                elif Dificulty=="Hard":

                    while not Player_Turn:
                        if searching == 1 and len(near)==0:
                            rand_shot=Possible_shots.pop(random.randint(0, len(Possible_shots)-1))
                            near=nearby(rand_shot[0], rand_shot[1])
                            previous=rand_shot
                            hits=0
                        elif searching==1 and len(near)!=0:
                            rand_shot=near.pop(random.randint(0, len(near)-1))
                            while rand_shot not in Possible_shots:
                                rand_shot=near.pop(random.randint(0, len(near)-1))
                                if len(near)==0:
                                    rand_shot = Possible_shots[random.randint(0, len(Possible_shots) - 1)]
                                    near = nearby(rand_shot[0], rand_shot[1])
                            Possible_shots.remove(rand_shot)

                        if rand_shot in Player_Ships:
                            PC_shots += [rand_shot]
                            hits += 1
                            if hits>=2:
                                searching=0
                                x=rand_shot
                                rand_shot=shot_direction(rand_shot, previous, orient)
                                previous=x
                                if rand_shot not in Possible_shots:
                                    rand_shot=other_side(rand_shot, orient, hits+1)
                                    if rand_shot not in Possible_shots:
                                        rand_shot = Possible_shots[random.randint(0, len(Possible_shots) - 1)]
                                        near = nearby(rand_shot[0], rand_shot[1])
                                        searching=1
                                        hits=0
                                Possible_shots.remove(rand_shot)
                            Player_Turn = False
                            PC_Turn = True
                            hit=1
                        else:
                            PC_misses+=[rand_shot]
                            if hits==0:
                                near = []
                                searching = 1
                            if hits>=2:
                                previous=other_side(rand_shot, orient, hits)
                                rand_shot=other_side(rand_shot, orient, hits+1)
                                if rand_shot not in Player_Ships:
                                    hit=2
                                    near=[]
                                    hits=0
                                    searching=1

                            Player_Turn = True
                            PC_Turn = False
                            if hits==1 and len(near)==0:
                                hit=2
                            if hit !=2 or hits!=1:
                                hit=0
                        if len(PC_shots) == 35:
                            break
                        start = 0.0
                        counter = 0
                        while start < 2.0:
                            start += clock.tick() / 1000.0
                            if start > 0.5 and start < 1.0:
                                Shots_draw(PC_shots)
                                Misses_draw(PC_misses)
                                pygame.display.update()
                            elif start > 1.0 and start < 2.0:
                                if hit==1 and counter == 0:
                                    messege("Dostaliśmy!", (255, 102, 0), -275, size="medium")
                                    pygame.display.update()
                                    counter = 1
                                if hit==0 and counter == 0:
                                    messege("Spudłowali!", (255, 102, 0), -275, size="medium")
                                    pygame.display.update()
                                    counter = 1
                                if hit==2 and counter == 0:
                                    messege("Zatopili nas!", (255, 102, 0), -275, size="medium")
                                    pygame.display.update()
                                    counter = 1
                            elif start > 2.0:
                                #SCREEN.fill((32, 178, 170), rect=(0, 0, resolution[0], space))
                                game_background()
                                screen()
                                button_text("komputer", (0, 0, 153), (resolution[0] / 2) - 345,
                                            (resolution[1] / 2) + 265, 100, 25, size='medium')
                                button_text("gracz", (0, 0, 153), (resolution[0] / 2) + 251, (resolution[1] / 2) + 265,
                                            100, 25, size='medium')
                                if Player_Ships != None:
                                    for j in Player_Ships:
                                        x = j[0]
                                        y = j[1]
                                        SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
                                Shots_draw(list(set(PC_shots)))
                                Misses_draw(list(set(PC_misses)))
                                Shots_draw(list(set(Player_Shots)))
                                Misses_draw(list(set(Player_Misses)))
                                pygame.display.update()
            elif quick_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_DOWN:
                        l+=1
                        if l==3:
                            l=0
                    elif event.key==pygame.K_UP:
                        l-=1
                        if l==-1:
                            l=2
                    elif event.key==pygame.K_RETURN:
                        if l==0:
                            quick_menu = False
                            quick = 0
                            if len(Player_Ships)==35:
                                Player_Turn=True
                            else:
                                Setting_Phase=True
                        elif l==1:
                            Menu()
                        elif l==2:
                            pygame.quit()
                            sys.exit()
        if quick:
            menu_p = [((resolution[0] / 2)-45, (resolution[1] / 2) -100),
                      ((resolution[0] / 2)-45, resolution[1] / 2), ((resolution[0]/2)-45, (resolution[1]/2)+100)]
            m = menu_p[l]
            menu_button = [(m[0], m[1]), (m[0] + 90, m[1]), (m[0] + 90, m[1] + 30), (m[0], m[1] + 30)]
            messege("PAUZA", (255,0,0), -150, size='menu')
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2) -100, 90, 30))
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2), 90, 30))
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2) + 100, 90, 30))
            button_text("Wznów", (255, 204, 0), (resolution[0]/2)-45, (resolution[1]/2)-100, 90, 30, size='small')
            button_text("Menu", (255, 204, 0), (resolution[0] / 2)-45, (resolution[1] / 2), 90, 30, size='small')
            button_text("Wyjdź", (255, 204, 0), (resolution[0] / 2)-45, (resolution[1] / 2)+100, 90, 30, size='small')
            pygame.draw.lines(SCREEN, (255, 255, 255), True, menu_button, 2)

        delta += clock.tick() / 1000.0
        while delta > 0.5:
            delta -= 0.5
            change *= -1


        if Player_Turn:
            if change==-1:
                pygame.draw.rect(SCREEN, (255,255,255), (pointer_x, pointer_y, space, space))
        if Setting_Phase:
            if change == -1:
                setting_pointer(start_x, start_y, set_orient, size, (204, 151, 102))

        pygame.display.update()
def Multi_Player():
    start_x_1 = space
    start_y_1 = space
    start_x_2 = space*13
    start_y_2 = space
    pointer_x_1 = space
    pointer_y_1= space
    pointer_x_2 = space*13
    pointer_y_2 = space
    set_orient = 1
    delta = 0.0

    Setting_Phase_1 = True
    Setting_Phase_2 = False
    Player_1_Turn = False
    Player_2_Turn = False
    quick_menu=False
    current=0
    l=0
    quick=0
    size_1 = 5
    count_1 = 0
    size_2 = 5
    count_2 = 0
    change = 1
    Player_1_Ship = Hull()
    Player_2_Ship = Hull()
    Player_1_Shots = []
    Player_1_Misses = []
    Player_2_Shots = []
    Player_2_Misses = []
    Player_1_water_taken = []
    Player_2_water_taken = []
    Player_1_Ships = []
    Player_2_Ships = []
    def setting_pointer(x, y, orient, size, color):
        if orient == 1:
            for i in range(size):
                pygame.draw.rect(SCREEN, color, (x + (i * space), y, space, space))
        elif orient == 0:
            for i in range(size):
                pygame.draw.rect(SCREEN, color, (x, y + (i * space), space, space))
    while True:
        screen()
        button_text("gracz 2 ", (0, 0, 153), (resolution[0] / 2) -345, (resolution[1] / 2) +265, 100, 25, size='medium')
        button_text("gracz 1", (0, 0, 153), (resolution[0] / 2) + 251, (resolution[1] / 2) +265, 100, 25, size='medium')
        if len(Player_1_Shots)==35:
            messege("Wygrywa gracz 1!", (0, 204, 0), -275, size='medium')
            Setting_Phase_1 = False
            Setting_Phase_2 = False
            Player_1_Turn = False
            Player_2_Turn = False
            if Player_1_Ships!=None:
                for j in Player_1_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
            if Player_2_Ships!=None:
                for j in Player_2_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
        if len(Player_2_Shots)==35:
            messege("Wygrywa gracz 2!", (0, 204, 0), -275, size='medium')
            Setting_Phase_1 = False
            Setting_Phase_2 = False
            Player_1_Turn = False
            Player_2_Turn = False
            if Player_1_Ships!=None:
                for j in Player_1_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
            if Player_2_Ships!=None:
                for j in Player_2_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
        if Setting_Phase_1:
            if Player_1_Ships!=None:
                for j in Player_1_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
        if Setting_Phase_2:
            if Player_2_Ships!=None:
                for j in Player_2_Ships:
                    x=j[0]
                    y=j[1]
                    SCREEN.fill((128, 66, 0), rect=(x, y, space, space))
        Shots_draw(list(set(Player_1_Shots)))
        Misses_draw(list(set(Player_1_Misses)))
        Shots_draw(list(set(Player_2_Shots)))
        Misses_draw(list(set(Player_2_Misses)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Setting_Phase_1:

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        start_x_1-=space
                    elif event.key == pygame.K_RIGHT:
                        start_x_1+=space
                    elif event.key == pygame.K_UP:
                        start_y_1-=space
                    elif event.key == pygame.K_DOWN:
                        start_y_1+=space

                    elif event.key == pygame.K_SPACE:   # Zmiana orientacji wskaznika
                        if set_orient!=0:
                            set_orient=0
                        elif set_orient!=1:
                            set_orient=1
                    elif event.key == pygame.K_ESCAPE:
                        quick_menu = True
                        quick = 1
                        current='Setting_Phase_1'
                        Setting_Phase_1=False


                    if event.key == pygame.K_RETURN and size_1>0:
                        if set_orient==0:
                            for i in range(0, size_1):
                                if (start_x_1, start_y_1 + i*space) in Player_1_water_taken:
                                    break # msg
                            else:
                                Player_1_Ships += Player_1_Ship.create_player(start_x_1, start_y_1, set_orient, size_1, Player_1_water_taken)
                                count_1+=1

                        elif set_orient==1:
                            for i in range(0, size_1):
                                if (start_x_1 + i*space, start_y_1) in Player_1_water_taken:
                                    break # msg
                            else:
                                Player_1_Ships += Player_1_Ship.create_player(start_x_1, start_y_1, set_orient, size_1, Player_1_water_taken)
                                count_1+=1

                        if count_1==6-size_1:
                            size_1-=1
                            count_1=0
                        if size_1==0:
                            Setting_Phase_1=False
                            Setting_Phase_2=True

                if set_orient==0:
                    if start_x_1<space*13:
                        start_x_1=space*13
                    elif start_y_1<space:
                        start_y_1=space
                    elif start_x_1>=space*23:
                        start_x_1=space*22
                    elif start_y_1+((size_1-1)*space)>=space*11:
                        start_y_1=(space*10)-((size_1-1)*space)
                elif set_orient==1:
                    if start_x_1<space*13:
                        start_x_1=space*13
                    elif start_y_1<space:
                        start_y_1=space
                    elif start_y_1>=space*11:
                        start_y_1=space*10
                    elif start_x_1 + ((size_1 - 1) * space) >= space * 23:
                        start_x_1 = (space * 22) - ((size_1 - 1) * space)
            elif Setting_Phase_2:

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        start_x_2-=space
                    elif event.key == pygame.K_RIGHT:
                        start_x_2+=space
                    elif event.key == pygame.K_UP:
                        start_y_2-=space
                    elif event.key == pygame.K_DOWN:
                        start_y_2+=space

                    elif event.key == pygame.K_SPACE:   # Zmiana orientacji wskaznika
                        if set_orient!=0:
                            set_orient=0
                        elif set_orient!=1:
                            set_orient=1
                    elif event.key == pygame.K_ESCAPE:
                        quick_menu = True
                        quick = 1
                        current='Setting_Phase_2'
                        Setting_Phase_2=False

                    if event.key == pygame.K_RETURN and size_2>0:
                        if set_orient==0:
                            for i in range(0, size_2):
                                if (start_x_2, start_y_2 + i*space) in Player_2_water_taken:
                                    break # msg
                            else:
                                Player_2_Ships += Player_2_Ship.create_player(start_x_2, start_y_2, set_orient, size_2, Player_2_water_taken)
                                count_2+=1

                        elif set_orient==1:
                            for i in range(0, size_2):
                                if (start_x_2 + i*space, start_y_2) in Player_2_water_taken:
                                    break # msg
                            else:
                                Player_2_Ships += Player_2_Ship.create_player(start_x_2, start_y_2, set_orient, size_2, Player_2_water_taken)
                                count_2+=1

                        if count_2==6-size_2:
                            size_2-=1
                            count_2=0
                        if size_2==0:
                            Setting_Phase_2=False
                            Player_1_Turn=True

                if set_orient==0:
                    if start_x_2<space:
                        start_x_2=space
                    elif start_y_2<space:
                        start_y_2=space
                    elif start_x_2>=space*11:
                        start_x_2=space*10
                    elif start_y_2+((size_2-1)*space)>=space*11:
                        start_y_2=(space*10)-((size_2-1)*space)
                elif set_orient==1:
                    if start_x_2<space:
                        start_x_2=space
                    elif start_y_2<space:
                        start_y_2=space
                    elif start_y_2>=space*11:
                        start_y_2=space*10
                    elif start_x_2 + ((size_2 - 1) * space) >= space * 11:
                        start_x_2 = (space * 10) - ((size_2 - 1) * space)
            elif Player_1_Turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pointer_x_1-=space
                    elif event.key == pygame.K_RIGHT:
                        pointer_x_1+=space
                    elif event.key == pygame.K_UP:
                        pointer_y_1-=space
                    elif event.key == pygame.K_DOWN:
                        pointer_y_1+=space
                    elif event.key == pygame.K_ESCAPE:
                        quick_menu = True
                        quick = 1
                        current='Player_1_Turn'
                        Player_1_Turn=False

                    elif event.key==pygame.K_RETURN:
                        if (pointer_x_1, pointer_y_1) in Player_1_Shots or (pointer_x_1, pointer_y_1) in Player_1_Misses:
                            messege("Już tam strzelaleś!", (255, 204, 0), -275, size='medium')
                            pygame.display.update()
                            time.sleep(1)
                        elif (pointer_x_1, pointer_y_1) not in Player_1_Shots and (pointer_x_1, pointer_y_1) not in Player_1_Misses:
                            if (pointer_x_1, pointer_y_1) in Player_2_Ships:     # Zatwierdzanie trafien
                                Player_1_Shots += [(pointer_x_1, pointer_y_1)]
                                Player_1_Turn = True
                                Player_2_Turn = False
                                P_hit=1
                            else:   # Zatwierdzanie Pudel
                                Player_1_Misses += [(pointer_x_1, pointer_y_1)]
                                Player_1_Turn = False
                                Player_2_Turn = True
                                P_hit=0

                            start = 0.0
                            counter = 0
                            while start < 1.0:
                                start += clock.tick() / 1000.0
                                if start < 1.0:
                                    if counter == 0 and P_hit==1:
                                        messege("Trafiony!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1
                                    elif counter == 0 and P_hit==0:
                                        messege("Pudło!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1

                # Ustawianie granic
                if pointer_x_1<space:
                    pointer_x_1=space
                elif pointer_x_1>=space*11:
                    pointer_x_1=space*10
                if pointer_y_1<space:
                    pointer_y_1=space
                elif pointer_y_1>=space*11:
                    pointer_y_1=space*10
            elif Player_2_Turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pointer_x_2-=space
                    elif event.key == pygame.K_RIGHT:
                        pointer_x_2+=space
                    elif event.key == pygame.K_UP:
                        pointer_y_2-=space
                    elif event.key == pygame.K_DOWN:
                        pointer_y_2+=space
                    elif event.key == pygame.K_ESCAPE:
                        quick_menu = True
                        quick = 1
                        current='Player_2_Turn'
                        Player_2_Turn=False

                    elif event.key==pygame.K_RETURN:
                        if (pointer_x_2, pointer_y_2) in Player_2_Shots or (pointer_x_2, pointer_y_2) in Player_2_Misses:
                            messege("Już tam strzelaleś!", (255, 204, 0), -275, size='medium')
                            pygame.display.update()
                            time.sleep(1)
                        elif (pointer_x_2, pointer_y_2) not in Player_2_Shots and (pointer_x_2, pointer_y_2) not in Player_2_Misses:
                            if (pointer_x_2, pointer_y_2) in Player_1_Ships:     # Zatwierdzanie trafien
                                Player_2_Shots += [(pointer_x_2, pointer_y_2)]
                                Player_2_Turn = True
                                Player_1_Turn = False
                                P_hit=1
                            else:   # Zatwierdzanie Pudel
                                Player_2_Misses += [(pointer_x_2, pointer_y_2)]
                                Player_2_Turn = False
                                Player_1_Turn = True
                                P_hit=0

                            start = 0.0
                            counter = 0
                            while start < 1.0:
                                start += clock.tick() / 1000.0
                                if start < 1.0:
                                    if counter == 0 and P_hit==1:
                                        messege("Trafiony!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1
                                    elif counter == 0 and P_hit==0:
                                        messege("Pudło!", (255, 204, 0), -275, size='medium')
                                        pygame.display.update()
                                        counter = 1

                # Ustawianie granic
                if pointer_x_2<space*13:
                    pointer_x_2=space*13
                elif pointer_x_2>=space*23:
                    pointer_x_2=space*22
                if pointer_y_2<space:
                    pointer_y_2=space
                elif pointer_y_2>=space*11:
                    pointer_y_2=space*10
            elif quick_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        l += 1
                        if l == 3:
                            l = 0
                    elif event.key == pygame.K_UP:
                        l -= 1
                        if l == -1:
                            l = 2
                    elif event.key == pygame.K_RETURN:
                        if l == 0:
                            if current=='Setting_Phase_1':
                                Setting_Phase_1=True
                            elif current=='Setting_Phase_2':
                                Setting_Phase_2=True
                            elif current=='Player_1_Turn':
                                Player_1_Turn=True
                            elif current=='Player_2_Turn':
                                Player_2_Turn=True
                            quick_menu = False
                            quick = 0
                        elif l == 1:
                            Menu()
                        elif l == 2:
                            pygame.quit()
                            sys.exit()
        if quick:
            menu_p = [((resolution[0] / 2) - 45, (resolution[1] / 2) - 100),
                      ((resolution[0] / 2) - 45, resolution[1] / 2),
                      ((resolution[0] / 2) - 45, (resolution[1] / 2) + 100)]
            m = menu_p[l]
            menu_button = [(m[0], m[1]), (m[0] + 90, m[1]), (m[0] + 90, m[1] + 30), (m[0], m[1] + 30)]
            messege("PAUZA", (255, 0, 0), -150, size='menu')
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2) - 100, 90, 30))
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2), 90, 30))
            pygame.draw.rect(SCREEN, (204, 0, 153), ((resolution[0] / 2) - 45, (resolution[1] / 2) + 100, 90, 30))
            button_text("Wznów", (255, 204, 0), (resolution[0] / 2) - 45, (resolution[1] / 2) - 100, 90, 30,
                        size='small')
            button_text("Menu", (255, 204, 0), (resolution[0] / 2) - 45, (resolution[1] / 2), 90, 30, size='small')
            button_text("Wyjdź", (255, 204, 0), (resolution[0] / 2) - 45, (resolution[1] / 2) + 100, 90, 30,
                        size='small')
            pygame.draw.lines(SCREEN, (255, 255, 255), True, menu_button, 2)

        delta += clock.tick() / 1000.0
        while delta > 0.5:
            delta -= 0.5
            change *= -1

        if Player_1_Turn:
            if change==-1:
                pygame.draw.rect(SCREEN, (255,255,255), (pointer_x_1, pointer_y_1, space, space))
        if Player_2_Turn:
            if change==-1:
                pygame.draw.rect(SCREEN, (255,255,255), (pointer_x_2, pointer_y_2, space, space))

        if Setting_Phase_1:
            if change == -1:
                setting_pointer(start_x_1, start_y_1, set_orient, size_1, (191, 125, 64))
        if Setting_Phase_2:
            if change == -1:
                setting_pointer(start_x_2, start_y_2, set_orient, size_2, (191, 125, 64))
        pygame.display.update()
Menu()
