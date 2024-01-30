import psycopg2 as psp2
import tkinter as tk
from config import host, db_name, user, password, port


def connection():
    '''Функция, устанавливающая соединение с БД и
    возвращающая объект типа Cursor.'''
    conn = psp2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
        )
    return conn.cursor()


def on_genre(request: str) -> list[str]:
    '''Функция реализует запрос пользователя, отправляя запрос в таблицу
    "author" БД дял поиска по жанрам. Возвращает список найденных
    книг или пустой список.'''
    cur = connection()
    cur.execute(
        "select b.title from book b join author a on b.author_id = a.id join genre g on g.id = b.genre_id WHERE g.genre_name iLIKE %(request)s;", {'request': f'%{request}%'}
        )
    genre_list: list = [el for el in cur.fetchall()]
    cur.close()
    return genre_list


def on_authors(request: str) -> list[str]:
    '''Функция реализует запрос пользователя, отправляя запрос в таблицу
    "author" БД дял поиска по фамилии. Возвращает список найденных
    книг или пустой список.'''
    cur = connection()
    cur.execute(
        "select b.title from book b join author a on b.author_id = a.id WHERE a.last_name iLIKE %(request)s;", {'request': f'%{request}%'}
        )
    authors_list: list = [el for el in cur.fetchall()]
    cur.close()
    return authors_list


def on_title(request: str) -> list[str]:
    '''Функция реализует запрос пользователя, отправляя запрос в таблицу
    "book" БД для поиска по названию. Возвращает список найденных
    книг или пустой список.'''
    cur = connection()
    cur.execute(
        "select title from book  WHERE title iLIKE %(request)s;", {'request': f'%{request}%'}
        )
    title_list: list = [el for el in cur.fetchall()]
    cur.close()
    return title_list


def book_searching(request: str) -> dict:
    '''Функция принимает на вход ввод с клавиатуры пользователем
    и поочередно отправляет запросы в функции - поисковики.'''
    authors: list = on_authors(request)
    title: list = on_title(request)
    genre: list = on_genre(request)
    final_list: list = list(tuple(authors + title + genre))
    quantity_list: list = [i for i in range(1, len(final_list) + 1)]
    books_dict: dict = dict(zip(quantity_list, final_list))
    for num, book in books_dict.items():
        print(f"{num} - {book[0]}")
    return books_dict


print("Здравствуйте! Введите параметры поиска нужной книги: ")
request_content: str = input().lower()
responce: dict = book_searching(request_content)
counter: int = len(responce)
print("Выберите нужную вам книгу, указав ее номер!")
print()
while True:
    try:
        print((f"Пожалуйста, введите целое число от 1 до {counter}: "))
        choise = int(input())
        if choise < 1 or choise > counter:
            raise ValueError
        print(f"'{responce[choise][0]}' - отличный выбор! \n Читайте на здоровье=)")
        print("До новых встреч!")
        break
    except ValueError:
        print("Неверно. Попробуйте еще разок!")
