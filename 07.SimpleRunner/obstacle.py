import os
import random
import pygame
from settings import *


class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()

		if type == "snail":
			snail1 = pygame.image.load(os.path.join("assets", "snail1.png"))
			snail2 = pygame.image.load(os.path.join("assets", "snail2.png"))
			self.frame = [snail1, snail2]
			y_bottom = HEIGHT - GRASS_HEIGHT
		else:
			fly1 = pygame.image.load(os.path.join("assets", "fly1.png"))
			fly2 = pygame.image.load(os.path.join("assets", "fly2.png"))
			self.frame = [fly1, fly2]
			y_bottom = 300

		self.selected_index = 0
		self.image = self.frame[self.selected_index]
		self.rect = self.image.get_rect()
		self.rect.midbottom = (random.randint(WIDTH + 200, WIDTH + 500), y_bottom)

	def animation_state(self):
		self.selected_index += 0.1
		if self.selected_index >= len(self.frame):
			self.selected_index = 0
		self.image = self.frame[int(self.selected_index)]

	def move(self):
		self.rect.x -= OBSTACLE_SPEED

	def update(self):
		self.move()
		self.animation_state()
		self.destroy()

	def destroy(self):
		if self.rect.x < -100:
			self.kill()

