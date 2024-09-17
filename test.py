import unittest
import pygame
import random
from unittest.mock import MagicMock, patch


# 导入被测试的模块，这里假设被测试的代码在一个名为main.py的文件中
from main import load_image, scale_image, generate_blocks, draw_button, draw_menu, draw_difficulty_selection, draw_board, \
    draw_slots, check_slots, remove_matching, draw_timer, draw_victory_screen, draw_defeat_screen


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # 创建一个模拟的屏幕对象
        self.mock_screen = MagicMock()

    def tearDown(self):
        pygame.quit()

    @patch('pygame.image.load')
    def test_load_image(self, mock_load):
        mock_image = MagicMock()
        mock_load.return_value = mock_image
        image = load_image('test_image.png')
        self.assertEqual(image, mock_image)

    def test_scale_image(self):
        test_image = pygame.Surface((100, 100))
        scaled_image = scale_image(test_image, (50, 50))
        self.assertEqual(scaled_image.get_size(), (50, 50))

    def test_generate_blocks(self):
        patterns = [(1, 1), (2, 1), (3, 1)]
        blocks = generate_blocks(patterns)
        self.assertEqual(len(blocks), 11)

    def test_draw_button(self):
        draw_button('Test', 100, 100, 200, 50, True)
        # 检查函数内部的调用是否正确
        self.mock_screen.draw.rect.assert_called()
        self.mock_screen.blit.assert_called()

    def test_draw_menu(self):
        start_button, quit_button = draw_menu()
        self.assertEqual(type(start_button), pygame.Rect)
        self.assertEqual(type(quit_button), pygame.Rect)
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1)

    def test_draw_difficulty_selection(self):
        easy_button, hard_button = draw_difficulty_selection()
        self.assertEqual(type(easy_button), pygame.Rect)
        self.assertEqual(type(hard_button), pygame.Rect)
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1)

    def test_draw_board(self):
        draw_board()
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1 + len(blocks))

    def test_draw_slots(self):
        draw_slots()
        # 检查函数内部的调用是否正确
        self.assertEqual(self.mock_screen.draw.rect.call_count, MAX_SLOTS + 1)
        self.assertEqual(self.mock_screen.blit.call_count, len(slots))

    def test_check_slots(self):
        slots = [1, 1, 1]
        self.assertEqual(check_slots(), True)
        slots = [1, 2, 3]
        self.assertEqual(check_slots(), False)

    def test_remove_matching(self):
        slots = [1, 1, 1, 2, 3]
        remove_matching()
        self.assertEqual(slots, [2, 3])

    def test_draw_timer(self):
        draw_timer(60000)
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1)

    def test_draw_victory_screen(self):
        restart_button, quit_button = draw_victory_screen()
        self.assertEqual(type(restart_button), pygame.Rect)
        self.assertEqual(type(quit_button), pygame.Rect)
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1)

    def test_draw_defeat_screen(self):
        restart_button, quit_button = draw_defeat_screen()
        self.assertEqual(type(restart_button), pygame.Rect)
        self.assertEqual(type(quit_button), pygame.Rect)
        # 检查函数内部的调用是否正确
        self.mock_screen.blit.assert_called()
        self.assertEqual(self.mock_screen.blit.call_count, 1)


if __name__ == '__main__':
    unittest.main()
