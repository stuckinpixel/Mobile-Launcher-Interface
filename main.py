
import pygame, sys, time, random, json, math, os
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 350, 600
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption("Mobile Launcher Design")

APP_ICON_SIZE = 50
APP_GRID_CONTAINER_PERCENTAGE_FOR_APP = 0.75
DRAWER_HEIGHT = 100
grid_height = HEIGHT-DRAWER_HEIGHT
each_app_container_size = APP_ICON_SIZE/APP_GRID_CONTAINER_PERCENTAGE_FOR_APP
ROWS = int(grid_height/each_app_container_size)
COLS = int(WIDTH/each_app_container_size)




class Wallpaper:
    def __init__(self, image=None, name=""):
        self.image = image
        self.name = name

class Wallpapers:
    def __init__(self):
        self.images = []
        self.path = "src/images/wallpapers/"
        self.load_images()
        self.cursor = 2
    def load_images(self):
        self.images = []
        for image_file_name in os.listdir(self.path):
            img = pygame.image.load(self.path+image_file_name)
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            new_wallpaper = Wallpaper(img)
            self.images.append(new_wallpaper)
    def set_wallpaper(self, index):
        self.cursor = index
    def get_image(self):
        return self.images[self.cursor].image

class Icon:
    def __init__(self, name):
        self.image = None
        self.name = name
        self.size = (APP_ICON_SIZE, APP_ICON_SIZE)
    def set_image(self, path_file_name):
        img = pygame.image.load(path_file_name)
        img = pygame.transform.scale(img, self.size)
        self.image = img


class App:
    def __init__(self, app_name):
        self.app = app_name
        self.icon = Icon(app_name)

class Drawer:
    def __init__(self):
        self.apps_count = 5
        self.apps = []
        self.height = DRAWER_HEIGHT
        self.add_initial_apps()
    def add_initial_apps(self):
        self.apps = []
        for _ in range(self.apps_count):
            new_app = App("")
            self.apps.append(new_app)

class HomeScreenGridApps:
    def __init__(self):
        self.matrix = [[]]
        self.initialize_matrix()
    def initialize_matrix(self):
        self.matrix = [ [None for __ in range(COLS)] for _ in range(ROWS) ]
        print (self.matrix)

class HomeScreen:
    def __init__(self):
        self.drawer = Drawer()
        self.grid = HomeScreenGridApps()


class Phone:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "loading": (40, 180, 140),
            "sky": (40, 140, 180),
            "grass": (40, 180, 80)
        }
        self.wallpapers = None
        self.drag_counts = 0
        self.drag_positions = []
        self.initialize()
        self.home_screen = HomeScreen()
    def initialize(self):
        self.wallpapers = Wallpapers()
    def get_drag_direction(self, drag_positions):
        if len(drag_positions)>0:
            initial_point = drag_positions[0][:]
            current_point = [self.mouse[0], self.mouse[1]]
            if initial_point!=current_point:
                x_div = current_point[0]-initial_point[0]
                x_dir = (x_div)/0.1
                if abs(x_div)!=0:
                    x_dir = int(x_div/abs(x_div))
                y_div = current_point[1]-initial_point[1]
                y_dir = (y_div)/0.1
                if abs(y_div)!=0:
                    y_dir = int(y_div/abs(y_div))
                return [x_dir, y_dir]
        return [0, 0]
    def distance_between_two_points(self, p1, p2):
        return int(math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)))
    def get_strength(self):
        if len(self.drag_positions)>0:
            initial_point = self.drag_positions[0][:]
            current_point = [self.mouse[0], self.mouse[1]]
            return self.distance_between_two_points(initial_point, current_point)
        return 0
    def on_drag_ending(self):
        direction = self.get_drag_direction(self.drag_positions[:])
        strength = self.get_strength()
        print (strength, direction)
    def on_dragging(self):
        pass
    def check_dragging(self):
        if self.click[0]==1:
            click_position = [self.mouse[0], self.mouse[1]]
            if click_position not in self.drag_positions:
                self.drag_positions.append(click_position[:])
            if len(self.drag_positions)>1:
                self.on_dragging()
        else:
            if len(self.drag_positions)>1:
                self.on_drag_ending()
                self.drag_positions = []
    def draw_wallpaper(self):
        self.surface.blit(self.wallpapers.get_image(), (0, 0))
    def action(self):
        self.check_dragging()
    def render(self):
        self.draw_wallpaper()
    def run(self):
        while self.play:
            self.surface.fill(self.color["sky"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
            #--------------------------------------------------------------
            self.action()
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    phone = Phone(surface)
    phone.run()






