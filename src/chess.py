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
        pygame.display.set_caption(kwargs.get('title', 'Damas en 6 esquinas'))
        self.colors = kwargs.get('colors', [(255,255,255), (0,0,0)])
        self.possible_move_colors = kwargs.get('possible_move_colors', [(255,0,0), (0,255,0)])
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
        self._prepare_pieces()

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

    def _prepare_pieces(self, *args, **kwargs):
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

    def _draw_pieces(self, *args, **kwargs):
        self._prepare_pieces()

    def _draw_possible_moves(self, possible_moves, *args, **kwargs):
        for move in possible_moves:
            move_idx = move['move']
            coords = [
                self.table[move_idx]['coords'][0],
                self.table[move_idx]['coords'][1],
                self.sq_sz,
                self.sq_sz,
            ]
            print(coords)
            self.surface.fill(self.possible_move_colors[0], coords)

    def _player_is_selecting_piece(self, event=None, *args, **kwargs):
        p1_piece = self.players['player_1']['piece']
        piece_in_collision = None

        for piece in self.players['player_1']['coords']:
            found_collision = self.surface \
                .blit(p1_piece, self.table[piece]['coords']) \
                .collidepoint(event.pos)
            if found_collision:
                piece_in_collision = piece
                break

        if piece_in_collision:
            return self.players['player_1']['coords'].index(piece_in_collision)
        else:
            return False

    def _quadrant_is_empty(self, quadrant=None, *args, **kwargs):
        print()
        print('==================================================')        
        print(self.table[quadrant]['coords'])
        print(self.table[quadrant]['occupied'])
        print('==================================================')
        print()

    def _piece_is_in_edge(self, move, *args, **kwargs):
        if move % self.n == 0:
            # Top edge
            return 't'
        elif move % self.n == self.n - 1:
            # Bottom edge
            return 'b'
        elif move - self.n < 0:
            # Left edge
            return 'l'
        elif move + self.n > self.n * self.n:
            # Right edge
            return 'r'
        else:
            # all others
            return None

    def _calculate_possible_moves_jumping_piece(self, possible_move, *args, **kwargs):
        if possible_move is None:
            return None

        if possible_move['move'] < 0 or possible_move['move'] > self.n * self.n:
            return None

        if possible_move['move'] in self.players['player_1']['coords']:
            return None
        elif possible_move['move'] in self.players['player_2']['coords']:
            return None

        return possible_move

    def _calculate_possible_moves_for(self, move, *args, **kwargs):
        possible_moves = []
        in_edge = self._piece_is_in_edge(move)

        if in_edge == 't':
            # Top edge
            possible_moves.append({'move': move + (self.n + 1), 'type': 'right'})
        elif in_edge == 'b':
            # Bottom edge
            possible_moves.append({'move': move - (self.n + 1), 'type': 'left'})
            possible_moves.append({'move': move + (self.n - 1), 'type': 'forward'})
        elif in_edge == 'l':
            # Left edge
            possible_moves.append({'move': move + (self.n - 1), 'type': 'forward'})
            possible_moves.append({'move': move + (self.n + 1), 'type': 'right'})
        elif in_edge == 'r':
            # Right edge
            possible_moves.append({'move': move - (self.n + 1), 'type': 'left'})
        else:
            # all others
            possible_moves.append({'move': move - (self.n + 1), 'type': 'left'})
            possible_moves.append({'move': move + (self.n - 1), 'type': 'forward'})
            possible_moves.append({'move': move + (self.n + 1), 'type': 'right'})
        return possible_moves

    def _calculate_possible_moves(self, piece_idx, *args, **kwargs):
        player_piece = self.players['player_1']['coords'][piece_idx]
        possible_moves = self._calculate_possible_moves_for(player_piece)
        new_possible_moves = []

        for possible_move in possible_moves:
            try:
                self.players['player_1']['coords'].index(possible_move['move'])
                if possible_move['type'] == 'left':
                    if possible_move['move'] in [0, 16, 32, 48,
                                                 15, 13, 11, 9]:
                        possible_move = None
                    else:
                        possible_move = {
                            'last_move': possible_move,
                            'move': possible_move['move'] - (self.n + 1),
                            'type': possible_move['type']
                        }
                elif possible_move['type'] == 'right':
                    if possible_move['move'] in [15, 31, 47,
                                                 57, 59, 61, 63]:
                        possible_move = None
                    else:
                        possible_move = {
                            'last_move': possible_move,
                            'move': possible_move['move'] + (self.n + 1),
                            'type': possible_move['type'],
                        }
                elif possible_move['type'] == 'forward':
                    if possible_move['move'] in [0, 16, 32, 48,
                                                 57, 59, 61, 63]:
                        possible_move = None
                    else:
                        possible_move = {
                            'last_move': possible_move,
                            'move': possible_move['move'] + (self.n - 1),
                            'type': possible_move['type'],
                        }
                possible_move = self._calculate_possible_moves_jumping_piece(possible_move)
                if possible_move is not None:
                    new_possible_moves.append(possible_move)
            except ValueError:
                new_possible_moves.append(possible_move)
        return new_possible_moves

    def main_loop(self, *args, **kwargs):
        # This is the main loop for the game
        possible_moves = []
        while True:
            ev = pygame.event.get()
            self._draw_table()
            self._draw_pieces()

            if possible_moves:
                self._draw_possible_moves(possible_moves)

            for event in ev:
                if not event.__dict__:
                    sys.exit(0)
                if (event.__dict__.get('button', False) == PLAYER_1
                    and event.type == pygame.MOUSEBUTTONUP):
                    piece_in_collision = self._player_is_selecting_piece(event=event)
                    if piece_in_collision is not False:
                        possible_moves = self._calculate_possible_moves(piece_in_collision)
            pygame.display.flip()
