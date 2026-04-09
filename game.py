import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()
pg.mixer.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250

        self.bird = Bird(self.scale_factor)

        # 🔊 SOUND
        self.flap_sound = pg.mixer.Sound("assets/sfx/flap.wav")
        self.score_sound = pg.mixer.Sound("assets/sfx/score.wav")
        self.dead_sound = pg.mixer.Sound("assets/sfx/dead.wav")
        self.click_sound = pg.mixer.Sound("assets/sfx/flap.wav")

        # LOGIN
        self.login_active = True
        self.username = ""
        self.password = ""
        self.correct_username = "Neeraj"
        self.correct_password = "95089"
        self.font = pg.font.Font(None, 40)
        self.login_error = ""

        self.username_box = pg.Rect(150, 250, 300, 50)
        self.password_box = pg.Rect(150, 330, 300, 50)
        self.active_box = "username"

        # LOGIN IMAGE
        self.login_bg = pg.image.load("assets/login.png").convert()
        self.login_bg = pg.transform.scale(self.login_bg, (self.width, self.height))

        # CURSOR
        self.cursor_visible = True
        self.cursor_timer = 0

        # GAME STATES
        self.game_started = False
        self.game_over = False

        # SCORE
        self.score = 0
        self.high_score = 0
        self.loadHighScore()

        self.button_hover = False

        self.start_btn = pg.Rect(200,300,200,60)
        self.restart_btn = pg.Rect(200,300,200,60)

        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71

        self.setUpBgAndGround()
        self.gameLoop()

    def loadHighScore(self):
        try:
            with open("highscore.txt","r") as f:
                self.high_score=int(f.read())
        except:
            self.high_score=0

    def saveHighScore(self):
        with open("highscore.txt","w") as f:
            f.write(str(self.high_score))

    def resetGame(self):
        self.bird = Bird(self.scale_factor)
        self.pipes = []
        self.score = 0
        self.game_over = False

        self.game_started = True
        self.is_enter_pressed = True
        self.bird.update_on = True
        self.pipe_generate_counter = 0

    def gameLoop(self):
        last_time=time.time()

        while True:
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if event.key == pg.K_RETURN and not self.game_started and not self.game_over and not self.login_active:
                        self.game_started=True
                        self.is_enter_pressed=True
                        self.bird.update_on=True
                        self.click_sound.play()

                    if event.key == pg.K_RETURN and self.game_over:
                        self.resetGame()

                    if event.key == pg.K_SPACE and self.is_enter_pressed and not self.game_over:
                        self.bird.flap(dt)
                        self.flap_sound.play()

                    if self.game_over and event.key == pg.K_h:
                        self.high_score=0
                        self.saveHighScore()

                if self.login_active:

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.username_box.collidepoint(event.pos):
                            self.active_box="username"
                        elif self.password_box.collidepoint(event.pos):
                            self.active_box="password"

                    if event.type == pg.KEYDOWN:

                        if event.key == pg.K_BACKSPACE:
                            if self.active_box=="username":
                                self.username=self.username[:-1]
                            else:
                                self.password=self.password[:-1]

                        elif event.key == pg.K_RETURN:
                            if self.username==self.correct_username and self.password==self.correct_password:
                                self.login_active=False
                            else:
                                self.login_error="Wrong ID or Password"

                        else:
                            if self.active_box=="username":
                                self.username+=event.unicode
                            else:
                                self.password+=event.unicode

                else:
                    if event.type == pg.MOUSEBUTTONDOWN:

                        if not self.game_started and not self.game_over:
                            if self.start_btn.collidepoint(event.pos):
                                self.game_started=True
                                self.is_enter_pressed=True
                                self.bird.update_on=True
                                self.click_sound.play()

                        if self.game_over:
                            if self.restart_btn.collidepoint(event.pos):
                                self.resetGame()

            # CURSOR BLINK
            self.cursor_timer+=dt
            if self.cursor_timer>0.5:
                self.cursor_visible=not self.cursor_visible
                self.cursor_timer=0

            if not self.login_active:
                mouse_pos=pg.mouse.get_pos()

                if not self.game_started:
                    self.button_hover=self.start_btn.collidepoint(mouse_pos)
                elif self.game_over:
                    self.button_hover=self.restart_btn.collidepoint(mouse_pos)

            if not self.login_active and self.game_started and not self.game_over:
                self.updateEverything(dt)
                self.checkCollisions()

            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom>568:
                if not self.game_over:
                    self.dead_sound.play()
                self.game_over=True

            for pipe in self.pipes:
                if (self.bird.rect.colliderect(pipe.rect_down) or
                    self.bird.rect.colliderect(pipe.rect_up)):
                    if not self.game_over:
                        self.dead_sound.play()
                    self.game_over=True

        if self.game_over:
            if self.score>self.high_score:
                self.high_score=self.score
                self.saveHighScore()

    def updateEverything(self,dt):
        if self.is_enter_pressed:
            self.ground1_rect.x-=int(self.move_speed*dt)
            self.ground2_rect.x-=int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x=self.ground1_rect.right

            if self.pipe_generate_counter>70:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))
                self.pipe_generate_counter=0

            self.pipe_generate_counter+=1

            for pipe in self.pipes:
                pipe.update(dt)

                if not hasattr(pipe,"passed"):
                    pipe.passed=False

                if not pipe.passed and pipe.rect_up.right<self.bird.rect.left:
                    self.score+=1
                    self.score_sound.play()
                    pipe.passed=True

            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)

        self.bird.update(dt)

    def drawEverything(self):

        if self.login_active:
            self.win.blit(self.login_bg,(0,0))

            active=(0,120,255)
            inactive=(200,200,200)

            pg.draw.rect(self.win,active if self.active_box=="username" else inactive,self.username_box,2)
            pg.draw.rect(self.win,active if self.active_box=="password" else inactive,self.password_box,2)

            user_text=self.font.render(self.username,True,(0,0,0))
            pass_text=self.font.render("*"*len(self.password),True,(0,0,0))

            self.win.blit(user_text,(self.username_box.x+10,self.username_box.y+10))
            self.win.blit(pass_text,(self.password_box.x+10,self.password_box.y+10))

            self.win.blit(self.font.render("Username",True,(0,0,0)),(150,220))
            self.win.blit(self.font.render("Password",True,(0,0,0)),(150,300))

            if self.cursor_visible:
                if self.active_box=="username":
                    x=self.username_box.x+10+user_text.get_width()
                    y=self.username_box.y+10
                else:
                    x=self.password_box.x+10+pass_text.get_width()
                    y=self.password_box.y+10

                pg.draw.line(self.win,(0,0,0),(x,y),(x,y+30),2)

            self.win.blit(self.font.render(self.login_error,True,(255,0,0)),(150,400))
            return

        if not self.game_started:
            self.win.blit(self.bg_img,(0,-300))

            overlay=pg.Surface((self.width,self.height))
            overlay.set_alpha(120)
            overlay.fill((0,0,0))
            self.win.blit(overlay,(0,0))

            color=(0,255,0) if self.button_hover else (0,180,0)
            pg.draw.rect(self.win,color,self.start_btn,border_radius=10)

            self.win.blit(self.font.render("START GAME",True,(255,255,255)),(220,315))
            self.win.blit(self.font.render("Press ENTER or CLICK",True,(255,255,255)),(140,380))
            return

        self.win.blit(self.bg_img,(0,-300))

        for pipe in self.pipes:
            pipe.drawPipe(self.win)

        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)

        self.win.blit(self.font.render("Score: "+str(self.score),True,(255,255,255)),(20,20))
        self.win.blit(self.font.render("High: "+str(self.high_score),True,(255,255,0)),(20,60))

        if self.game_over:
            overlay=pg.Surface((self.width,self.height))
            overlay.set_alpha(150)
            overlay.fill((0,0,0))
            self.win.blit(overlay,(0,0))

            self.win.blit(self.font.render("GAME OVER",True,(255,0,0)),(200,200))

            color=(0,0,255) if self.button_hover else (0,0,200)
            pg.draw.rect(self.win,color,self.restart_btn)

            self.win.blit(self.font.render("RESTART",True,(255,255,255)),(240,315))
            self.win.blit(self.font.render("Press ENTER to Restart",True,(255,255,255)),(120,360))
            self.win.blit(self.font.render("H = Reset Score | ESC = Exit",True,(255,255,255)),(100,420))

    def setUpBgAndGround(self):
        self.bg_img=pg.transform.scale_by(pg.image.load("assets/bg.png").convert(),self.scale_factor)
        self.ground1_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)

        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground2_img.get_rect()

        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=568
        self.ground2_rect.y=568

game = Game()