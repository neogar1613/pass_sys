import cv2
import os
from uuid import uuid4
from pathlib import Path
from settings import SRC_DIR, PEOPLES_DIR, MAX_PEOPLE_PICTURES


def generate_face_data() -> tuple:
    """ Запрашивает от пользователя имя человека, для котрого будут собираться данные с камеры.
    Определяет лицо, при успешном определении, сохраняет фото лица в .pgm .
    Возвращает кортеж с количеством сохраненных кадров и именем нового человека.
    После добавления нового человека, нужно запустить add_embeddings_service() """
    name: str = input("Введите имя человека: ")
    if not name:
        name = str(uuid4().hex)
    namedir_path = os.path.join(PEOPLES_DIR, name)
    Path(namedir_path).mkdir(parents=True, exist_ok=True)
    face_cascade = cv2.CascadeClassifier(os.path.join(SRC_DIR, 'classificator.xml'))
    camera = cv2.VideoCapture(0)
    count = 0
    while True:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            # Показать рамку при удачном распозновании лица
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            face_img = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            cv2.imwrite(os.path.join(PEOPLES_DIR, name, f'{count}.pgm'), face_img)
            count += 1
        cv2.imshow('camera', frame)
        if cv2.waitKey(int(1000/12)) & 0xff == ord("q") or count >= MAX_PEOPLE_PICTURES:
            break
    camera.release()
    cv2.destroyAllWindows()
    return (count, name)
