import Dot
import main
import Populations
import pygame


class Obstacle(pygame.sprite.DirtySprite):

    def __init__(self, screen: pygame.rect, location: tuple):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface([location[0], location[1]])
        self.image.fill((250, 100, 0))
        self.rect = pygame.rect.Rect((location[2], location[3]),
                                     self.image.get_rect().size)
        self.screen = screen


class ObstactlePop(pygame.sprite.Group):

    def __init__(self, pop: int, screen: pygame.Surface) -> None:
        pygame.sprite.Group.__init__(self)
        self.screen = screen
        for _ in range(pop):
            tmp_obs = Obstacle(screen, (0,0,0,0))
            self.add(tmp_obs)

