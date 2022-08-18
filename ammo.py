# Ammo module for Kritter Killer
#
import pygame
from pygame.sprite import Sprite

class Ammo(Sprite):
	'''Class to manage the ammo the shooter shoots.'''

	def __init__(self, kk_game):
		'''Initialize the ammo object.'''
		super().__init__()
		self.field = kk_game.field
		self.settings = kk_game.settings
		self.color = self.settings.ammo_color

		# Create ammo rect and firing location.
		self.rect = pygame.Rect(
			0, 0, self.settings.ammo_width, self.settings.ammo_height)
		self.rect.center = (kk_game.shooter.rect.right, (
			kk_game.shooter.rect.top + 7))

		# Store the ammo's position as a decimal value.
		self.float_x = float(self.rect.x)

	def update(self):
		'''Create the movement of the ammo.'''
		self.float_x += self.settings.ammo_speed
		self.rect.x = self.float_x

	def draw_ammo(self):
		'''Draw the ammo on the screen.'''
		pygame.draw.rect(self.field, self.color, self.rect)
