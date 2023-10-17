import pygame
import random
import math

from mover import mover

class dol:
    def __init__(self, diff, exp, life):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.exp = exp

        # screen define
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dash of Legends")

        # color define
        self.BLACK  = (  0,   0,   0)
        self.WHITE  = (255, 255, 255)
        self.RED    = (255,   0,   0)
        self.GREEN  = (  0, 255,   0)
        self.BLUE   = (  0,   0, 255)
        self.YELLOW = (255, 255,   0)

        # player define
        nx = self.screen_width // 2 - 5
        ny = self.screen_height * 3 // 4
        self.player = mover(10, 0.2, life, nx, ny)

        self.dashing = False
        self.dash_duration = 10
        self.dash_timer = 0
        self.dash_speed = 1

        # enemy define
        self.enemies = []
        for _ in range(diff):
            dx = random.randint(-1000, 1000)
            dy = random.randint(-1000, 1000)
            nx = (0 if dx < 0 else self.screen_width) + dx
            ny = (0 if dy < 0 else self.screen_height) + dy
            self.enemies.append(mover(10, 0.1, diff // 10 + 1, nx, ny))

        # boss define
        self.bosses = []
        for _ in range(diff // 10):
            dx = random.randint(-1000, 1000)
            dy = random.randint(-1000, 1000)
            nx = (0 if dx < 0 else self.screen_width) + dx
            ny = (0 if dy < 0 else self.screen_height) + dy
            self.bosses.append(mover(30, 0.05, diff, nx, ny))

        self.q_skills = []

    def dungeon(self):
        while True:
            fps = self.clock.tick(60)

            if not self.enemies and not self.bosses:
                pygame.quit()
                return True, self.player.life

            # event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False, 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        for i in range(int(math.log(self.exp, 10))):
                            self.q_skills.append(mover(10, 0.5, 0, self.player.rect.x - 20 * (i + 2), self.player.rect.y + 10 * (i + 1)))
                            self.q_skills.append(mover(10, 0.5, 0, self.player.rect.x + 20 * (i + 2), self.player.rect.y + 10 * (i + 1)))
                        self.q_skills.append(mover(10, 0.5, 0, self.player.rect.x - 5, self.player.rect.y - 5))
                    if event.key == pygame.K_r and not self.dashing:
                        self.dashing = True
                        self.dash_timer = self.dash_duration

            # player move
            player_speed = self.player.speed

            if self.dashing:
                if self.dash_timer:
                    player_speed = self.dash_speed
                    self.dash_timer -= 1
                else:
                    self.dashing = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player.rect.left > 0:
                self.player.rect.x -= player_speed * fps
            if keys[pygame.K_RIGHT] and self.player.rect.right < self.screen_width:
                self.player.rect.x += player_speed * fps
            if keys[pygame.K_UP] and self.player.rect.top > 0:
                self.player.rect.y -= player_speed * fps
            if keys[pygame.K_DOWN] and self.player.rect.bottom < self.screen_height:
                self.player.rect.y += player_speed * fps

            # enemy move
            for enemy in self.enemies:
                enemy.rect.x += (self.player.rect.x - enemy.nx) / self.screen_width * enemy.speed * fps
                enemy.rect.y += (self.player.rect.y - enemy.ny) / self.screen_height * enemy.speed * fps
                if enemy.rect.x < -1000 or enemy.rect.x > 1000 + self.screen_width or enemy.rect.y < -1000 or enemy.rect.y > 1000 + self.screen_height:
                    enemy.nx = enemy.rect.x
                    enemy.ny = enemy.rect.y
                if enemy.rect.colliderect(self.player.rect):
                    del self.enemies[self.enemies.index(enemy)]
                    self.player.life -= 1
                    print("life : ", self.player.life)
                    if not self.player.life:
                        pygame.quit()
                        return False, 0
                    
            # boss move
            for boss in self.bosses:
                boss.rect.x += (1 if self.player.rect.x > boss.rect.x else -1) * boss.speed * fps
                boss.rect.y += (1 if self.player.rect.y > boss.rect.y else -1) * boss.speed * fps
                if boss.rect.colliderect(self.player.rect):
                    self.player.life -= 1
                    print("life : ", self.player.life)
                    if not self.player.life:
                        pygame.quit()
                        return False, 0

            # q skill move
            for q_skill in self.q_skills:
                q_skill.rect.y -= q_skill.speed * fps
                if q_skill.rect.y < -q_skill.size:
                    del self.q_skills[self.q_skills.index(q_skill)]
                for enemy in self.enemies:
                    if q_skill.rect.colliderect(enemy.rect):
                        enemy.life -= 1
                        if not enemy.life:
                            del self.enemies[self.enemies.index(enemy)]
                for boss in self.bosses:
                    if q_skill.rect.colliderect(boss.rect):
                        boss.life -= 1
                        if not boss.life:
                            del self.bosses[self.bosses.index(boss)]

            # screen update
            self.screen.fill(self.BLACK)

            pygame.draw.rect(self.screen, self.GREEN, self.player.rect)
            for enemy in self.enemies:
                pygame.draw.rect(self.screen, self.RED, enemy.rect)
            for boss in self.bosses:
                pygame.draw.rect(self.screen, self.BLUE, boss.rect)
            for q_skill in self.q_skills:
                pygame.draw.rect(self.screen, self.WHITE, q_skill.rect)

            pygame.display.flip()