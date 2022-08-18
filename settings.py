# Settings for Kritter Killer
#
class Settings():
	'''Class to store Kritter Killer game settings.'''

	def __init__(self):
		'''Initialize settings.'''

		# Screen settings.
		self.bg_color = (0, 150, 0)
		self.field_width = 1200  # Will actually be fullscreen settings.
		self.field_height = 800

		# Shooter settings.
		self.extra_shooter_limit = 2

		# Ammo settings.
		self.ammo_color = (237, 214, 43)
		self.ammo_width = 15
		self.ammo_height = 3
		self.ammo_allowed = 3

		# Kritter settings.
		self.swarm_column_speed = 10

		# Rate of game speed and scoring increase.
		self.speedup_rate = 1.1
		self.scoring_rate = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		'''Initialize settings that change throughout the game.'''
		self.shooter_speed = 1.5
		self.ammo_speed = 2.0
		self.kritter_speed = 1.0
		self.kritter_points = 50
		
		# Plus 1 moves down on y axis; Minus 1 moves up on y axis.	
		self.swarm_direction = 1

	def increase_speed(self):
		'''Increase game speed.'''
		self.shooter_speed *= self.speedup_rate
		self.ammo_speed *= self.speedup_rate
		self.kritter_speed *= self.speedup_rate

		# Increase points scored.
		self.kritter_points = int(self.kritter_points * self.scoring_rate)
