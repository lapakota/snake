import unittest

from shake import *


class TestClassGame(unittest.TestCase):
    def test_init(self):
        game = Game()
        self.assertEqual(game.fps, 7)
        self.assertEqual(game.score, 0)
        self.assertEqual(game.lives, 3)
        self.assertFalse(game.is_paused)

    def test_change_attributes(self):
        game = Game()
        fps = game.fps
        score = game.score
        lives = game.lives
        flag = game.is_paused
        game.fps = 15
        game.score = 10
        game.lives = 5
        game.is_paused = True
        self.assertNotEqual(game.fps, fps)
        self.assertNotEqual(game.score, score)
        self.assertNotEqual(game.lives, lives)
        self.assertNotEqual(game.is_paused, flag)

    def test_equality(self):
        game1 = Game()
        game2 = Game()
        self.assertNotEqual(game1, game2)


class TestClassSnake(unittest.TestCase):
    def test_init(self):
        snake = Snake(0, 0, 'orange', 'white')
        self.assertEqual(snake.x, 0)
        self.assertEqual(snake.y, 0)
        self.assertEqual(snake.dx, 0)
        self.assertEqual(snake.dy, 0)
        self.assertEqual(snake._dx, 0)
        self.assertEqual(snake._dy, 0)
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.body, [(snake.x, snake.y)])
        self.assertEqual(snake.color, 'orange')
        self.assertEqual(snake.eye_color, 'white')

    def test_check_death(self):
        snake1 = Snake(-1, 0, 'orange', 'white')
        snake2 = Snake(WIDTH, 0, 'orange', 'white')
        snake3 = Snake(0, -1, 'orange', 'white')
        snake4 = Snake(0, HEIGHT, 'orange', 'white')
        snake5 = Snake(40, 40, 'orange', 'white')
        walls = [Wall(40, 40, 'gray')]
        self.assertTrue(snake1.check_death(walls))
        self.assertTrue(snake2.check_death(walls))
        self.assertTrue(snake3.check_death(walls))
        self.assertTrue(snake4.check_death(walls))
        self.assertTrue(snake5.check_death(walls))

    def test_equality(self):
        snake1 = Snake(0, 0, 'orange', 'white')
        snake2 = Snake(0, 0, 'orange', 'white')
        self.assertNotEqual(snake1, snake2)


class TestClassFood(unittest.TestCase):
    def test_init(self):
        food = Food(0, 0, 'red')
        self.assertEqual(food.x, 0)
        self.assertEqual(food.y, 0)
        self.assertEqual(food.color, 'red')

    def test_apple_give_bonus(self):
        food = Food(0, 0, 'red')
        snake = Snake(0, 0, 'orange', 'white')
        game = Game()
        score = game.score
        length = snake.length
        food.give_bonus(snake, game)
        self.assertNotEqual(game.score, score)
        self.assertNotEqual(snake.length, length)

    def test_speed_up_give_bonus(self):
        food = SpeedUp(0, 0, 'red')
        snake = Snake(0, 0, 'orange', 'white')
        game = Game()
        score = game.score
        fps = game.fps
        food.give_bonus(snake, game)
        self.assertNotEqual(game.score, score)
        self.assertNotEqual(game.fps, fps)

    def test_speed_down_give_bonus(self):
        food = SpeedDown(0, 0, 'red')
        snake = Snake(0, 0, 'orange', 'white')
        game = Game()
        score = game.score
        fps = game.fps
        food.give_bonus(snake, game)
        self.assertNotEqual(game.score, score)
        self.assertNotEqual(game.fps, fps)

    def test_equality(self):
        food1 = Food(0, 0, 'red')
        food2 = Food(0, 0, 'red')
        speed_up1 = SpeedUp(0, 0, 'red')
        speed_up2 = SpeedUp(0, 0, 'red')
        speed_down1 = SpeedDown(0, 0, 'red')
        speed_down2 = SpeedDown(0, 0, 'red')
        self.assertNotEqual(food1, food2)
        self.assertNotEqual(speed_up1, speed_up2)
        self.assertNotEqual(speed_down1, speed_down2)


class TestClassPortal(unittest.TestCase):
    def test_init(self):
        portals = Portal(0, 0, 40, 40, 'white', 'red')
        self.assertEqual(portals.f_x, 0)
        self.assertEqual(portals.f_y, 0)
        self.assertEqual(portals.s_x, 40)
        self.assertEqual(portals.s_y, 40)
        self.assertEqual(portals.f_color, 'white')
        self.assertEqual(portals.s_color, 'red')

    def test_collision_with_portal(self):
        snake1 = Snake(0, 0, 'orange', 'white')
        portals1 = Portal(0, 0, 40, 40, 'white', 'red')
        snake2 = Snake(40, 40, 'orange', 'white')
        portals2 = Portal(0, 0, 40, 40, 'white', 'red')

        portals1.collision_with_portal(snake1)
        portals2.collision_with_portal(snake2)

        self.assertEqual(snake1.x, portals1.s_x)
        self.assertEqual(snake1.y, portals1.s_y)

        self.assertEqual(snake2.x, portals2.f_x)
        self.assertEqual(snake2.y, portals2.f_y)

    def test_equality(self):
        portals1 = Portal(0, 0, 40, 40, 'white', 'red')
        portals2 = Portal(0, 0, 40, 40, 'white', 'red')
        self.assertNotEqual(portals1, portals2)


class TestClassWall(unittest.TestCase):
    def test_init(self):
        wall = Wall(0, 0, 'gray')
        self.assertEqual(wall.x, 0)
        self.assertEqual(wall.y, 0)
        self.assertEqual(wall.color, 'gray')

    def test_collision_with_wall(self):
        snake = Snake(0, 0, 'orange', 'white')
        wall = Wall(0, 0, 'gray')
        self.assertTrue(wall.check_collision_with_wall(snake))

    def test_equality(self):
        wall1 = Wall(0, 0, 'gray')
        wall2 = Wall(0, 0, 'gray')
        self.assertNotEqual(wall1, wall2)


class TestClassLevel(unittest.TestCase):
    def test_init(self):
        level = Level()
        self.assertEqual(level.type, 1)
        self.assertEqual(level.walls, [])
        self.assertEqual(level.portals, [])
        self.assertEqual(level.snake_cords, (0, 0))

    def test_check_new_level(self):
        level = Level()
        snake = Snake(0, 0, 'orange', 'white')
        game = Game()
        snake.length = 6
        game.score = 11
        self.assertTrue(level.check_new_level(snake, game))
        snake.length = 11
        game.score = 21
        self.assertTrue(level.check_new_level(snake, game))

    def test_equality(self):
        level1 = Level()
        level2 = Level()
        self.assertNotEqual(level1, level2)


if __name__ == '__main__':
    unittest.main()
