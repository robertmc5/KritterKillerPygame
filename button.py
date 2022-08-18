# Button module for Kritter Killer
#
import pygame.font

class Button:
	'''Class to represent a button onscreen.'''

	def __init__(self, kk_game, msg):
		'''Initialize button attributes.'''

		self.field = kk_game.field
		self.field_rect = self.field.get_rect()

		self.width, self.height = (200, 50)
		self.button_color = (135, 0, 255)
		self.text_color = (250, 250, 250)
		self.font = pygame.font.SysFont("arial", 40, bold=True)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.field_rect.center

		self._prep_msg(msg)

	def _prep_msg(self, msg):
		'''Turn msg into a rendered image and center text on button.'''

		self.msg_image = self.font.render(msg, True, self.text_color,
			 self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		'''Draw button and then draw message on it.'''

		self.field.fill(self.button_color, self.rect)
		self.field.blit(self.msg_image, self.msg_image_rect)
