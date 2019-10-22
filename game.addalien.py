import pgzrun
player = Actor("player", (400, 550)) # Load in the player Actor image

def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.draw()
    drawLasers()
    drawBases()
    drawAliens()

def update():
    global player,lasers
    checkKeys()
    updateLasers()

def drawAliens():
    for a in range(len(aliens)): aliens[a].draw()

def drawBases():
    for b in range(len(bases)): bases[b].drawClipped()

def drawLasers():
    for l in range(len(lasers)): lasers[l].draw()

def checkKeys():
    global player, lasers
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            l = len(lasers)
            lasers.append(Actor("laser2", (player.x,player.y-32)))
            lasers[l].status = 0
            lasers[l].type = 1

def makeLaserActive():
    global player
    player.laserActive = 1

def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updateLasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += (2*DIFFICULTY)
            if lasers[l].y > 600: lasers[l].status = 1
        if lasers[l].type == 1:
            lasers[l].y -= 5
            if lasers[l].y < 10: lasers[l].status = 1

def updateAliens():
    global moveSequence, lasers, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30: movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 50 + (10 * DIFFICULTY)
        moveDelay -= 1
    if moveSequence >10 and moveSequence < 30: movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
        else:
            aliens[a].image = "alien1b"
            if randint(0, 5) == 0:
                lasers.append(Actor("laser1", (aliens[a].x,aliens[a].y)))
                lasers[len(lasers)-1].status = 0
                lasers[len(lasers)-1].type = 0
        if aliens[a].y > player.y and player.status == 0:
            player.status = 1
    moveSequence +=1
    if moveSequence == 40: moveSequence = 0                

def init():
    global lasers,moveSequence,moveDelay
    lasers = [] 
    player.laserActive = 1
    initBases()
    initAliens()

def initAliens():
    global aliens
    aliens = []
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80,100+(int(a/6)*64))))
        aliens[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def initBases():
    global bases
    bases = []
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            #bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1

init()
pgzrun.go()
