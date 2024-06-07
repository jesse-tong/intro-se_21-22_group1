from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from models.book_model import Book, BookAuthor, BookGenre, Author, Genre, BookImage, BookLocation, BookFile, BookLanguage
from sqlalchemy import select, func, exists
from global_vars.database_init import db
from utils.file_utils import *
from global_vars.errors import *
from flask_login import login_user, login_required, current_user, logout_user

def add_book(title, publish_year: int=None, description=None, isbn=None, stock=None):
    #Find if any with that title and isbn exist
    if isbn != None:
        exist_book_with_same_title_isbn = db.session.query(Book).filter(Book.title == title).filter(Book.isbn == isbn).first()
        if exist_book_with_same_title_isbn:
            return False, None, BOOK_TITLE_ISBN_EXISTS
        
    new_book = Book()
    if publish_year != None:
        new_book.publish_year = publish_year
    if description != None:
        new_book.description = description
    if isbn != None:
        new_book.isbn = isbn
    if stock != None:
        new_book.stock = stock
    new_book.title = title
    try:
        db.session.add(new_book)
        db.session.commit()
        return True, new_book, None
    except:
        db.session.rollback()
        return False, None, ADD_ENTRY_ERROR

def delete_book(id: int):
    try:
        db.session.query(BookAuthor).filter(BookAuthor.bookId == id).delete()
        db.session.query(BookGenre).filter(BookGenre.bookId == id).delete()
        db.session.query(BookLocation).filter(BookLocation.bookId == id).delete()
        db.session.query(BookImage).filter(BookImage.bookId == id).delete()
        db.session.query(BookFile).filter(BookFile.bookId == id).delete()
        db.session.query(BookLanguage).filter(BookLanguage.bookId == id).delete()

        #Delete genres without a book references it
        delete_genre_subquery = ~db.session.query(BookGenre).filter(BookGenre.genreId == Genre.id).exists()
        db.session.query(Genre).filter(delete_genre_subquery).delete()

        #Delete authors that are without a book referencing it
        delete_author_subquery = ~db.session.query(BookAuthor).filter(BookAuthor.authorId == Author.id).exists()
        db.session.query(Author).filter(delete_author_subquery).delete()

        db.session.commit()
        rows_deleted = db.session.query(Book).filter(Book.id == id).delete()
        db.session.commit()
        return True, rows_deleted, None
    except:
        db.session.rollback()
        return False, 0, DELETE_ERROR

def change_book_data(book_id: int, title: str=None, publish_year: int=None, 
description: str=None, authors: list=None, genres: list=None, isbn=None, stock: int=0, languages:list[str]=None):
    genre_ids = list()
    author_ids = list()

    if authors != None:
        for author in authors:
            result, __, error = add_author(author)
            row = db.session.query(Author).filter(Author.name == author).first()
            if row:
                author_ids.append(row.id)

    if genres != None:
        for genre in genres:
            result, __, error = add_genre(genre)
            row = db.session.query(Genre).filter(Genre.name == genre).first()

            if row != None:
                genre_ids.append(row.id)

    try:
        book = db.session.query(Book).filter(Book.id == book_id).first()

        if book == None:
            return False, None, INVALID_ID
        if title != None:
            book.title = title
        if publish_year != None:
            book.publish_year = publish_year
        if description != None:
            book.description = description
        if isbn != None:
            book.isbn = isbn
        if stock != None:
            book.stock = stock
        db.session.commit()

        #Delete old genre and author data
        if genres != None:
            db.session.query(BookGenre).filter(BookGenre.bookId == book.id).delete()
        if authors != None:
            db.session.query(BookAuthor).filter(BookAuthor.bookId == book.id).delete()
        if languages != None:
            db.session.query(BookLanguage).filter(BookLanguage.bookId == book.id).delete()
        db.session.commit()

        if genres != None:
            for genre_id in genre_ids:
                book_genre = BookGenre()
                book_genre.bookId = book.id
                book_genre.genreId = genre_id
                try:
                    db.session.add(book_genre)
                    db.session.commit()
                except:
                    db.session.rollback()

        if authors != None:
            for author_id in author_ids:
                book_author = BookAuthor()
                book_author.bookId = book.id
                book_author.authorId = author_id
                try:
                    db.session.add(book_author)
                    db.session.commit()
                except:
                    db.session.rollback()

        if languages != None:
            for language in languages:
                book_language = BookLanguage()
                book_language.bookId = book.id
                book_language.language = language
                try:
                    db.session.add(book_language)
                    db.session.commit()
                except:
                    db.session.rollback()

        return True, book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR

def change_book_stock(id: int, stock: int):
    try:
        book = db.session.query(Book).filter(Book.id == id).update({Book.stock: stock})
        db.session.commit()
        return True, book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR


