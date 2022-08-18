# Message module for Kritter Killer
#
import pygame.font

class Message:
	'''Class to write a message onscreen.'''

	def __init__(self, kk_game, width, height, font_size, msg):
		'''Initialize message attributes.'''

		self.field = kk_game.field
		self.field_rect = self.field.get_rect()

		self.width, self.height = (width, height)
		self.text_color = (250, 250, 250)
		self.backing_color = (135, 0, 255)
		self.border_color = (237, 214, 43)
		self.font = pygame.font.SysFont("arial", font_size, bold=True)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = self.field_rect.centerx
		self.rect.centery = self.field_rect.height // 4

		self._prep_message(msg)

	def _prep_message(self, msg):
		'''Render message into image.'''

		self.message_image = self.font.render(msg, True, self.text_color, 
			self.backing_color)
		self.message_rect = self.message_image.get_rect()
		self.message_rect.center = self.rect.center

	def write_message(self):
		'''Write the message with border to screen.'''

		self.field.fill(self.border_color, self.rect)
		self.field.blit(self.message_image, self.message_rect)
