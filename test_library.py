import json
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
from library import Library, Book

# Путь к тестовому файлу с данными
TEST_DATA_FILE: str = 'test_library.json'

class TestBook(unittest.TestCase):
    def test_to_dict(self):
        book = Book(id=1, title="Название книги", author="Автор книги", year="2021", status="в наличии")
        expected_dict = {
            'id': 1,
            'title': "Название книги",
            'author': "Автор книги",
            'year': "2021",
            'status': "в наличии"
        }
        self.assertEqual(book.to_dict(), expected_dict)

    def test_str(self):
        book = Book(id=1, title="Название книги", author="Автор книги", year="2021", status="в наличии")
        expected_str = "ID: 1, Название: Название книги, Автор: Автор книги, Год: 2021, Статус: в наличии"
        self.assertEqual(str(book), expected_str)

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.books = []  # Очистить список книг перед каждым тестом

    def tearDown(self):
        # Удалить тестовый файл после каждого теста, если он существует
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_data(self, mock_file):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        book2 = Book(id=2, title="Книга 2", author="Автор 2", year="2021", status="выдана")
        self.library.books = [book1, book2]
        self.library.save_data()
        mock_file.assert_called_once_with(TEST_DATA_FILE, 'w', encoding='utf-8')

    def test_generate_id(self):
        self.assertEqual(self.library.generate_id(), 1)
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books.append(book1)
        self.assertEqual(self.library.generate_id(), 2)
 
    @patch('builtins.input', side_effect=["Название книги", "Автор книги", "2021"])
    def test_add_book_valid_input(self, mock_input):
        self.library.generate_id = MagicMock(return_value=1)
        self.library.save_data = MagicMock()
        self.library.add_book()
        self.assertEqual(len(self.library.books), 1)
        book = self.library.books[0]
        self.assertEqual(book.title, "Название книги")
        self.assertEqual(book.author, "Автор книги")
        self.assertEqual(book.year, "2021")
        self.assertEqual(book.status, "в наличии")
        self.library.save_data.assert_called_once()

    @patch('builtins.input', side_effect=["1"])
    def test_delete_book_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books = [book1]
        self.library.save_data = MagicMock()
        self.library.delete_book()
        self.assertEqual(len(self.library.books), 0)
        self.library.save_data.assert_called_once()

    @patch('builtins.input', side_effect=["2"])
    def test_delete_book_non_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books = [book1]
        self.library.save_data = MagicMock()
        self.library.delete_book()
        self.assertEqual(len(self.library.books), 1)
        self.library.save_data.assert_not_called()

    @patch('builtins.input', side_effect=["1", "выдана"])
    def test_update_book_status_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books = [book1]
        self.library.save_data = MagicMock()
        self.library.update_book_status()
        self.assertEqual(self.library.books[0].status, "выдана")
        self.library.save_data.assert_called_once()

    @patch('builtins.input', side_effect=["2", "выдана"])
    def test_update_book_status_non_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books = [book1]
        self.library.save_data = MagicMock()
        self.library.update_book_status()
        self.assertEqual(self.library.books[0].status, "в наличии")
        self.library.save_data.assert_not_called()

    @patch('builtins.input', side_effect=["Название книги"])
    def test_title_search_existing(self, mock_input):
        book1 = Book(id=1, title="Название книги", author="Автор книги", year="2021", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.title_search()
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Название книги")

    @patch('builtins.input', side_effect=["Несуществующая книга"])
    def test_title_search_non_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year="2020", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.title_search()
        self.assertEqual(found_books, None)

    @patch('builtins.input', side_effect=["Автор книги"])
    def test_author_search_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор книги", year="2020", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.author_search()
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].author, "Автор книги")

    @patch('builtins.input', side_effect=["Несуществующий автор"])
    def test_author_search_non_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор книги", year="2020", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.author_search()
        self.assertEqual(found_books, None)

    @patch('builtins.input', side_effect=["2020"])
    def test_year_search_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор книги", year="2020", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.year_search()
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].year, "2020")

    @patch('builtins.input', side_effect=["2022"])
    def test_year_search_non_existing(self, mock_input):
        book1 = Book(id=1, title="Книга 1", author="Автор книги", year="2020", status="в наличии")
        self.library.books = [book1]
        found_books = self.library.year_search()
        self.assertEqual(found_books, None)

    def test_display_books_empty(self):
        with patch('builtins.print') as mock_print:
            self.library.display_books()
            mock_print.assert_called_once_with("Библиотека пуста.")

    def test_display_books_non_empty(self):
        book1 = Book(id=1, title="Книга 1", author="Автор книги", year="2020", status="в наличии")
        self.library.books = [book1]
        with patch('builtins.print') as mock_print:
            self.library.display_books()
            mock_print.assert_called_once_with(book1)
