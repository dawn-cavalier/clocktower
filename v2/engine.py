"""Temp Documentation"""

import pygame

from queue import Queue
from collections.abc import Callable
from typing import Any


class Engine:
    work_queue: Queue[tuple[Callable[[tuple[Any]], None], tuple[Any]]]
    screen: pygame.Surface
    clock: pygame.Clock
    dt: float
    running: bool

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode((1280, 720))
        self.running = True

        self.work_queue = Queue()

    def __add_queue__(self, func: Callable[[tuple[Any]], None], params: tuple[Any]):
        self.work_queue.put((func, params))

    def __process_queue__(self):
        while not self.work_queue.empty():
            func, params = self.work_queue.get()
            func(params[0])

    # def process_controls(self):
    #     for event in pygame.event.get():

    def process_frame(self):
        for event in pygame.event.get():
            print (f"Event: {event}")
            if event.type == pygame.QUIT:
                self.running = False
        
        self.dt = self.clock.tick() / 1000


def main():
    engine = Engine()
    while engine.running:
        engine.process_frame()


if __name__ == "__main__":
    main()
