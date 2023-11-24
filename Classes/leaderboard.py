import pygame

from random import choice

aesthetic_colors = [
    (255, 192, 203),  # Pink
    (255, 105, 180),  # Hot Pink
    (154, 205, 50),   # Yellow Green
    (173, 216, 230),  # Light Blue
    (135, 206, 250),  # Sky Blue
    (176, 224, 230),  # Powder Blue
    (240, 128, 128),  # Light Coral
    (255, 160, 122),  # Light Salmon
    (250, 128, 114),  # Salmon
    (255, 165, 0),    # Orange
    (255, 215, 0),    # Gold
    (154, 205, 50),   # Yellow Green
    (0, 128, 0),      # Green
    (0, 255, 0),      # Lime
    (127, 255, 0),    # Chartreuse
    (0, 255, 255),    # Cyan
    (0, 191, 255),    # Deep Sky Blue
    (30, 144, 255),   # Dodger Blue
    (65, 105, 225),   # Royal Blue
    (138, 43, 226),   # Blue Violet
    (218, 112, 214),  # Orchid
    (255, 0, 255),    # Magenta
    (255, 20, 147),   # Deep Pink
    (255, 69, 0),     # Red Orange
    (128, 0, 0),      # Maroon
    (139, 0, 139),    # Dark Magenta
    (128, 0, 128),    # Purple
    (75, 0, 130),     # Indigo
    (72, 61, 139),    # Dark Slate Blue
    (65, 105, 225),   # Royal Blue
    (0, 0, 128),      # Navy
    (25, 25, 112),    # Midnight Blue
    (0, 0, 139),      # Dark Blue
    (0, 100, 0),      # Dark Green
    (0, 128, 0),      # Green
    (0, 128, 128),    # Teal
    (0, 0, 205),      # Medium Blue
    (0, 191, 255),    # Deep Sky Blue
    (65, 105, 225),   # Royal Blue
    (72, 209, 204),   # Medium Turquoise
    (70, 130, 180),   # Steel Blue
    (0, 139, 139),    # Dark Cyan
    (0, 128, 128),    # Teal
    (47, 79, 79),     # Dark Slate Gray
    (105, 105, 105),  # Dim Gray
    (169, 169, 169),  # Dark Gray
    (128, 128, 128),  # Gray
    (169, 169, 169),  # Dark Gray
    (0, 0, 0),        # Black
    (139, 69, 19),    # Saddle Brown
    (160, 82, 45),    # Sienna
    (139, 0, 0),      # Dark Red
    (128, 0, 0),      # Maroon
    (178, 34, 34),    # Fire Brick
    (205, 92, 92)     # Indian Red
]

class Row:
    def __init__(self, score, name, screen, width, height, offsetX, offsetY, y, color):
        self.width = width
        self.height = height
        self.score = score
        self.name = name
        self.screen = screen
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.y = y
        self.color = color

        self.newY = -1
        self.speed = 0
        self.moving = False

        self.separation = 5
        self.font = pygame.font.SysFont('Arial', 25)

    def move(self, newY, frames):
        self.moving = True
        self.newY = newY
        self.speed = (self.newY-self.y)//frames

    def drawRow(self):
        if self.moving:
            self.y += self.speed
            if self.speed > 0 and self.y >= self.newY:
                self.y = self.newY
                self.moving = False
            if self.speed < 0 and self.y <= self.newY:
                self.y = self.newY
                self.moving = False

        pygame.draw.rect(self.screen, self.color, pygame.Rect((self.offsetX, self.offsetY+self.y, self.width, self.height-self.separation)), border_radius=8)
        # Writing name
        self.screen.blit(self.font.render(str(self.name), True, (255,255,255)), (self.offsetX + 5, self.offsetY+self.y))
        # Writing score
        self.screen.blit(self.font.render(str(self.score), True, (255,255,255)), (self.offsetX + self.width - 100, self.offsetY+self.y))

class Leaderboard:
    def __init__(self, screen, width, height, offsetX, offsetY, numOfRows):
        self.screen = screen
        self.width = width
        self.height = height
        self.offsetX = offsetX
        self.offsetY = offsetY    
        self.numOfRows = numOfRows

        self.framesAnimation = 30
        self.visibleRows = []
        self.rows = []
        self.rowHeight = height//(numOfRows+1)
        self.lastAdded = None
    
    def __repr__(self):  
        return str(self.score)

    def addRow(self, score, name):
        # color = (randint(0,255), randint(0,255), randint(0,255))
        color = choice(aesthetic_colors)
        row = Row(score, name, self.screen, self.width, self.rowHeight, self.offsetX, self.offsetY, self.height, color)
        self.rows.append(row)
        self.lastAdded = row

    def drawLeaderBoard(self):
        for _,row in enumerate(self.visibleRows):
            row.drawRow()
        
        if self.lastAdded is not None:
            # Drawing last participant
            pygame.draw.rect(self.screen, (255,255,255), 
                             pygame.Rect((self.offsetX, self.offsetY+(self.numOfRows+1)*self.rowHeight, self.width, self.rowHeight-5)), 
                             border_radius=8)
            self.screen.blit(self.lastAdded.font.render(str("Last participant: "+self.lastAdded.name), 
                                                        False, 
                                                        (0,0,0)), 
                                                        (self.offsetX + 5, self.offsetY+(self.numOfRows+1)*self.rowHeight))
            self.screen.blit(self.lastAdded.font.render(str("Score: "+str(self.lastAdded.score)),
                                                        True, 
                                                        (0,0,0)), 
                                                        (self.offsetX + self.width - 150, self.offsetY+(self.numOfRows+1)*self.rowHeight))


    def orderRows(self):  
        sortedRows = sorted(self.rows, key = lambda x: x.score, reverse=True)
        self.visibleRows = sortedRows[:self.numOfRows]

        for i,row in enumerate(self.visibleRows):
            row.move(i*self.rowHeight, self.framesAnimation)
    
    def addParticipantsFromAPI(self, participants):
        for participant in participants:

            score = participants[participant]['player_score'] * 100

            time =  participants[participant]['player_time']
            if time < 500000:
                time += time
                time = 1000000 - time
                time = time // 10000
                score += time

            self.addRow(score, participants[participant]['player_alias'])

    def removeParticipants(self, remove):
        for participant in remove:
            filteredRows = [row for row in self.rows if row.name != participant]
            self.rows = filteredRows
