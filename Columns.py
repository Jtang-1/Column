#Columns
#Jonathan Tang 85625237

from game_mechanic import Jewel,Faller,GameState,Field
import Game_model
import pygame

_FIELD_COLUMNS = 6
_FIELD_ROWS = 13
_FRAME_RATE = 60
_INITIAL_HEIGHT = 800
_INITIAL_WIDTH = 370
_BACKGROUND_COLOR = pygame.Color(220,250,255)

class Columns:
    def __init__(self):
        self._state = GameState(_FIELD_ROWS,_FIELD_COLUMNS)
        self._state.new_game_field()
        self._running = True
        
    def run(self)-> None:
        pygame.init()
        try:
            clock = pygame.time.Clock()
            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            self._draw_frame()
            while self._running:
                self.new_faller = Game_model.random_faller(self._state)
                tick = 0
                while (self.new_faller.get_faller_state() != "FROZEN"):
                    
#                    self._state.display_field()
                    clock.tick(_FRAME_RATE)
                    self._handle_events()
                    self._state.place_faller_on_board(self.new_faller)
                    self._draw_frame()
                    tick +=1
                    if tick >60:
                        if self._state.empty_below_faller(self.new_faller):
                            self._state.drop_faller_one_down(self.new_faller)
                            self._state.update_faller_state(self.new_faller)
                            tick = 0
                        else:
                            self._state.place_faller_on_board(self.new_faller)
                            self._state.update_faller_state(self.new_faller)
                            tick = 0
                    
                while Game_model.check_match(self._state):
                    pass
                while Game_model.check_match(self._state):
                    pass
                self._draw_frame()
                clock.tick(_FRAME_RATE)
                if self._state.not_frozen_or_faller_in_field(self.new_faller) != True:
                    self._running = False

                                                                                            
                
        finally:
            pygame.quit()
            
    def _create_surface(self,size:(int,int)) -> None:
        self._surface = pygame.display.set_mode(size,pygame.RESIZABLE)
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)


    def _handle_event(self,event) -> None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._state.move_faller_left(self.new_faller)
            if event.key == pygame.K_RIGHT:
                self._state.move_faller_right(self.new_faller)
            if event.key == pygame.K_UP:
                self._state.rotate_faller(self.new_faller)
            if event.key == pygame.K_DOWN:
                if self._state.empty_below_faller(self.new_faller):
                    self._state.drop_faller_one_down(self.new_faller)
                    self._state.update_faller_state(self.new_faller)
        
    def _handle_keys(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self._state.move_faller_left(self.new_faller)

        if keys[pygame.K_RIGHT]:
            self._state.move_faller_right(self.new_faller)
    

    def _draw_field(self) -> None:
        line_color = pygame.Color(0,0,0)

        top_left_frac_x,top_left_frac_y = self._state.field_object().top_left()
        self.field_top_left_pixel_x = self._frac_x_to_pixel_x(top_left_frac_x)
        self.field_top_left_pixel_y = self._frac_y_to_pixel_y(top_left_frac_y)

        self.field_width_pixel = self._frac_x_to_pixel_x(self._state.field_object().width())
        self.field_height_pixel = self._frac_y_to_pixel_y(self._state.field_object().height())

        self.field_bottom_right_pixel_x = self.field_top_left_pixel_x + self.field_width_pixel
        self.field_bottom_right_pixel_y = self.field_top_left_pixel_y + self.field_height_pixel
        
        field_rect = pygame.Rect(
            self.field_top_left_pixel_x,self.field_top_left_pixel_y,
            self.field_width_pixel,self.field_height_pixel)
            
                         
        grid_width_frac = self._state.field_object().grid_width()
        grid_height_frac = self._state.field_object().grid_height()

        self.grid_width_pixel = self._frac_x_to_pixel_x(grid_width_frac)
        self.grid_height_pixel = self._frac_y_to_pixel_y(grid_height_frac)
                         
        surface_height_pixel = self._surface.get_height()
        surface_width_pixel = self._surface.get_width()

        x_pos = self.field_top_left_pixel_x
        while x_pos < self.field_width_pixel + self.grid_width_pixel:
            #Draws vertical lines
            pygame.draw.line(self._surface, line_color,
                             (x_pos,self.field_top_left_pixel_y),
                             (x_pos,self.field_bottom_right_pixel_y),1)
            x_pos += self.grid_width_pixel

            
        y_pos = self.field_top_left_pixel_y
        while y_pos < self.field_height_pixel+self.grid_height_pixel:
            #Draws horizontal lines
            pygame.draw.line(self._surface, line_color,
                             (self.field_top_left_pixel_x,y_pos),
                             (self.field_bottom_right_pixel_x,y_pos),1)
            y_pos += self.grid_height_pixel

    def _draw_jewels(self) -> None:
        pass
        # Reads model field and draws jewels. Goes from top left to bottom right
        # Gets the top left x and y coordinate of top left jewel
        jewel_top_left_pixel_y = self.field_top_left_pixel_y
        
        for row in range(self._state.get_field_height()):
            jewel_top_left_pixel_x = self.field_top_left_pixel_x 
            for col in range(self._state.get_field_width()):
                if self._state.is_empty(row,col):
                    pass
                else:
                    jewel = self._state.jewel_in_pos(row,col)
                    jewel_state = jewel.get_state()
                    jewel_rect = pygame.Rect(
                        jewel_top_left_pixel_x,jewel_top_left_pixel_y,
                        self.grid_width_pixel,self.grid_height_pixel)
                    if jewel_state == "FROZEN":
                        pygame.draw.rect(self._surface,self.jewel_color(jewel),jewel_rect,0)     
                        pygame.draw.rect(self._surface,pygame.Color(255,255,255),jewel_rect,3)

                    else:
                        pygame.draw.rect(self._surface,self.jewel_color(jewel),jewel_rect,0)
                        pygame.draw.rect(self._surface,pygame.Color(0,0,0),jewel_rect,3)

                jewel_top_left_pixel_x += self.grid_width_pixel
            jewel_top_left_pixel_y += self.grid_height_pixel
                
    def _draw_frame(self) -> None:
        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_field()
        self._draw_jewels()
        pygame.display.flip()
        
    def jewel_color(self,jewel:Jewel) -> pygame.Color:
     #   if jewel's letter is something
        a_color = pygame.Color(255,0,0)
        b_color = pygame.Color(0,255,0)
        c_color = pygame.Color(0,0,255)
        d_color = pygame.Color(255,255,0)
        e_color = pygame.Color(255,167,3)
        f_color = pygame.Color(33,33,33)
        g_color = pygame.Color(155,0,255)
        
        color_dictionary = {"A":a_color,
                            "B":b_color,
                            "C":c_color,
                            "D":d_color,
                            "E":e_color,
                            "F":f_color,
                            "G":g_color
                            }

        return color_dictionary[jewel.get_color()]
        
    def _stop_running(self) -> None:
        self._running = False

    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        return self._frac_to_pixel(frac_x, self._surface.get_width())

    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        return self._frac_to_pixel(frac_y, self._surface.get_height())

    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        return int(frac * max_pixel)
    
if __name__ == '__main__':
    Columns().run()
