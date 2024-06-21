from werkzeug.utils import secure_filename #Sanitize filename
from global_vars.init_env import *
import os, shutil, mimetypes

mimetypes.init()

book_files_save_directory = os.environ.get('FILE_STORAGE_PATH') if os.environ.get('FILE_STORAGE_PATH')!=None else '../.ebook_files'
book_images_save_directory = os.environ.get('BOOK_IMAGE_STORAGE_PATH') if os.environ.get('BOOK_IMAGE_STORAGE_PATH')!=None else '../.book_images'
user_images_save_directory = os.environ.get('USER_IMAGE_STORAGE_PATH') if os.environ.get('USER_IMAGE_STORAGE_PATH')!=None else '../.user_images'
#Try to create directory for ebooks and images
try:
    os.mkdir(book_files_save_directory)
except FileExistsError:
    pass

try:
    os.mkdir(book_images_save_directory)
except FileExistsError:
    pass

try:
    os.mkdir(user_images_save_directory)
except FileExistsError:
    pass


def get_save_ebook_path(id: int, name: str):
    save_dir = os.path.join(os.path.abspath(book_files_save_directory), str(id))
    save_dir = os.path.join(save_dir, name)
    return save_dir

def get_save_user_image_path(id: int, name: str):
    save_dir = os.path.join(os.path.abspath(user_images_save_directory), str(id))
    save_dir = os.path.join(save_dir, name)
    return save_dir

def get_save_book_image_path(id: int, name: str):
    save_dir = os.path.join(os.path.abspath(book_images_save_directory), str(id))
    save_dir = os.path.join(save_dir, name)
    return save_dir

def add_file_with_name(file: bytes, id: int, name: str, save_directory:str):
    save_dir = os.path.join(os.path.abspath(save_directory), str(id))
    try:
        os.mkdir(save_dir)
    except FileExistsError:
        pass

    with open(os.path.join(save_dir, name), 'wb') as f:
        f.write(file)

def delete_file_with_name(id: int, name: str, save_directory: str):
    save_dir = os.path.join(save_directory, str(id))
    file_path = os.path.join(save_dir, name)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

def delete_dir_with_id(id: int, save_directory: str):
    abs_save_directory = os.path.abspath(save_directory)
    book_dir_path = os.path.join(abs_save_directory, str(id))
    try:
        shutil.rmtree(book_dir_path)
    except FileNotFoundError:
        pass

def save_book_image(image: bytes, id: int, name: str):
    add_file_with_name(image, id, name, book_images_save_directory)

def delete_book_image(id: int, name: str):
    delete_file_with_name(id, name, book_images_save_directory)

def delete_book_image_dir(id: int):
    delete_dir_with_id(id, book_images_save_directory)

def save_user_image(image: bytes, id: int, name: str):
    add_file_with_name(image, id, name, user_images_save_directory)

def delete_user_image(id: int, name: str):
    delete_file_with_name(id, name, user_images_save_directory)

def delete_user_image_dir(id: int):
    delete_dir_with_id(id, user_images_save_directory)

def save_ebook_file(ebook: bytes, id: int, name: str):
    add_file_with_name(ebook, id, name, book_files_save_directory)

def delete_ebook_file(id: int, name: str):
    delete_file_with_name(id, name, book_files_save_directory)

def delete_ebook_files_dir(id: int):
    delete_dir_with_id(id, book_files_save_directory)

