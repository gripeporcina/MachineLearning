# -*- coding: utf-8 -*-
import pygame
import sys

# Player button codes
# 1 for left click
# 2 for right click
# So the first player will use the
# first click, and the second player
# the right one.
PLAYER_1 = 1
PLAYER_2 = 3

class Chess:
    def __init__(self, *args, **kwargs):
        pygame.init()
        self.colors = kwargs.get('colors', [(255,255,255), (0,0,0)])
        self.rectangle_dragin = kwargs.get('rectangle_dragin', False)
        self.n = kwargs.get('board_size', 8)       
        self.surface_sz = kwargs.get('surface_sz', 480)
        
        self.sq_sz = self.surface_sz // self.n
        self.surface_sz = self.n * self.sq_sz     
        self.surface = pygame.display.set_mode((self.surface_sz, self.surface_sz))

        player_1_piece = kwargs.get('player_1_piece', "static/Ficha_Naranja.jpeg")
        player_2_piece = kwargs.get('player_2_piece', "static/Ficha_Azul.jpeg")
        self.players = {
            'player_1': { 'piece': pygame.image.load(player_1_piece) },
            'player_2': { 'piece': pygame.image.load(player_2_piece) }
        }
        self.ball_offset = kwargs.get('ball_offset', 
                                      (self.sq_sz - self.players['player_1']['piece'].get_width()) 
                                       // 2)
        self._prepare_table()

    def _prepare_table(self, *args, **kwargs):
        self.table = []
        all_x = all_y = [i * self.sq_sz for i in range(self.n)]
        white = True
        for x in all_x:
            for y in all_y:
                c_index = 0 if white is True else 1
                self.table.append({
                    'coords': [x, y, x + 60, y + 60],
                    'color': self.colors[c_index],
                    'occupied': None  # Values will be: 'player_1', 'player_2' or 'None'
                })
                white = not white
            # Quick hack XD!!!
            white = not white

    def _draw_table(self, *args, **kwargs):
        for quadrant in self.table:
            self.surface.fill(quadrant['color'], quadrant['coords'])

    def main_loop(self, *args, **kwargs):
        # This is the main loop for the game
        # player_1_piece = self.players['player_1']['piece']
        # player_2_piece = self.players['player_2']['piece']
        while True:
            ev = pygame.event.get()
            self._draw_table()
            for event in ev:
                if not event.__dict__:
                    # Closing game
                    sys.exit(0)
                if event.__dict__.get('button', False) == PLAYER_1:
                    print(self.table)
            pygame.display.flip()
