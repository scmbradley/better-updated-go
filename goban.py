#!/usr/bin/env python
# coding: utf-8

"""Goban for B.U.G.

This is the main file for playing a game of Better Updated Go
"""

__author__ = "Seamus Bradley <github@scmb.xyz>"
__version__ = "0.1.1"

import pygame
import go
from sys import exit

from random import random


BOARD_SIZE = (920, 920)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Stone(go.Stone):
    def __init__(self, board, point, color):
        """Create, initialize and draw a stone."""
        super(Stone, self).__init__(board, point, color)
        self.coords = Stone.points_to_coords(point[0], point[1])
        self.draw()

    def draw(self):
        """Draw the stone as a circle."""
        pygame.draw.circle(screen, self.color, self.coords, 20, 0)
        pygame.display.update()

    def remove(self):
        """Remove the stone from board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pygame.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        super(Stone, self).remove()

    @staticmethod
    def coords_to_points(x_coord, y_coord):
        x = int(round(((x_coord - 5) / 40.0), 0))
        y = int(round(((y_coord - 105) / 40.0), 0))
        return x, y

    @staticmethod
    def points_to_coords(x_point, y_point):
        x = 5 + x_point * 40
        y = 105 + y_point * 40
        return x, y


class Board(go.Board):
    def __init__(self):
        """Create, initialize and draw an empty board."""
        super(Board, self).__init__()
        self.outline = pygame.Rect(45, 145, 720, 720)
        self.draw()

    def draw(self):
        """Draw the board to the background and blit it to the screen.

        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.

        This method should only be called once, when initializing the
        board.

        """
        pygame.draw.rect(background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 145 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 265 + (240 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))
        pygame.display.update()

    def update_liberties(self, added_stone=None):
        """Updates the liberties of the entire board, group by group.

        Usually a stone is added each turn. To allow killing by 'suicide',
        all the 'old' groups should be updated before the newly added one.

        """
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()

    def _play_stone(self, pos_point):
        """
        Play a stone at position.

        This version of the function does not add randomness
        """
        stone = self.search(point=pos_point)
        if stone:
            stone.remove()
        else:
            added_stone = Stone(self, pos_point, self.turn())
        board.update_liberties(added_stone)

    def _random_play_stone(self, pos_point):
        """
        Play a stone at a position, adding randomness.

        Play a stone at +/- 1 of the position on each axis
        """
        pos_point_mod = [0, 0]
        for a in [0, 1]:
            if random() < 0.5:
                pos_point_mod[a] += 1 if random() < 0.5 else -1

        self._play_stone(pos_point)


def main():
    while True:
        pygame.time.wait(150)
        pygame.draw.circle(screen, board.next, (820, 90), 20, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_p:
                    board.pass_go()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and board.outline.collidepoint(event.pos):
                    x, y = Stone.coords_to_points(event.pos[0], event.pos[1])
                    board.play_stone((x, y))
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Goban")
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.Surface(BOARD_SIZE)
    background.fill((128, 128, 128))
    board = Board()
    p_to_pass = pygame.font.SysFont("dejavu", 18)
    p_to_pass_img = p_to_pass.render("Press P to pass", True, (0, 0, 255))
    screen.blit(p_to_pass_img, (800, 150))
    pygame.display.update()
    main()
