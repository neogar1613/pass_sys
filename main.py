""" Точка входа.
    Для корректной установки face_recognition
    sudo apt-get install libboost-all-dev libgtk-3-dev build-essential cmake """
import click
from pathlib import Path

from add_embeddings import add_embeddings_service
from add_face_from_cam import generate_face_data
from recognize_faces import reconize_faces_service
from services.qrcode_service import qrcode_gen
from settings import SRC_DIR, PEOPLES_DIR, QRCODES_DIR


def create_dirs():
    Path(SRC_DIR).mkdir(parents=True, exist_ok=True)
    Path(PEOPLES_DIR).mkdir(parents=True, exist_ok=True)
    Path(QRCODES_DIR).mkdir(parents=True, exist_ok=True)


def add_new_people():
    pictures_count, name = generate_face_data()
    print(f'Собрано {pictures_count} изображений для {name}')

@click.command()
@click.argument("mode")
def main(mode: str):
    """
    init - create dirs;\n
    add - add new face from webcamera;\n
    addembs - add or refresh embeddings;\n
    find - reconize faces from webcamera stream; """
    if mode == 'init':
        create_dirs()
    elif mode == 'add':
        add_new_people()
    elif mode == 'addembs':
        add_embeddings_service()
    elif mode == 'find':
        reconize_faces_service()
    elif mode == 'qr_gen':
        qrcode_gen({'qq': 'ww'})
    else:
        print('Invalid "mode" argument value!')
        exit()


if __name__ == '__main__':
    main()
