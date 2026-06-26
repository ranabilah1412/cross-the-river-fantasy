import pygame
import os

ASSETS_DIR = "assets"

MENU_BG = None
GAME_BG = None
WIZARD_IMG = None
DRAGON_IMG = None
PRINCESS_IMG = None
CRYSTAL_IMG = None
RAFT_IMG = None

def load_and_scale(filename, width, height):
    path = os.path.join(ASSETS_DIR, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (width, height))
    except Exception as e:
        print(f"Warning: Could not load {path}. Using fallback colored box.")
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((200, 50, 50, 150)) # Fallback translucent box
        return surf

def init():
    """Initializes and transforms images safely after display setup."""
    global MENU_BG, GAME_BG, WIZARD_IMG, DRAGON_IMG, PRINCESS_IMG, CRYSTAL_IMG, RAFT_IMG
    
    MENU_BG = load_and_scale("menu_bg.png", 800, 600)
    GAME_BG = load_and_scale("game_bgp.png", 800, 500) 
    
    WIZARD_IMG = load_and_scale("wizard.png", 80, 80)
    DRAGON_IMG = load_and_scale("dragon.png", 80, 80)
    PRINCESS_IMG = load_and_scale("princess.png", 80, 80)
    CRYSTAL_IMG = load_and_scale("sorcery_ball.png", 80, 80) 
    
    RAFT_IMG = load_and_scale("raft.png", 120, 80)