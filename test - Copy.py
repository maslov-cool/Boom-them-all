import pygame
import os
import sys
import random


# инициализация Pygame:
pygame.init()
# размеры окна:
size = width, height = 500, 500
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 50)
        self.rect.y = random.randrange(height - 51)
        while (pygame.sprite.spritecollideany(self, all_sprites) and
               pygame.sprite.spritecollideany(self, all_sprites) != self):
            self.rect.x = random.randrange(width - 50)
            self.rect.y = random.randrange(height - 51)
        self.flag = False

    def update(self, *args):
        if self.flag:
            self.rect = self.rect.move(random.randrange(3) - 1,
                                       random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.flag = True
            self.image = self.image_boom


if __name__ == '__main__':
    # команды рисования на холсте
    pygame.display.set_caption('Boom them all')

    running = True
    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()
    x, y = 10, 10
    for _ in range(20):
        Bomb(all_sprites)
    clock = pygame.time.Clock()
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update(event)
        clock.tick(60)
        # обновление экрана
        pygame.display.flip()
    # завершение работы:
    pygame.quit()
