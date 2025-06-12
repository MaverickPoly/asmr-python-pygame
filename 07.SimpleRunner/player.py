import pygame
from settings import *
import os


class Player(pygame.sprite.Sprite):
	def __init__(self, jump_audio):
		super().__init__()
		self.player_jump = pygame.image.load(os.path.join("assets", "player_jump.png"))
		player_walk_1 = pygame.image.load(os.path.join("assets", "player_walk_1.png")) 
		player_walk_2 = pygame.image.load(os.path.join("assets", "player_walk_2.png")) 

		self.jump_audio = jump_audio
		self.frames = [player_walk_1, player_walk_2]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (100, HEIGHT - GRASS_HEIGHT)
		self.gravity = 0

	def animation_state(self):
		if self.rect.bottom < HEIGHT - GRASS_HEIGHT:
			self.image = self.player_jump
		else:
			self.animation_index += 0.1
			if self.animation_index >= len(self.frames):
				self.animation_index = 0
			self.image = self.frames[int(self.animation_index)]

	def apply_gravity(self):
		self.gravity += GRAVITY
		self.rect.y += self.gravity
		if self.rect.bottom >= HEIGHT - GRASS_HEIGHT:
			self.rect.bottom = HEIGHT - GRASS_HEIGHT

	def user_input(self):
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_SPACE] and self.rect.bottom == HEIGHT - GRASS_HEIGHT:
			self.gravity = -JUMP_FORCE
			self.jump_audio.play()

	def update(self):
		self.apply_gravity()
		self.user_input()
		self.animation_state()
