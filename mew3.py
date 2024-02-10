import os
import sys
import pygame
import requests


class Map(object):
    def __init__(self):
        self.x = 55.556
        self.y = 37.897
        self.zoom = 16
        self.type = "map"

    def ll(self):
        return str(self.y) + "," + str(self.x)

    def update(self, event):
        if event.key == pygame.K_PAGEUP and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN and self.zoom > 2:
            self.zoom -= 1


def load_map(mp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.zoom}&l={mp.type}"
    response = requests.get(map_request)
    if not response:
        print(f"Http статус: {response.status_code} ({response.reason})")
        sys.exit()

    map = "map.png"
    try:
        with open(map, "wb") as file:
            file.write(response.content)
    except IOError as mew:
        print(f"Ошибка записи, {mew}")
        sys.exit()
    return map


if __name__ == "__main__":
    pygame.init()
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    mp = Map()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            mp.update(event)
        map = load_map(mp)
        screen.blit(pygame.image.load(map), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map)
