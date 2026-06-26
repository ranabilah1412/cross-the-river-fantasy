import pygame
import sys
import os
import assets  

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRAY = (50, 50, 50)
RED = (200, 50, 50)


music_path = "background_music.mp3"

if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.4) 
        print("🎵 Background music started successfully!")
    except Exception as e:
        print(f"⚠️ Music file found but couldn't play: {e}")
else:
    print("ℹ️ 'background_music.mp3' not found. Put it in your project folder to hear music!")


class GameEntity:
    def __init__(self, name, start_side, image, left_x, right_x, y):
        self.name = name
        self.side = start_side       
        self.image = image  
        self.left_x = left_x    
        self.right_x = right_x  
        self.y = y              
        self.is_on_boat = False
        self.rect = self.image.get_rect()
        self.reset_to_bank()
        
    def reset_to_bank(self):
        self.rect.y = self.y
        self.is_on_boat = False
        if self.side == "right":
            self.rect.x = self.right_x
        else:
            self.rect.x = self.left_x

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Boat:
    def __init__(self, image):
        self.side = "left"
        self.image = image  
        self.rect = self.image.get_rect(topleft=(295, 310))
        self.passengers = []  

    def move(self):
        if self.side == "left":
            self.side = "right"
            self.rect.x = 450  
        else:
            self.side = "left"
            self.rect.x = 295  
            
        for entity in self.passengers:
            entity.side = self.side
            if entity.name == "Wizard":
                entity.rect.x = self.rect.x + 10
            else:
                entity.rect.x = self.rect.x + 55

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class GameManager:
    def __init__(self):
        self.state = "MENU"  
        self.score = 0       
        self.time_left = 60   
        self.game_over_reason = ""
        self.is_victory = False
        
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        
        self.font_large = pygame.font.SysFont("Arial", 40)
        self.font_medium = pygame.font.SysFont("Arial", 26)
        self.font_small = pygame.font.SysFont("Arial", 18)

    def draw_menu(self, screen):
        if assets.MENU_BG:
            screen.blit(assets.MENU_BG, (0, 0))
        else:
            screen.fill((20, 40, 60))

    def draw_hud_and_instructions(self, screen):
        pygame.draw.rect(screen, GRAY, pygame.Rect(0, 500, SCREEN_WIDTH, 100))
        pygame.draw.line(screen, GOLD, (0, 500), (SCREEN_WIDTH, 500), 3)
        
        inst1 = self.font_small.render("Controls: [SPACE] Row Boat | [0] Wizard | [1] Dragon | [2] Princess | [3] Sorcery Ball", True, WHITE)
        inst2 = self.font_small.render("Rules: Pilot is Wizard. Dragon cannot be with Princess unless Sorcery Ball protects her!", True, GOLD)
        screen.blit(inst1, (20, 520))
        screen.blit(inst2, (20, 555))

        timer_txt = self.font_medium.render(f"Time: {self.time_left}s", True, WHITE)
        score_txt = self.font_medium.render(f"Score: {self.score}", True, GOLD)
        screen.blit(timer_txt, (660, 515))
        screen.blit(score_txt, (660, 550))

    def update_timer(self):
        if self.state == "PLAYING":
            self.time_left -= 1
            if self.time_left <= 0:
                self.time_left = 0
                self.trigger_game_over(False, "OUT OF TIME!")

    def check_puzzle_rules(self, wizard, dragon, princess, crystal):
        left_bank = [e.name for e in [wizard, dragon, princess, crystal] if e.side == "left" and not e.is_on_boat]
        right_bank = [e.name for e in [wizard, dragon, princess, crystal] if e.side == "right" and not e.is_on_boat]

        for bank in [left_bank, right_bank]:
            if "Wizard" not in bank:
                if "Dragon" in bank and "Princess" in bank and "Magic Crystal" not in bank:
                    self.trigger_game_over(False, "The Dragon frightened the Princess! (No magical shield)")
                    return

        all_right_bank = [e.name for e in [wizard, dragon, princess, crystal] if e.side == "right" and not e.is_on_boat]
        if len(all_right_bank) == 4:
            self.score += self.time_left * 50
            self.trigger_game_over(True, "VICTORY! Kingdom Saved!")

    def trigger_game_over(self, won, reason):
        self.state = "GAME_OVER"
        self.is_victory = won
        self.game_over_reason = reason


# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("River Crossing Puzzle: Fantasy Kingdom")
clock = pygame.time.Clock()

if hasattr(assets, 'init'):
    assets.init() 

wizard = GameEntity("Wizard", "left", assets.WIZARD_IMG, 120, 600, 220)
dragon = GameEntity("Dragon", "left", assets.DRAGON_IMG, 120, 600, 310)
princess = GameEntity("Princess", "left", assets.PRINCESS_IMG, 40, 680, 220)
crystal = GameEntity("Magic Crystal", "left", assets.CRYSTAL_IMG, 40, 680, 310)

boat = Boat(assets.RAFT_IMG)
manager = GameManager()

def toggle_passenger(entity):
    if entity in boat.passengers:
        boat.passengers.remove(entity)
        entity.reset_to_bank()
        if entity.side == "right":
            manager.score += 1000
    else:
        if entity.side == boat.side:
            if entity.name == "Wizard":
                boat.passengers.append(entity)
                entity.is_on_boat = True
                entity.rect.x = boat.rect.x + 10
                entity.rect.y = boat.rect.y - 20
            elif len(boat.passengers) < 2:
                boat.passengers.append(entity)
                entity.is_on_boat = True
                entity.rect.x = boat.rect.x + 55
                entity.rect.y = boat.rect.y - 20


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == manager.timer_event:
            manager.update_timer()
            
        elif event.type == pygame.KEYDOWN:
            if manager.state == "MENU":
                if event.key == pygame.K_s:
                    manager.state = "PLAYING"
                elif event.key == pygame.K_e:
                    running = False
            
            elif manager.state == "GAME_OVER":
                if event.key == pygame.K_r: 
                    wizard = GameEntity("Wizard", "left", assets.WIZARD_IMG, 120, 600, 220)
                    dragon = GameEntity("Dragon", "left", assets.DRAGON_IMG, 120, 600, 310)
                    princess = GameEntity("Princess", "left", assets.PRINCESS_IMG, 40, 680, 220)
                    crystal = GameEntity("Magic Crystal", "left", assets.CRYSTAL_IMG, 40, 680, 310)
                    boat = Boat(assets.RAFT_IMG)
                    manager = GameManager()
                    manager.state = "PLAYING"

            elif manager.state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    if wizard in boat.passengers:
                        boat.move()
                        manager.check_puzzle_rules(wizard, dragon, princess, crystal)
                    else:
                        print("The boat can't move! The Wizard must get on the boat first.")

                elif event.key in (pygame.K_0, pygame.K_KP0):
                    toggle_passenger(wizard)
                    manager.check_puzzle_rules(wizard, dragon, princess, crystal)
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    toggle_passenger(dragon)
                    manager.check_puzzle_rules(wizard, dragon, princess, crystal)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    toggle_passenger(princess)
                    manager.check_puzzle_rules(wizard, dragon, princess, crystal)
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    toggle_passenger(crystal)
                    manager.check_puzzle_rules(wizard, dragon, princess, crystal)

    if manager.state == "MENU":
        manager.draw_menu(screen)
        
    elif manager.state == "PLAYING":
        if assets.GAME_BG:
            screen.blit(assets.GAME_BG, (0, 0))
        else:
            screen.fill((34, 139, 34)) 
            
        boat.draw(screen)
        wizard.draw(screen)
        dragon.draw(screen)
        princess.draw(screen)
        crystal.draw(screen)
        
        manager.draw_hud_and_instructions(screen)
        
    elif manager.state == "GAME_OVER":
        screen.fill(BLACK)
        color = GOLD if manager.is_victory else RED
        
        end_title = manager.font_large.render(manager.game_over_reason, True, color)
        score_final = manager.font_medium.render(f"Final Score: {manager.score}", True, WHITE)
        retry_txt = manager.font_medium.render("Press 'R' to Restart Game", True, GOLD)
        
        title_rect = end_title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        score_rect = score_final.get_rect(center=(SCREEN_WIDTH // 2, 300))
        retry_rect = retry_txt.get_rect(center=(SCREEN_WIDTH // 2, 380))
        
        screen.blit(end_title, title_rect)
        screen.blit(score_final, score_rect)
        screen.blit(retry_txt, retry_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()