def decrement_book_stock(id: int):
    try:
        book = db.session.query(Book).filter(Book.id == id).update({Book.stock: Book.stock - 1})
        db.session.commit()
        return True, book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR  

def increment_book_stock(id: int):
    try:
        book = db.session.query(Book).filter(Book.id == id).update({Book.stock: Book.stock + 1})
        db.session.commit()
        return True, book, None
    except:
        db.session.rollback()
        return False, None, EDIT_ERROR  

def is_book_out_of_stock(id: int):
    book = db.session.query(Book).filter(Book.id == id).first()
    if book.stock == None or book.stock == 0:
        return True
    else:
        return False

#start_from: Where the return result index starts (from index 0)
def search_book(title: str=None, start_publish: int=None, end_publish: int=None,
 description: str=None, start_from: int=None, limit: int=None, isbn: str=None, book_id: int=None):
    query = select(Book)
    if book_id != None:
        query = query.filter(Book.id == book_id)
    if title != None:
        query = query.filter(Book.title.like('%{}%'.format(title)))
    if start_publish != None:
        query = query.filter(Book.publish_year >= start_publish)
    if end_publish != None:
        query = query.filter(Book.publish_year <= end_publish)
    if description != None:
        query = query.filter(Book.description.like('%{}%'.format(description)))
    if isbn != None:
        query = query.filter(Book.isbn == isbn)
    if start_from != None:
        query = query.offset(start_from)
    if limit != None:
        query = query.limit(limit)
    
    
    result = db.session.execute(query)
    result = result.all()
    result = [query_result[0] for query_result in result] #select unlike query return a list of tuples
    #which the first element in is the actual model object
    return True, result, None

def get_book_data(id: int):
    book = db.session.query(Book).filter(Book.id == id).first()
    res = dict()
    if book != None:
        res['id'] = book.id
        res['publish_year'] = book.publish_year
        res['description'] = book.description
        res['title'] = book.title
        res['stock'] = book.stock
        res['isbn'] = book.isbn
        res['authors'] = list()
        res['genres'] = list()
        res['languages'] = list()

        authors = db.session.query(BookAuthor.bookId, BookAuthor.authorId, Author.id, Author.place, Author.name) \
        .filter(BookAuthor.bookId == book.id).filter(BookAuthor.authorId == Author.id).join(Author).all()

        genres = db.session.query(BookGenre.bookId, BookGenre.genreId, Genre.id, Genre.name) \
            .filter(BookGenre.bookId == book.id).filter(BookGenre.genreId == Genre.id).join(Genre).all()

        languages = db.session.query(BookLanguage.bookId, BookLanguage.language) \
            .filter(BookLanguage.bookId == book.id).all()
        
        for author in authors:         
            res['authors'].append(author.name)

        for genre in genres:
            res['genres'].append(genre.name)

        for language in languages:
            res['languages'].append(language.language)

        return True, res, None
    else:
        return False, None, INVALID_ID

def get_genres(page: int = None, limit: int=None):
    try:
        query = db.session.query(Genre).distinct()
        if page != None and limit != None:
            offset = (page - 1)*limit
            query = query.offset(offset).limit(limit)
        genres = query.all()
        return True, genres, None
    except:
        return False, None, DATABASE_ERROR

def get_authors(page: int = None, limit: int=None):
    try:
        query = db.session.query(Author).distinct()
        if page != None and limit != None:
            offset = (page - 1)*limit
            query = query.offset(offset).limit(limit)
        genres = query.all()
        return True, genres, None
    except:
        return False, None, DATABASE_ERROR

def get_books_genre(genre_id: int | list[int], page: int =None, limit: int=None):
    if type(genre_id) == list:
        try:
            query = db.session.query(Book).join(BookGenre).filter(Book.id == BookGenre.bookId).filter(BookGenre.genreId.in_(genre_id))
            if page != None and limit != None and page > 0  and limit > 0:
                offset = (page - 1)*limit
                query = query.offset(offset).limit(limit)
            books_for_genres = query.all()
            
            return True, books_for_genres, None
        except:
            return False, None, DATABASE_ERROR
    else:
        try:
            query = db.session.query(Book).join(BookGenre).filter(Book.id == BookGenre.bookId).filter(BookGenre.genreId == genre_id)
            if page != None and limit != None and page > 0  and limit > 0:
                offset = (page - 1)*limit
                query = query.offset(offset).limit(limit)
            books_for_genre = query.all()

            return True, books_for_genre, None
        except:
            return False, None, DATABASE_ERROR
    
