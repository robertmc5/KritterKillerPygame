# Shooter module for Kritter Killer
#
import pygame
from pygame.sprite import Sprite

class Shooter(Sprite):
	'''Class for shooter character in Kritter Killer.'''

	def __init__(self, kk_game):
		'''Initialize shooter settings.'''
		super().__init__()
		self.settings = kk_game.settings
		self.field = kk_game.field
		self.field_rect = kk_game.field.get_rect()

		# Load the shooter image and rect.
		self.image = pygame.image.load('images/shooter.bmp')
		self.rect = self.image.get_rect()

		# Start the shooter at the middle almost left side of the screen.
		self.rect.midleft = (self.field_rect.width // 8 + 10, self.field_rect.centery)

		# Shooter vertical location as a decimal float.
		self.float_y = float(self.rect.y)

		# Movement flags.
		self.moving_up = False
		self.moving_down = False

	def update_shooter(self):
		'''Update the shooter's location based on the movement flags.'''
		# Update the shooter's y {float} value, not the rect.
		if self.moving_up and self.rect.top > 10:
			self.float_y -= self.settings.shooter_speed

		if self.moving_down and self.rect.bottom < (
				self.settings.field_height - 3):
			self.float_y += self.settings.shooter_speed

		# Update rect object {with floor} of y {float} value.
		self.rect.y = self.float_y

	def blit_it(self):
		'''Draw the shooter surface.'''
		self.field.blit(self.image, self.rect)

	def center_shooter(self):
		'''Position the shooter in the center of the screen.'''
		self.rect.midleft = (self.field_rect.width // 8 + 10, self.field_rect.centery)
		self.float_y = float(self.rect.y)
