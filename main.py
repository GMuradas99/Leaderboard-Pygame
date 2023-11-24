import pygame
import random

from time import sleep, time

from Classes.leaderboard import Leaderboard, Row
from Classes.apiInteraction import ScienceDayAPI

UPDATE_DELAY = 3               # In seconds
FPS = 30                       # Frames per second
NUMBER_OF_ROWS = 20            # Number of rows in leaderboard

# Initializing 
pygame.init()
# screen = pygame.display.set_mode((800,600))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

removed = []

offsetW = 30
offsetH = 30

lead = Leaderboard(screen, screenWidth - offsetW*2, screenHeight - offsetH*2, offsetW, offsetH, NUMBER_OF_ROWS)
sda = ScienceDayAPI('https://psytests.be/tests/day_of_science/api/')

lead.addParticipantsFromAPI(sda.participants)
lead.orderRows()

# Main loop
run = True
startTime = time()
while run:
    #Clearing previous frame
    screen.fill((43,5,92))

    # Drawing
    lead.drawLeaderBoard()

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Key is pressed
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_u:
                lead.orderRows()
            if event.key == pygame.K_a:
                randScore = random.randint(0,100)
                print('Adding',randScore)
                lead.addRow(randScore, 'temp')
                lead.orderRows()
            if event.key == pygame.K_q:
                run = False
    
    # Time check for API updates
    elapsedTime = time() - startTime
    if elapsedTime >= UPDATE_DELAY:
        startTime = time()
        new = sda.getNewParticipants()
        sda.updateParticipants()

        # Removing important
        for key in new:
            if new[key]['player_alias'][:4] == 'rem-':
                removed.append(new[key]['player_alias'][4:])
                new[key]['player_alias'] = 'None'
                removed.append(new[key]['player_alias'])
        lead.removeParticipants(removed)

        print("Updating:", new)

        lead.addParticipantsFromAPI(new)
        lead.orderRows()


    # Updating
    pygame.display.update()

    sleep(1/FPS)

pygame.quit()