# Scoreboard module for Kritter Killer
#
import pygame.font
from pygame.sprite import Group
from shooter import Shooter

class Scoreboard:
	'''A class to report scoring and game information.'''

	def __init__(self, kk_game):
		'''Initialize scoreboard attributes.'''
		self.kk_game = kk_game  # For spare shooters.

		self.field = kk_game.field
		self.field_rect = self.field.get_rect()
		self.settings = kk_game.settings
		self.stats = kk_game.stats

		# Font settings for scoring info.
		# Scoreboard font is 35 pixels high; the arrows are 36 pixels.
		self.text_color = (240, 240, 240)
		self.instruction_color = self.settings.ammo_color
		self.font = pygame.font.SysFont("arial", 30, bold=True)

		# Scoreboard background.
		self.scoreboard_rect = pygame.Rect(0, 0, self.field_rect.width // 8, 
			self.field_rect.height)
		self.scoreboard_rect.topleft = self.field_rect.topleft
		self.sb_color = (135, 0, 255)
		self.scoreboard_impact = False

		# Image preparation of onscreen text.
		self._prep_images()

	def _prep_images(self):
		'''Initial renderings of onscreen text into pygame images.'''
		# Prepare static labels.
		self.prep_score_label()
		self.prep_high_score_label()
		self.prep_level_label()

		# Prepare initial score, high score, level and spare shooter images.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_spare_shooters()

		self.prep_instruction_legend()  # When not playing.
		self.prep_game_over()  # After game is complete.		

	def prep_instruction_legend(self):
		'''Render game instructions into image.'''
		play_legend_str = "P - Play"
		self.play_legend = self.font.render(play_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.play_legend_rect = self.play_legend.get_rect()
		self.play_legend_rect.centerx = self.field_rect.width // 16
		self.play_legend_rect.centery = (self.field_rect.height // 4) - 35 - 7

		quit_legend_str = "Esc - Quit"
		self.quit_legend = self.font.render(quit_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.quit_legend_rect = self.quit_legend.get_rect()
		self.quit_legend_rect.centerx = self.field_rect.width // 16
		self.quit_legend_rect.centery = self.field_rect.height // 4

		pause_legend_str = "F - Freeze"
		self.pause_legend = self.font.render(pause_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.pause_legend_rect = self.pause_legend.get_rect()
		self.pause_legend_rect.centerx = self.field_rect.width // 16
		self.pause_legend_rect.centery = (self.field_rect.height // 4) + 35 + 7

		up_legend_str = "↑ - Up"
		self.up_legend = self.font.render(up_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.up_legend_rect = self.up_legend.get_rect()
		self.up_legend_rect.centerx = self.field_rect.width // 16
		self.up_legend_rect.centery = (
			self.field_rect.height // (1.4)) - 36 - 7

		down_legend_str = "↓ - Down"
		self.down_legend = self.font.render(down_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.down_legend_rect = self.down_legend.get_rect()
		self.down_legend_rect.centerx = self.field_rect.width // 16
		self.down_legend_rect.centery = self.field_rect.height // (1.4)

		fire_legend_str = "Space - Fire"
		self.fire_legend = self.font.render(fire_legend_str, True, 
			self.instruction_color, self.sb_color)
		self.fire_legend_rect = self.fire_legend.get_rect()
		self.fire_legend_rect.centerx = self.field_rect.width // 16
		self.fire_legend_rect.centery = (
			self.field_rect.height // (1.4)) + 36 + 7

	def prep_score_label(self):
		'''Render static score label into image.'''
		score_label_str = "Score"
		self.score_label = self.font.render(score_label_str, True, 
			self.text_color, self.sb_color)
		self.score_label_rect = self.score_label.get_rect()
		self.score_label_rect.centerx = self.field_rect.width // 16
		self.score_label_rect.bottom = self.field_rect.centery - 17 - 35 - 7		

	def prep_high_score_label(self):
		'''Render static high score label into image.'''
		high_score_label_str = "High Score"
		self.high_score_label = self.font.render(high_score_label_str, True, 
			self.text_color, self.sb_color)
		self.high_score_label_rect = self.high_score_label.get_rect()
		self.high_score_label_rect.centerx = self.field_rect.width // 16
		self.high_score_label_rect.top = 15

	def prep_level_label(self):
		'''Render static level label into image.'''
		level_label_str = "Level"
		self.level_label = self.font.render(level_label_str, True, 
			self.text_color, self.sb_color)
		self.level_label_rect = self.level_label.get_rect()
		self.level_label_rect.centerx = self.field_rect.width // 16
		self.level_label_rect.top = self.field_rect.centery + 17

	def prep_score(self):
		'''Render current score into image.'''
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, 
			self.sb_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.centerx = self.field_rect.width // 16
		self.score_rect.bottom = self.field_rect.centery - 17

	def prep_high_score(self):
		'''Render high score into image.'''
		rounded_high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(rounded_high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
			self.text_color, self.sb_color)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.field_rect.width // 16
		self.high_score_rect.top = 15 + 35 + 7

	def check_high_score(self):
		'''Check if current score is new high score.'''
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		'''Render current level into image.'''
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color, 
			self.sb_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.centerx = self.field_rect.width // 16
		self.level_rect.top = self.field_rect.centery + 17 + 35 + 7

	def prep_spare_shooters(self):
		'''Prepare spare shooter surfaces sprite group for drawing.'''
		self.spare_shooters = Group()
		for shooter_number in range(self.stats.shooters_left):
			shooter = Shooter(self.kk_game)
			shooter.rect.centerx = self.field_rect.width // 16
			shooter.rect.bottom = (self.field_rect.bottom - 15) - (
				shooter_number * (shooter.rect.height + 10))
			self.spare_shooters.add(shooter)

	def prep_game_over(self):
		'''Render 'game over' message into image.'''
		game_over_str = "Game Over"
		self.game_over = self.font.render(game_over_str, True, 
			self.text_color, self.sb_color)
		self.game_over_rect = self.game_over.get_rect()
		self.game_over_rect.centerx = self.field_rect.width // 16
		self.game_over_rect.bottom = self.field_rect.bottom - 15 - 35

	def display_scoreboard(self):
		'''Draw the scoreboard on the screen.'''
		pygame.draw.rect(self.field, self.sb_color, self.scoreboard_rect)
		if not self.stats.game_active:
			# Game instruction legend.
			self.field.blit(self.play_legend, self.play_legend_rect)
			self.field.blit(self.quit_legend, self.quit_legend_rect)
			self.field.blit(self.pause_legend, self.pause_legend_rect)
			self.field.blit(self.up_legend, self.up_legend_rect)
			self.field.blit(self.down_legend, self.down_legend_rect)
			self.field.blit(self.fire_legend, self.fire_legend_rect)
		# Static labels.
		self.field.blit(self.score_label, self.score_label_rect)
		self.field.blit(self.high_score_label, self.high_score_label_rect)
		self.field.blit(self.level_label, self.level_label_rect)

		# Draw the dynamic score, high score, level and spare shooters.
		self.field.blit(self.score_image, self.score_rect)
		self.field.blit(self.high_score_image, self.high_score_rect)
		self.field.blit(self.level_image, self.level_rect)
		self.spare_shooters.draw(self.field)

		if self.stats.game_over:
			self.field.blit(self.game_over, self.game_over_rect)
			