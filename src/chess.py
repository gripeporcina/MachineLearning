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
            'player_1': { 
                'coords': [4, 6, 13, 15, 22, 31],
                'piece': pygame.image.load(player_1_piece) 
            },
            'player_2': { 
                'coords': [32, 41, 48, 50, 57, 59],
                'piece': pygame.image.load(player_2_piece) 
            }
        }
        self.ball_offset = kwargs.get('ball_offset', 
                                      (self.sq_sz - self.players['player_1']['piece'].get_width()) 
                                       // 2)
        self._prepare_table()
        self._prepare_chess_pieces()

    def _prepare_table(self, *args, **kwargs):
        self.table = []
        all_x = all_y = [i * self.sq_sz for i in range(self.n)]
        white = True

        """
        Setting up the base table
        """
        for x in all_x:
            for y in all_y:
                c_index = 0 if white is True else 1
                self.table.append({
                    'coords': [x, y, x + 60, y + 60],
                    'color': self.colors[c_index],
                    'occupied': None  # Values will be: 'player_1', 'player_2' or 'None'
                })
                white = not white
            white = not white

    def _prepare_chess_pieces(self, *args, **kwargs):
        p1_piece = self.players['player_1']['piece']
        p2_piece = self.players['player_2']['piece']

        for piece in self.players['player_1']['coords']:
            self.table[piece]['occupied'] = 'player_1'
            self.surface.blit(p1_piece, self.table[piece]['coords'])

        for piece in self.players['player_2']['coords']:
            self.table[piece]['occupied'] = 'player_2'
            self.surface.blit(p2_piece, self.table[piece]['coords'])

    def _draw_table(self, *args, **kwargs):
        for quadrant in self.table:
            self.surface.fill(quadrant['color'], quadrant['coords'])

    def _draw_chess_pieces(self, *args, **kwargs):
        self._prepare_chess_pieces()

    def _player_is_selecting_piece(self, event, *args, **kwargs):
        p1_piece = self.players['player_1']['piece']
        piece_in_collision = None
        for piece in self.players['player_1']['coords']:
            found_collision = self.surface \
                .blit(p1_piece, self.table[piece]['coords']) \
                .collidepoint(event.pos)
            if found_collision:
                piece_in_collision = piece
        return piece_in_collision

    def main_loop(self, *args, **kwargs):
        # This is the main loop for the game
        while True:
            ev = pygame.event.get()
            self._draw_table()
            self._draw_chess_pieces()
            for event in ev:
                if not event.__dict__:
                    sys.exit(0)
                if event.__dict__.get('button', False) == PLAYER_1:
                    piece_in_collision = self._player_is_selecting_piece(event)
                    if piece_in_collision:
                        print('Player is selecting a piece: ' + str(piece_in_collision))
            pygame.display.flip()
