import pygame
import sys
import random

class PenduGame:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Jeu du pendu")
        self.clock = pygame.time.Clock()

        self.word = ""
        self.difficulty = 1
        self.score = 0

        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def draw_line(self, color, start_pos, end_pos, width):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def draw_circle(self, color, center, radius, width):
        pygame.draw.circle(self.screen, color, center, radius, width)

    def draw_text(self, text, font, color, position):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_word(self, word, font, color, position):
        text_surface = font.render(word, True, color)
        self.screen.blit(text_surface, position)

    def draw_button(self, text, font, color, position):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect.topleft)

    def draw_menu(self):
        menu_text = "MENU"
        self.draw_text(menu_text, self.font_large, (255, 0, 0), (325, 50))
        self.draw_text("Pygame", self.font_small, (255, 255, 25), (10, 10))
        self.draw_button("Jouer (bouton 1-&)", self.font_medium, (255, 255, 255), (400, 150))
        self.draw_button("Tableau des scores (bouton 2-é)", self.font_medium, (255, 255, 255), (400, 300))
        self.draw_button("Quitter (bouton 3-#)", self.font_medium, (255, 255, 255), (400, 450))
        pygame.display.flip()

    def read_words_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                words = [line.strip() for line in file.readlines()]
            return words
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return []

    def ajouter_mot(self):
        input_box = pygame.Rect(300, 300, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        font = pygame.font.Font(None, 32)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_2:
                        words_from_file = self.read_words_from_file('mots.txt')
                        if words_from_file:
                            return words_from_file
                        else:
                            print("No words found in the file.")

            self.screen.fill((255, 255, 255))
            width = 2
            pygame.draw.rect(self.screen, color, input_box, width)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, width)
            txt_surface = font.render(str(text), True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            self.draw_text("Entrer un mot a trouvé", font, (0, 0, 0), (280, 250))
            pygame.display.flip()
            self.clock.tick(30)

    def run_game(self):
        running = True
        errors = 0
        correct_letters = set()
        input_text = ""

        guess_text = "Devinez le mot:"
        lose_text = "Perdu"
        win_text = "Vous avez gagné!"
        guess_text_position = (320, 10)
        lose_text_position = (200, 300)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(input_text) == 1:
                            if input_text.lower() in self.word.lower():
                                correct_letters.add(input_text.lower())
                            else:
                                errors += 1
                                if errors >= 7:
                                    self.draw_text(lose_text, self.font_large, (255, 0, 0), lose_text_position)
                                    pygame.display.flip()
                                    pygame.time.delay(2000)
                                    running = False
                                input_text = ""
                        else:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                        input_text = chr(event.key).lower()

            self.screen.fill((255, 255, 255))

            if set(self.word.lower()) == correct_letters:
                self.draw_text(win_text, self.font_large, (0, 255, 0), lose_text_position)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False
                self.save_score(errors)
            else:
                self.draw_text(guess_text, self.font_medium, (0, 0, 0), guess_text_position)
                self.draw_word(" ".join(letter if letter in correct_letters else "_" for letter in self.word.lower()),
                               self.font_medium, (0, 0, 0), (250, 550))
                self.draw_text(input_text, self.font_medium, (0, 0, 0), (10, 10))

            self.draw_pendu(errors)

            pygame.display.flip()

    def draw_pendu(self, errors):
        if errors >= 1:
            self.draw_line((0, 0, 0), (250, 25), (250, 50), 5)
            self.draw_line((0, 0, 0), (170, 24), (250, 24), 5)
            self.draw_line((0, 0, 0), (170, 50), (200, 25), 5)
            self.draw_line((0, 0, 0), (170, 24), (170, 200), 5)
            self.draw_line((0, 0, 0), (120, 200), (300, 200), 5)

        if errors >= 2:
            self.draw_circle((0, 0, 0), (250, 62), 15, 5)

        if errors >= 3:
            self.draw_line((0, 0, 0), (250, 110), (250, 75), 5)

        if errors >= 4:
            self.draw_line((0, 0, 0), (262, 100), (250, 80), 5)

        if errors >= 5:
            self.draw_line((0, 0, 0), (237, 100), (250, 80), 5)

        if errors >= 6:
            self.draw_line((0, 0, 0), (260, 125), (250, 110), 5)

        if errors >= 7:
            self.draw_line((0, 0, 0), (240, 125), (250, 110), 5)
            self.draw_text("Perdu", self.font_large, (255, 0, 0), (200, 300))
            pygame.display.flip()
            pygame.time.delay(2000)

    def save_score(self, errors):
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

        name_input = self.get_player_name_input()
        if name_input:
            score = 7 - errors  # Plus d'erreurs signifie un meilleur score
            scores_file = 'scores.txt'

            with open(scores_file, 'a') as file:
                file.write(f"{name_input}: {errors} erreurs, Score: {score}\n")

            # Vérifier si le nombre total de scores est un multiple de 10
            with open(scores_file, 'r') as file:
                scores = file.readlines()
                if len(scores) % 10 == 0:
                    # Effacer le contenu du fichier
                    open(scores_file, 'w').close()

    def get_player_name_input(self):
        input_box = pygame.Rect(300, 300, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = True
        text = ''
        font = pygame.font.Font(None, 32)

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            self.screen.fill((255, 255, 255))
            width = 2
            pygame.draw.rect(self.screen, color, input_box, width)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, width)
            txt_surface = font.render(str(text), True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            self.draw_text("Entrez votre nom:", font, (0, 0, 0), (300, 250))
            pygame.display.flip()
            self.clock.tick(30)

        return text

    def show_scores(self):
        scores_file = 'scores.txt'
        try:
            with open(scores_file, 'r') as file:
                scores = file.readlines()

            self.screen.fill((255, 255, 255))
            self.draw_text("Tableau des scores", self.font_large, (255, 0, 0), (195, 50))

            y_position = 150
            for score in scores:
                self.draw_text(score.strip(), self.font_medium, (0, 0, 0), (200, y_position))
                y_position += 40

            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        except FileNotFoundError:
            print(f"File {scores_file} not found.")

if __name__ == "__main__":
    screen_width = 800
    screen_height = 600
    pendu_game = PenduGame(screen_width, screen_height)

    menu_active = True
    while menu_active:
        pendu_game.draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu_active = False
                    pendu_game.word = random.choice(pendu_game.read_words_from_file('mots.txt'))
                    pendu_game.run_game()
                elif event.key == pygame.K_2:
                    pendu_game.show_scores()
                elif event.key == pygame.K_3:
                    menu_active = False

    pygame.quit()
    sys.exit()