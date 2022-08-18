# Kritter Killer (2D shooting game)
# by Robert McCarter
#
# The player moves up and down the left side of the screen.  Kritters
# approach from the right side of the screen.  The player shoots the
# Kritters as they approach.  If they touch the left side of the screen
# or the player, the player is injured and the screen resets.  The 
# third injury results in death and the game is over. Every time the 
# swarm of critters is destroyed, the next swarm is faster.
#
import sys
from time import sleep
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from message import Message
from shooter import Shooter
from ammo import Ammo
from muzzle_flash import MuzzleFlash
from kritter import Kritter

class KritterKiller:
	'''Class to manage the game behavior.'''

	def __init__(self):
		'''Initialize game attributes.'''
		pygame.init()
		pygame.mixer.set_reserved(0)
		# pygame.mixer.set_reserved(1)
		self.channel1 = pygame.mixer.Channel(0)
		# self.channel2 = pygame.mixer.Channel(0)
		self.settings = Settings()

		# Set screen size.
		self.field = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.field_width = self.field.get_rect().width
		self.settings.field_height = self.field.get_rect().height
		self.field_rect = self.field.get_rect()

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.shooter = Shooter(self)
		self.ammunition = pygame.sprite.Group()
		self.flash = MuzzleFlash(self)
		self.kritters = pygame.sprite.Group()

		self._load_sounds()

		self.play_button = Button(self, "Play")
		self.freeze_button = Button(self, "PAUSE")
		self.new_high_score_message = Message(
			self, 575, 100, 50, " You got a new high score! ")
		self.high_score_sound_unplayed = True

		self._create_swarm()

	def _load_sounds(self):
		'''Establish sound effects.'''
		self.gunshot_sound = pygame.mixer.Sound("sounds/gunshot.wav")
		self.gunshot_sound.set_volume(0.25)
		self.squish_sound = pygame.mixer.Sound("sounds/squish.wav")
		self.lose_round_sound = pygame.mixer.Sound("sounds/lose_round.wav")
		self.lose_round_sound.set_volume(0.25)
		self.win_round_sound = pygame.mixer.Sound("sounds/win_round.wav")
		self.crush_shooter_sound = pygame.mixer.Sound("sounds/crush_shooter.wav")
		self.crush_shooter_sound.set_volume(0.25)
		self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
		self.high_score_sound = pygame.mixer.Sound("sounds/high_score.wav")

		self.music = pygame.mixer.music.load("sounds/background_music.wav")
		pygame.mixer.music.set_volume(0.5)

	def run_game(self):
		'''The main game loop.'''
		while True:
			self._check_events()

			if self.stats.game_active and not self.stats.game_freeze:
				self.shooter.update_shooter()
				self._update_ammo()
				self._update_kritters()
    
			self._update_screen()

	def _check_events(self):
		'''Respond to user events.'''
		for event in pygame.event.get():

			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			if event.type == pygame.KEYUP:
				self._check_keyup_events(event)

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_position = pygame.mouse.get_pos()
				self._check_play_button(mouse_position)

	def _check_play_button(self, mouse_position):
		'''Check if mouse is over Play button to start a game.'''
		if self.play_button.rect.collidepoint(mouse_position) and (
			not self.stats.game_active):
			self._start_game()

	def _start_game(self):
		'''Reset the screen and stats and start a new game.'''
		# Reset game stats.
		self.stats.game_active = True
		self.stats.reset_stats()
		self.settings.initialize_dynamic_settings()
		self.high_score_sound_unplayed = True

		# Prepare starting score, level and spare shooter images.
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_spare_shooters()

		# Clear out remaining sprite groups.
		self.kritters.empty()
		self.ammunition.empty()

		# Create a new swarm and center the shooter.
		self.shooter.center_shooter()	
		pygame.mixer.music.play(-1)		
		self._create_swarm()

		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)	

	def _check_keydown_events(self, event):
		'''Respond to key presses.'''
		if event.key == pygame.K_UP:
			self.shooter.moving_up = True

		if event.key == pygame.K_DOWN:
			self.shooter.moving_down = True

		if event.key == pygame.K_ESCAPE:
			# Save high score to json file.
			with open('high_score.json', "w") as f:
				json.dump(str(self.stats.high_score), f)

			sys.exit()

		if event.key == pygame.K_p and self.stats.game_active == False:
			self._start_game()

		if event.key == pygame.K_f and self.stats.game_active == True:
			self.stats.game_freeze = not self.stats.game_freeze
			if self.stats.game_freeze:
				pygame.mixer.music.pause()
			else:
				pygame.mixer.music.unpause()

		if event.key == pygame.K_SPACE:
			self._fire_ammo()

	def _check_keyup_events(self, event):
		'''Respond to key releases.'''
		if event.key == pygame.K_UP:
			self.shooter.moving_up = False

		if event.key == pygame.K_DOWN:
			self.shooter.moving_down = False

	def _fire_ammo(self):
		'''Fire the ammo and add to sprite group.'''
		if len(self.ammunition) < self.settings.ammo_allowed:
			self.gunshot_sound.play()
			new_ammo = Ammo(self)
			self.ammunition.add(new_ammo)
			self.flash.fire = True

	def _update_ammo(self):
		'''Update position of ammo and get rid of old ammo.'''
		self.ammunition.update()

		for ammo in self.ammunition.copy():
			if ammo.rect.left >= self.field_rect.right:
				self.ammunition.remove(ammo)

		self._check_ammo_kritter_collisions()

	def _check_ammo_kritter_collisions(self):
		'''Respond to ammo and kritter collisions.'''
		# Check for ammo that has hit a kritter.
		# If so, remove the ammo and the kritter.
		collisions = pygame.sprite.groupcollide(
			self.ammunition, self.kritters, True, True)

		if collisions:
			self.squish_sound.play()
			for kritters in collisions.values():
				self.stats.score += len(kritters) * self.settings.kritter_points
			self.sb.prep_score()
			self.sb.check_high_score()

		# When the entire swarm is eliminated.
		if not self.kritters:
			self.channel1.play(self.win_round_sound)
			self._start_new_level()

	def _start_new_level(self):
		'''Empty ammo, increase speed and level and create new swarm.'''
		self.ammunition.empty()
		self.settings.increase_speed()
		self.stats.level += 1
		self.sb.prep_level()
		self._create_swarm()

	def _update_kritters(self):
		'''Move the kritters in the swarm.'''
		self._check_swarm_edges()
		self.kritters.update()

		# Check if a kritter hit the shooter.
		if pygame.sprite.spritecollideany(self.shooter, self.kritters):
			self.channel1.play(self.crush_shooter_sound)
			self._shooter_hit()

		# Check if a kritter reached the left side of the field of play.
		for kritter in self.kritters.sprites():
			if kritter.rect.left <= self.field_rect.width // 8:
				# Treat the same as kritter hitting the shooter.
				self._shooter_hit()
				break

	def _shooter_hit(self):
		'''Respond to kritter hitting shooter; or reaching screen end.'''
		# Show an impact.
		self.channel1.queue(self.lose_round_sound)
		self.sb.scoreboard_impact = True
		self._scoreboard_impact_flash()
 
		# Pause, to realize loss of shooter.
		sleep(1.5)
		self.sb.scoreboard_impact = False
		self._scoreboard_impact_flash()

		if self.stats.shooters_left > 0:
			# Decrement number of shooters left.
			self.stats.shooters_left -= 1
			self.sb.prep_spare_shooters()

			# Remove remaining kritters and ammo.
			self.kritters.empty()
			self.ammunition.empty()

			# Center the shooter and recreate swarm.
			self.shooter.center_shooter()
			self.shooter.blit_it()
			self._create_swarm()
		else:
			# End game.
			pygame.mixer.music.stop()
			sleep(0.5)
			self.game_over_sound.play()
			self.stats.game_active = False
			self.stats.game_over = True
			pygame.mouse.set_visible(True)

	def _scoreboard_impact_flash(self):
		'''Flash a color change on the scoreboard due to kritter impact.'''
		if self.sb.scoreboard_impact:
			self.sb.sb_color = (255, 0, 0)
		else:
			self.sb.sb_color = (135, 0, 255)

		self.sb.prep_score_label()
		self.sb.prep_high_score_label()
		self.sb.prep_level_label()

		self.sb.prep_score()
		self.sb.prep_high_score()
		self.sb.prep_level()

		self._update_screen()

	def _check_swarm_edges(self):
		'''Respond if a kritter in the swarm touches an edge.'''
		for kritter in self.kritters.sprites():
			if kritter.check_edges():
				self._change_swarm_direction()
				break

	def _change_swarm_direction(self):
		'''
		Move the kritters in the swarm columns to the left 
		and change the direction they move.
		'''
		for kritter in self.kritters.sprites():
			kritter.rect.x -= self.settings.swarm_column_speed
		self.settings.swarm_direction *= -1

	def _create_swarm(self):
		'''Create a swarm of kritters.'''
		# Find the number of kritters in a column.
		# Spacing between each kritter is equal to one kritter height.
		kritter = Kritter(self, 0)
		available_space_y = self.settings.field_height - (
			2 * kritter.rect.height)
		number_kritters_y = available_space_y // (2 * kritter.rect.height)

		# Find the number of columns in the field.
		# Spacing between each column is equal to one kritter width.
		shooter_width = self.shooter.rect.width
		available_space_x = self.settings.field_width - (
			3 * kritter.rect.width + shooter_width)
		number_columns_x = available_space_x // (2 * kritter.rect.width)
		if number_columns_x > 8: number_columns_x = 8

		# Create the swarm of kritters.
		for kritter_column in range(number_columns_x):
			for kritter_number in range(number_kritters_y):
				self._create_kritter(kritter_number, kritter_column)

		# Pause.
		self._update_screen()
		sleep(1.0)

	def _create_kritter(self, kritter_number, kritter_column):
		'''Create each kritter and position it properly.'''
		kritter = Kritter(self, kritter_column)
		kritter.y = kritter.rect.height + (
			kritter_number * 2 * kritter.rect.height)
		kritter.rect.y = kritter.y  # All kritters have same height of 60.
		kritter.rect.x = (self.field_rect.right - 88 - 46) - (
			kritter_column * (88 + 46))  # Biggest and smallest kritter widths.
		self.kritters.add(kritter)		

	def _update_screen(self):
		'''Update images on the screen.'''
		self.field.fill(self.settings.bg_color)
		self.shooter.blit_it()
		for ammo in self.ammunition.sprites():
			ammo.draw_ammo()
		self.kritters.draw(self.field)

		# Muzzle flashes.
		if self.flash.fire:
			self.flash.blit_flash(self)
		self.flash.tick += 1
		if self.flash.tick == 50:  # Image remains long enough to be visible.
			self.flash.fire = False
			self.flash.tick = 0

		self.sb.display_scoreboard()

		# Check if game is either paused or over; to show button.
		if self.stats.game_freeze:
			self.freeze_button.draw_button()

		if not self.stats.game_active:
			self.play_button.draw_button()
			# If player acheived new high score, show a message.
			if self.stats.score == self.stats.high_score and (
				self.stats.high_score != 0):
				if self.high_score_sound_unplayed:
					self.high_score_sound.play()
					self.high_score_sound_unplayed = False
				self.new_high_score_message.write_message()

		pygame.display.flip()
  
if __name__ == '__main__':
	# Create game instance and start the game.
	kk = KritterKiller()
	kk.run_game() 
