# Kritter module for Kritter Killer
#
import pygame
from pygame.sprite import Sprite

class Kritter(Sprite):
	'''Class to represent a creeping critter.'''

	def __init__(self, kk_game, kritter_type):
		'''Initialize Kritter and set starting position.'''

		super().__init__()

		self.field = kk_game.field
		self.field_rect = kk_game.field.get_rect()
		self.settings = kk_game.settings

		self.kritter_types = [	"images/scorpion.bmp", "images/beetle.bmp",
								"images/snake.bmp", "images/crab.bmp",
								"images/fly-beetle.bmp", "images/scorpion2.bmp",
								"images/mosquito.bmp", "images/spider.bmp"
								]
		self.image = pygame.image.load(self.kritter_types[kritter_type])
		self.rect = self.image.get_rect()

		self.rect.x = (self.field_rect.right - (2 * self.rect.width))
		self.rect.y = self.rect.height
		self.y = float(self.rect.y)

	def update(self):
		'''Move the Kritter down and up.'''
		self.y += (self.settings.kritter_speed * self.settings.swarm_direction)
		self.rect.y = self.y

	def check_edges(self):
		'''Check to see if a kritter in the swarm touched an edge.'''
		if self.rect.bottom >= self.field_rect.bottom or self.rect.top <=0:
			return True
