import arcade
import time

# Константы_размер окна
SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Rabbit&Carrots"

# Константы_размеры спрайтов
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 1.2
CARROTS_SCALING = TILE_SCALING
PORTAL_SCALING = TILE_SCALING * 1.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Скорость перемещения игрока, в пикселях на кадр
PLAYER_SPEED = 8
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 22

PLAYER_START_X = SPRITE_PIXEL_SIZE * 2
PLAYER_START_Y = SPRITE_PIXEL_SIZE * 1

# Константы, используемые для отслеживания того, смотрит ли игрок влево или вправо
RIGHT_FACING = 0
LEFT_FACING = 1

# Константы слоев
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_CARROTS = "Carrot"
LAYER_NAME_BACKGROUND = "images/background.png"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_PORTAL = "Portals"

# Пустой список для таблицы лидеров
leader_board = []


def load_texture(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerCharacter(arcade.Sprite):
    """Класс игровой персонаж"""

    def __init__(self):

        super().__init__()

        self.direction_of_view = RIGHT_FACING
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Загрузка текстур для стояния на месте и прыжка
        self.texture_in_place = load_texture("images/animated_characters/rabbit_front.png")
        self.texture_in_jump = load_texture("images/animated_characters/rabbit_up.png")
        self.texture_in_fall = load_texture("images/animated_characters/rabbit_front.png")

        # Изображения для передвижения персонажа
        main_path = "images/animated_characters"

        # Загрузка текстур для ходьбы
        self.textures_walk = []
        for i in range(3):
            texture = load_texture(f"{main_path}/rabbit_right_{i}.png")
            self.textures_walk.append(texture)

        # Изначальная текстура нахождения на месте
        self.texture = self.texture_in_place[0]

    def update_animation(self, delta_time: float = 30 / 60):

        # Определение направления взгляда игрока
        if self.change_x < 0 and self.direction_of_view == RIGHT_FACING:
            self.direction_of_view = LEFT_FACING
        elif self.change_x > 0 and self.direction_of_view == LEFT_FACING:
            self.direction_of_view = RIGHT_FACING

        # Анимация прыжка
        if self.change_y > 0:
            self.texture = self.texture_in_jump[self.direction_of_view]
            return
        elif self.change_y < 0:
            self.texture = self.texture_in_fall[self.direction_of_view]
            return

        # Неподвижное состояние
        if self.change_x == 0:
            self.texture = self.texture_in_place[self.direction_of_view]
            return

        # Анимация ходьбы
        self.cur_texture += 1
        if self.cur_texture >= 3:
            self.cur_texture = 0
        self.texture = self.textures_walk[self.cur_texture][
            self.direction_of_view
        ]


class MyGame(arcade.Window):
    """
    Класс Игры.
    """

    def __init__(self):
        """
        Initializer for the game
        """
        # Вызов родительского класса и установка окна
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.start_time = None
        self.time_spent = None

        # Объект для карты уровня
        self.tile_map = None
        self.tile_map1 = None

        # Объект сцены
        self.scene = None

        # Переменная игрока
        self.player_sprite = None

        # Физический движок
        self.physics_engine = None

        # Камера для прокрутки экрана
        self.camera = None

        # Камера для отрисовки интерфейса
        self.gui_camera = None

        # Текущий счет
        self.score = None

        # Звук
        self.carrots_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def setup(self):
        """Настройка игры. Функция перезапуска"""
        self.start_time = time.time()

        #Переменная для проверки перехода на уровень
        self.check = 2
        
        # Установка камер
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Имя карты
        map_name = "map.json"

        # Опции для слоя карты уровня
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_CARROTS: {
                "use_spatial_hash": True,
            },
        }

        # Загрузка карты уровня
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Создание новой сцены с помощью TileMap, слои добавляются автоматически
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Перезапуск счета
        self.score = 0

        # Размещение игрока в заданных координатах
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Создание физического движка (гравитации)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )
        
    #Создание второго уровня игры   
    def level2(self):
        #Переменная для перехода на уровень
        self.check = 1
        
        # Установка камер
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Имя карты
        map_name = "map_02.json"

        # Опции для слоя карты уровня
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_CARROTS: {
                "use_spatial_hash": True,
            },
        }

        # Загрузка карты уровня
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Создание новой сцены с помощью TileMap, слои добавляются автоматически
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Перезапуск счета
        self.score = 0

        # Размещение игрока в заданных координатах
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Создание физического движка (гравитации)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )

    def draw_rating(self):
        """ --- Отрисовка рейтинга --- """

        formatted_time = self.stopwatch()

        start_x = 10
        start_y = self.height - 20
        font_size = 16

        arcade.draw_text(formatted_time, start_x=start_x, start_y=start_y,
                         color=arcade.color.WHITE, font_size=font_size)

        for i, num in enumerate(sorted(leader_board)[:20]):
            arcade.draw_text(f"{i + 1} - {num}", start_x=start_x, start_y=start_y - (20 * (i + 1)),
                             color=arcade.color.WHITE, font_size=font_size)

    def on_draw(self):

        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            arcade.load_texture(LAYER_NAME_BACKGROUND)
                                            )
        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

        # отрисовка панели управления
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            16,
        )

        restart_text = "R - restart game"
        arcade.draw_text(
            restart_text,
            self.width - 180,
            self.height - 30,
            arcade.csscolor.WHITE,
            16,
        )
        quit_text = "Q - quit game"
        arcade.draw_text(
            quit_text,
            self.width - 180,
            self.height - 50,
            arcade.csscolor.WHITE,
            16,
        )

        # отрисовка рейтинга
        self.draw_rating()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.R:
            self.setup()
        elif key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def stopwatch(self):
        # --- Время начала отсчета ---

        # сохранение затраченного времени
        self.time_spent = time.time()

        # вычисление прошедшего время, как разница между затраченным и начальным временем
        timer = (self.time_spent - self.start_time)

        # возвращаем время в формате строки с двумя знаками после запятой
        return f"{timer: .2f}"

    def center_camera_to_player(self):
        """ Центрирование камеры на игроке """

        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, 0.5)

    def generate_portal(self):
        """Создание портала"""

        # Начальные координаты портала
        portal_pos = (1730, 230)

        # Создание нового спрайта и добавление на сцену
        portal_sprite = arcade.Sprite("images/portal.png", PORTAL_SCALING)
        portal_sprite.position = portal_pos
        self.scene.add_sprite(LAYER_NAME_PORTAL, portal_sprite)

    def on_update(self, delta_time):
        """Движение и игровая логика"""
        
        # Обновление положения игрока с помощью физического движка
        self.physics_engine.update()

        # Обновление анимации
        self.scene.update_animation(
            delta_time, [LAYER_NAME_CARROTS, LAYER_NAME_PLAYER]
        )

        carrot_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_CARROTS]
        )

        for carrot in carrot_hit_list:
            carrot.remove_from_sprite_lists()
            self.score += 1

            if self.score == 4:
                self.generate_portal()
                arcade.play_sound(self.carrots_sound)
        try:
            # Проверка столкновения игрока с порталом
            portal_hit_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene["Portals"]
            )

            for portal in portal_hit_list:
                # Remove the portal
                portal.remove_from_sprite_lists()
                timer = self.stopwatch()
                leader_board.append(timer)
                # Проверяем на какой уровень нужно идти
                if self.check == 2:
                    self.level2()
                elif self.check == 1:
                    self.setup()
        except:
            ...

        # Центрирование камеры на игроке
        self.center_camera_to_player()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
