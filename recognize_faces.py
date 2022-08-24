import cv2
import face_recognition
import os
import pickle

from settings import SRC_DIR


def _load_embeddings_data(embeddings_file_path: str):
    """ Читает данные из файла в виде потока байтов """
    with open(embeddings_file_path, "rb") as fil:
        data = pickle.loads(fil.read())
        return data


def reconize_faces_service():
    """ Распознование лиц """
    face_cascade = cv2.CascadeClassifier(os.path.join(SRC_DIR, 'classificator.xml'))
    embeddeds_file_path: str = os.path.join(SRC_DIR, "embeddeds")
    embedded_data = _load_embeddings_data(embeddings_file_path=embeddeds_file_path)
    video_capture = cv2.VideoCapture(0)
    while True:
        _, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,
                                              scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(60, 60),
                                              flags=cv2.CASCADE_SCALE_IMAGE)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(embedded_data["encodings"], encoding)
            name = "Неопределён"
            if True in matches:
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for idx in matched_idxs:
                    name = embedded_data["names"][idx]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            names.append(name)
            for ((x, y, w, h), name) in zip(faces, names):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.imshow("reconize_faces", frame)
        if cv2.waitKey(int(1000/12)) & 0xff == ord("q"):
            break
    video_capture.release()
    cv2.destroyAllWindows()
