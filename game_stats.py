# Game Stats module for Kritter Killer
#
import json

class GameStats:
	'''Track statistics for Kritter Killer.'''

	def __init__(self, kk_game):
		'''Initialize statistics.'''
		self.settings = kk_game.settings
		self.game_active = False
		self.game_freeze = False
		self.reset_stats()
		self._get_high_score()

	def reset_stats(self):
		'''Initialize statistics that can change during the game.'''
		self.shooters_left = self.settings.extra_shooter_limit
		self.score = 0
		self.level = 1
		self.game_over = False  # For printing the words "Game Over" or not.
	
	def _get_high_score(self):
		'''Load persistent high score from json file.'''
		try:
			with open('high_score.json') as f:
				self.high_score = int(json.load(f))
		except FileNotFoundError:
			with open('high_score.json', "w") as f:
				json.dump(str(0), f)
			self.high_score = 0
