from math import *
from neuron_constants import *
from random import randint, choice
import pygame, cell, channel
import ion as ion_class

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()

# Run
if __name__ == "__main__":
	main_cell = cell.Cell()

	circle_x = 10*main_cell.dt

	while True:
		for event in pygame.event.get():
			SCREEN.fill(WHITE)
			if event.type == pygame.KEYDOWN:
				name = main_cell.process_click(event)
				x, y = pygame.mouse.get_pos()
				if name != None:
					new_ion = ion_class.Ion(name=name, x=x, y=y)
					if new_ion.notInMembrane(delta_x=0, delta_y=0):
						main_cell.append_ion(new_ion)
				else:
					circle_x = clamp(x, SCROLL_BAR_START_X, SCROLL_BAR_START_X+SCROLL_BAR_WIDTH)
					main_cell.dt = (circle_x-SCROLL_BAR_START_X)/10
			pygame.draw.rect(SCREEN, BLUE, (0, MEMBRANE_START_Y, WIDTH, MEMBRANE_END_Y-MEMBRANE_START_Y))

			pygame.draw.rect(SCREEN, SCROLL_BAR_COLOR, (SCROLL_BAR_START_X, SCROLL_BAR_START_Y, SCROLL_BAR_WIDTH, SCROLL_BAR_HEIGHT))
			pygame.draw.ellipse(SCREEN, SCROLL_CIRCLE_COLOR, (circle_x - (SCROLL_CIRCLE_RAD/2), SCROLL_BAR_START_Y, SCROLL_CIRCLE_RAD, SCROLL_CIRCLE_RAD))

			for channel in main_cell.channels:
				pygame.draw.rect(SCREEN, channel.color, (channel.start_x - (channel.diam/2), MEMBRANE_START_Y, channel.diam, MEMBRANE_END_Y-MEMBRANE_START_Y))
			for ion in main_cell.ions:
				pygame.draw.ellipse(SCREEN, ion.color, (ion.x - (ION_WIDTH/2), ion.y - (ION_WIDTH/2), ION_WIDTH, ION_WIDTH))
				ion.change_pos(main_cell.ions, main_cell.channels, main_cell.dt)
			pygame.display.update()
			membrane_potential = main_cell.get_membrane_potential()
			#print("Membrane potential: ", membrane_potential)
