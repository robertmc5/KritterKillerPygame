# Muzzle flash module for Alien Invasion
#
import pygame

class MuzzleFlash:
	'''Class to manage the muzzle flash when the shooter fires weapon.'''

	def __init__(self, kk_game):
		'''Initialize muzzle flash.'''
		self.field = kk_game.field
		self.field_rect = kk_game.field.get_rect()
		self.fire = False
		self.tick = 0

		# Load the muzzle flash image and rect.
		self.flash_image = pygame.image.load("images/muzzle_flash.bmp")
		self.flash_rect = self.flash_image.get_rect()

	def blit_flash(self, kk_game):
		'''Draw the muzzle flash.'''
		# Location of muzzle flash.
		self.flash_rect.midleft = (kk_game.shooter.rect.right, (
			kk_game.shooter.rect.top + 7))

		# Draw the muzzle flash surface.
		self.field.blit(self.flash_image, self.flash_rect)