def get_books_author(author_id: int | list[int], page: int=None, limit: int=None):
    if type(author_id) == list:
        try:
            query = db.session.query(Book).join(BookAuthor).filter(Book.id == BookAuthor.bookId).filter(BookAuthor.authorId.in_(author_id))
            if page != None and limit != None and page > 0  and limit > 0:
                offset = (page - 1)*limit
                query = query.offset(offset).limit(limit)
            books_for_authors = query.all()
            return True, books_for_authors, None
        except:
            return False, None, DATABASE_ERROR
    else:
        try:
            query = db.session.query(Book).join(BookAuthor).filter(Book.id == BookAuthor.bookId).filter(BookAuthor.authorId == author_id)
            if page != None and limit != None and page > 0  and limit > 0:
                offset = (page - 1)*limit
                query = query.offset(offset).limit(limit)
            books_for_author = query.all()
            return True, books_for_author, None
        except:
            return False, None, DATABASE_ERROR

def get_book_images(book_id: int):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    images = list()
    if book != None:
        image_paths = db.session.query(BookImage).filter(BookImage.bookId == book.id).all()
        return True, image_paths, None
    else:
        return False, None, ROW_NOT_EXISTS

def add_book_image(book_id: int, file: bytes):
    return

#Add genre to database (note that when changing a book's genres and authors use change_book_data instead)
def add_genre(genre_name: str):
    genre = db.session.query(Genre).filter(Genre.name == genre_name).first()
    if not genre:
        new_genre = Genre()
        new_genre.name = genre_name
        db.session.add(new_genre)
        db.session.commit()
        return True, new_genre, None
    else:
        db.session.rollback()
        return False, None, ROW_EXISTS

def add_author(name: str, place: str=None):
    author = db.session.query(Author).filter(Author.name == name).first()
    if author == None:
        author = Author()
        author.name = name
        if place != None:
            author.place = place
        db.session.add(author)
        db.session.commit()
        return True, author, None
    else:
        db.session.rollback()
        return False, None, ROW_EXISTS 

def get_book_location(book_id: int):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if not book:
        return False, None, INVALID_ID
    else:
        result = db.session.query(BookLocation).filter(BookLocation.bookId == book_id).all()
        return True, result, None

def add_book_location(book_id: int, room_id: str, shelf_id: str):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if not book:
        return False, None, INVALID_ID
    else:
        book_location = BookLocation()
        book_location.bookId = book_id
        book_location.roomId = room_id
        book_location.shelfId = shelf_id
        try:
            db.session.add(book_location)
            db.session.commit()
            return True, book_location, None
        except:
            db.session.rollback()
            return False, None, ADD_ENTRY_ERROR

def change_book_location(book_location_id: int, room_id: str, shelf_id: str):
    book_location = db.session.query(BookLocation).filter(BookLocation.id == book_location_id).first()
    if not book_location:
        return False, None, INVALID_ID
    else:
        try:
            book_location.roomId = room_id; book_location.shelfId = shelf_id
            db.session.commit()
            return True, book_location, None
        except:
            db.session.rollback()
            return False, None, EDIT_ERROR

def delete_book_location(book_location_id: int):
    try:
        deleted_row_count = db.session.query(BookLocation).filter(BookLocation.id == book_location_id).delete()
        db.session.commit()
        return True, deleted_row_count, None
    except:
        db.session.rollback()
        return False, None, DELETE_ERROR

def advanced_search(book_id: int=None, title: str=None, publish_year: int=None,
                     description: str=None, authors: list[str]=None, genres: list[str]=None, isbn: str=None, page: int=None, limit: int=None):
    
    query = db.session.query(Book)
    if book_id != None:
        query = query.filter(Book.id == book_id)
        
    if title != None:
        query = query.filter(Book.title.like('%{}%'.format(title)))
        
    if publish_year != None:
        query = query.filter(Book.publish_year == publish_year)
        
    if description != None:
        query = query.filter(Book.description.like('%{}%'.format(description)))
        res = query.all();
    if isbn != None:
        query = query.filter(Book.isbn.like('%{}%'.format(isbn)))
    if authors != None:
        subquery = db.session.query(Author.id).filter(Author.name.in_(authors))
        query = query.join(BookAuthor).filter(BookAuthor.bookId == Book.id).filter(BookAuthor.authorId.in_(subquery))
    if genres != None:
        subquery = db.session.query(Genre.id).filter(Genre.name.in_(genres))
        query = query.join(BookGenre).filter(BookGenre.bookId == Book.id).filter(BookGenre.genreId.in_(subquery))
    if page != None and limit != None and page > 0 and limit > 0 :
        offset = (page - 1)*limit 
        query = query.offset(offset).limit(limit)
    result = query.all()
    
    return True, result, None