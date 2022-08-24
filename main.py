""" Точка входа.
    Для корректной установки face_recognition
    sudo apt-get install libboost-all-dev libgtk-3-dev build-essential cmake """
from pathlib import Path

from add_embeddings import add_embeddings_service
from add_face_from_cam import generate_face_data
from settings import SRC_DIR, PEOPLES_DIR


def create_dirs():
    Path(SRC_DIR).mkdir(parents=True, exist_ok=True)
    Path(PEOPLES_DIR).mkdir(parents=True, exist_ok=True)


def add_new_people():
    pictures_count, name = generate_face_data()
    print(f'Собрано {pictures_count} изображений для {name}')


def main():
    create_dirs()
    #add_new_people()
    #add_embeddings_service()



if __name__ == '__main__':
    main()
