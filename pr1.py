import random


class DungeonGame:
    def __init__(self):
        self.levels = {
            1: "Вы находитесь в первом зале подземелья. Вам нужно найти ключ, чтобы открыть дверь. В зале есть следующие предметы: ",
            2: "Вы попали во второй зал. Здесь вам нужно собрать три магических кристалла, чтобы открыть портал. Кристаллы находятся в следующих местах: ",
            3: "Вы достигли третьего зала. Здесь вам нужно ответить на загадку, чтобы получить сокровище. Загадка: 'Что всегда идет, но никогда не приходит?'"
        }
        self.items_level_1 = ["ключ", "меч", "щит"]
        self.items_level_2 = ["кристалл огня", "кристалл воды", "кристалл земли", "кристалл воздуха"]
        self.answer_riddle = "время"
        self.player_items = []
        self.current_level = 1

    def start_game(self):
        print("Добро пожаловать в игру 'Приключение в Подземелье'!")
        while self.current_level <= 3:
            self.play_level(self.current_level)

        print("Поздравляем! Вы прошли все уровни и нашли сокровище!")

    def play_level(self, level):
        print(self.levels[level])

        if level == 1:
            self.solve_level_1()
        elif level == 2:
            self.solve_level_2()
        elif level == 3:
            self.solve_level_3()

    def solve_level_1(self):
        print(", ".join(self.items_level_1))
        choice = input("Какой предмет вы хотите взять? ").strip().lower()

        if choice in self.items_level_1:
            self.player_items.append(choice)
            print(f"Вы взяли {choice}. Теперь у вас: {', '.join(self.player_items)}")
            self.current_level += 1
        else:
            print("Такого предмета нет. Попробуйте снова.")
            self.solve_level_1()

    def solve_level_2(self):
        available_crystals = random.sample(self.items_level_2, 3)
        print(", ".join(available_crystals))

        collected_crystals = set()
        while len(collected_crystals) < 3:
            choice = input("Какой кристалл вы хотите собрать? ").strip().lower()
            if choice in available_crystals:
                collected_crystals.add(choice)
                print(f"Вы собрали {choice}. У вас теперь: {', '.join(collected_crystals)}")
            else:
                print("Такого кристалла нет. Попробуйте снова.")

        self.player_items.extend(collected_crystals)
        self.current_level += 1

    def solve_level_3(self):
        answer = input("Введите ваш ответ на загадку: ").strip().lower()
        if answer == self.answer_riddle:
            print("Правильно! Вы получили сокровище!")
            self.player_items.append("сокровище")
            self.current_level += 1
        else:
            print("Неправильно. Попробуйте снова.")
            self.solve_level_3()


if __name__ == "__main__":
    game = DungeonGame()
    game.start_game()

