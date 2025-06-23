import pygame
from pygame.locals import *
import sys
import time
import random


class Game:

    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ""
        self.word = ""
        self.time_start = 0
        self.total_time = 0
        self.accuracy = "0%"
        self.results = "Time: 0 Accuracy 0% WPM: 0"
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULTS_C = (255, 70, 70)

        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill([0, 0, 0])
        pygame.display.set_caption("Typing speed test")

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)

    def get_sentence(self):
        with open("sentences.txt", "r") as f:
            sentences = f.read().split("\n")
            sentence = random.choice(sentences)
            return sentence

    def show_results(self, screen):
        self.total_time = time.time() - self.time_start

        # Accuracy
        count = 0
        for i, c in enumerate(self.word):
            try:
                if self.input_text[i] == c:
                        count += 1
            except:
                pass
        
        self.accuracy = count / len(self.word) * 100

        # Words per minut
        self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
        self.end = True
        print(self.total_time)

        self.results = (
            f"Time: {str(round(self.total_time))} secs "
            f"Accuracy: {str(round(self.accuracy))}% "
            f"WPM: {str(round(self.wpm))}"
        )

        self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))
        print(self.results)

        pygame.display.update()

    def reset_game(self):
        self.screen.fill([0, 0, 0])

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = ""
        self.word = ""
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()

        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()
        self.active = True

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)

            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if x >= 310 and x <= 510 and y >= 390 and self.end:
                        self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if self.time_start == 0:
                            self.time_start = time.time()

                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULTS_C)

                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[: -1]
                        else:
                            self.input_text += event.unicode

                if self.end:
                    self.draw_text(self.screen, "Reset", self.h - 70, 26, (100, 100, 100))

                pygame.display.update()

            clock.tick(60)
                

def main():
    Game().run()


if __name__ == "__main__":
    main()
