""" Собор векторов изображений.
В peoples папки с фотографиями людей.
В каждой папку должны быть фото одного и того же человека.
Название папки - имя человека (будет отображаться при обнаружении) """
import face_recognition
import pickle
import cv2
import os
from typing import Dict, List
from settings import SRC_DIR, PEOPLES_DIR


images_dir: str = PEOPLES_DIR
embeddeds_file_path: str = os.path.join(SRC_DIR, "embeddeds")


def _check_dirs_exists() -> bool:
    """ Проверка наличия необходимых файлов и директорий """
    if not os.path.exists(images_dir):
        print('Не нашёл папку с изображениями.')
        return False


def _get_images_data(root_path: str) -> List[Dict]:
    """ Считывает все папки внутри images_dir. Возвращает список словарей,
    каждый из которых содержит имя папки и список файлов в ней.
    images_data = [{"name": $dirname, "files": [$photo_1.jpg, ..., $photo_n.jpeg]}, ...]"""
    peoples_count = 0
    images_data = []
    for root, dirs, files in os.walk(root_path):
        if len(dirs) < 1:
            images_data.append({"name": root.split('/')[-1], 'files': files})
            peoples_count += 1
    print(f'Найдено людей: {peoples_count}')
    return images_data


def _generate_embenddings(images_data: List[Dict]) -> Dict:
    """ Читает изображения в массив, преобразует даные в нужный формат,
    находит лица на каждом изображении, вычисляет эмбеддинги.
    Возвращает словарь, содержащий имена и эмбеддинги для каждого имени.
    embeddings_data = {"encodings": knownEncodings, "names": knownNames} """
    faces_count = 0
    images_count = 0
    embeddings = []
    names = []
    # перебираем все папки с изображениями
    for img_data in images_data:
        name: str = img_data.get("name")
        images: List[str] = img_data.get("files")
        # загружаем изображение и конвертируем его из BGR (OpenCV ordering) в dlib ordering (RGB)
        for img in images:
            image = cv2.imread(os.path.join(images_dir, name, img))
            images_count += 1
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # получаем лица на изображении
            faces = face_recognition.face_locations(rgb, model='hog')
            faces_count += len(faces)
            # вычисляем эмбеддинги для каждого лица
            encodings = face_recognition.face_encodings(rgb, faces)
            # loop over the encodings
            for encoding in encodings:
                embeddings.append(encoding)
                names.append(name)
    print(f'Изображений обработано: {images_count}')
    print(f'Лиц обнаружено: {faces_count}')
    return {"encodings": embeddings, "names": names}


def save_embeddings_data(embeddings_data: Dict):
    """ Пишет полученныые данные в файл в виде потока байтов """
    with open(embeddeds_file_path, "wb") as fil:
        fil.write(pickle.dumps(embeddings_data))


def add_embeddings_service():
    dirs_exists: bool = _check_dirs_exists()
    if dirs_exists is False:
        exit()
    print('START')
    print('#'*40)
    images_data: List[Dict] = _get_images_data(root_path=images_dir)
    embenddings_data: Dict = _generate_embenddings(images_data=images_data)
    save_embeddings_data(embeddings_data=embenddings_data)
    print('#'*40)
    print('END')
