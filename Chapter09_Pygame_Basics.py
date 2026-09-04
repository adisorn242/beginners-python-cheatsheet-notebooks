"""Chapter 09: Pygame Basics -- run this locally (not in Colab) to see a real window."""
import sys
import pygame as pg

pg.init()

# Set up the screen and background color.
screen = pg.display.set_mode((1200, 800))
pg.display.set_caption("Alien Invasion")
bg_color = (230, 230, 230)

# A rect we'll draw and move around.
bullet_rect = pg.Rect(100, 100, 3, 15)
color = (100, 100, 100)


class Bullet(pg.sprite.Sprite):
    """A simple bullet."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((3, 15))
        self.image.fill((60, 60, 60))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 1


bullets = pg.sprite.Group()
clock = pg.time.Clock()

# Main game loop.
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bullets.add(Bullet(*pg.mouse.get_pos()))
            elif event.key == pg.K_q:
                pg.quit()
                sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            bullets.add(Bullet(*pg.mouse.get_pos()))

    bullets.update()

    screen.fill(bg_color)
    pg.draw.rect(screen, color, bullet_rect)
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        else:
            screen.blit(bullet.image, bullet.rect)

    pg.display.flip()
    clock.tick(60)
