import json
import os
from typing import List

# Путь к файлу с данными
DATA_FILE: str = 'test_library.json'


class Book:
    """
    Класс, представляющий книгу в библиотеке.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (str): Год издания книги.
        status (str): Статус книги (например, "в наличии" или "выдана").
    """

    def __init__(self, id: int, title: str, author: str, year: str, status: str):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    def __str__(self):
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"


class Library:
    """
    Класс, представляющий библиотеку с книгами.

    Атрибуты:
        books (List[Book]): Список книг в библиотеке.
    """

    def __init__(self):
        self.books: List[Book] = self.load_data()

    def load_data(self) -> List[Book]:
        """
        Загружает данные о книгах из файла JSON.
        """
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                data: List[dict] = json.load(file)
                return [Book(**book) for book in data]
        return []

    def save_data(self) -> None:
        """
        Сохраняет данные о книгах в файл JSON.
        """
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def generate_id(self) -> int:
        """
        Генерирует уникальный идентификатор для новой книги.
        """
        if not self.books:
            return 1
        return self.books[-1].id + 1

    def _get_valid_id(self) -> int:
        """
        Запрашивает у пользователя ввод ID книги и проверяет его корректность.
        """
        while True:
            book_id = input("Введите ID книги: ").strip()
            if book_id.isdigit():
                return int(book_id)
            print("Неверный ID. Пожалуйста, введите числовое значение.")

    def add_book(self) -> None:
        """
        Добавляет новую книгу в библиотеку.
        """
        while True:
            title: str = input("Введите название книги: ").strip()
            if not title:
                print("Название книги не может быть пустым. Пожалуйста, попробуйте снова.")
                continue
            break

        while True:
            author: str = input("Введите автора книги: ").strip()
            if not author:
                print("Автор книги не может быть пустым. Пожалуйста, попробуйте снова.")
                continue
            break

        while True:
            year: str = input("Введите год издания: ").strip()
            if not year:
                print("Год издания книги не может быть пустым. Пожалуйста, попробуйте снова.")
                continue
            break

        status: str = "в наличии"

        new_book = Book(self.generate_id(), title, author, year, status)
        self.books.append(new_book)
        self.save_data()
        print(new_book)
        print("Книга успешно добавлена!")

    def delete_book(self) -> None:
        """
        Удаляет книгу из библиотеки по её ID.
        """
        book_id: int = self._get_valid_id()
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_data()
                print(f'Книга "{book.title}" успешно удалена!')
                return
        print("Книга с таким ID не найдена.")

    def _get_valid_status(self) -> str:
        """
        Запрашивает у пользователя ввод статуса книги и проверяет его корректность.
        """
        valid_statuses = ["в наличии", "выдана"]
        while True:
            status = input("Введите статус книги (в наличии/выдана): ").strip().lower()
            if status in valid_statuses:
                return status
            print("Неверный статус. Пожалуйста, введите 'в наличии' или 'выдана'. \n")

    def update_book_status(self) -> None:
        """
        Обновляет статус книги по её ID.
        """
        book_id: int = self._get_valid_id()
        for book in self.books:
            if book.id == book_id:
                print(book)
                new_status: str = self._get_valid_status()
                book.status = new_status
                self.save_data()
                print("Статус книги успешно изменен!")
                return
        print("Книга с таким ID не найдена.")

    def search_book(self) -> None:
        """
        Позволяет пользователю искать книги по различным критериям.
        """
        while True:
            print("\nПоиск:")
            print("1. По названию")
            print("2. По автору")
            print("3. По году издания")
            print("4. Выйти из поиска")

            choice: str = input("Выберите действие: ")

            if choice == '1':
                self.title_search()
            elif choice == '2':
                self.author_search()
            elif choice == '3':
                self.year_search()
            elif choice == '4':
                print("Выход из поиска")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def title_search(self) -> List[Book]:
        """
        Ищет книги по названию.
        """
        title: str = input("Введите название книги для поиска: ").strip().lower()
        found_books: List[Book] = [book for book in self.books if book.title.lower() == title]
        if found_books:
            for book in found_books:
                print(book)
            return found_books
        else:
            print("Книги с таким названием не найдены.")

    def author_search(self) -> List[Book]:
        """
        Ищет книги по автору.
        """
        author: str = input("Введите имя автора для поиска: ").strip().lower()
        found_books: List[Book] = [book for book in self.books if book.author.lower() == author.lower()]
        if found_books:
            for book in found_books:
                print(book)
            return found_books
        else:
            print("Книги этого автора не найдены.")

    def year_search(self) -> List[Book]:
        """
        Ищет книги по году издания.
        """
        year: str = input("Введите год издания для поиска: ").strip().lower()
        found_books: List[Book] = [book for book in self.books if book.year == year]
        if found_books:
            for book in found_books:
                print(book)
            return found_books

        else:
            print(f"Книги {year} года издания не найдены.")

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке.
        """
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(book)


class LibraryApp:
    """
    Класс, представляющий приложение для управления библиотекой.
    """

    def __init__(self):
        self.library = Library()

    def main(self) -> None:
        while True:
            print("\nМеню:")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Найти книгу")
            print("4. Отобразить все книги")
            print("5. Изменить статус книги")
            print("6. Выйти")

            choice: str = input("Выберите действие: ")

            if choice == '1':
                self.library.add_book()
            elif choice == '2':
                self.library.delete_book()
            elif choice == '3':
                self.library.search_book()
            elif choice == '4':
                self.library.display_books()
            elif choice == '5':
                self.library.update_book_status()
            elif choice == '6':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    app = LibraryApp()
    app.main()