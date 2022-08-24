import os
import face_recognition
import pickle
from typing import List
import cv2
from settings import SRC_DIR


def load_embeddings_data(embeddings_file_path: str):
    """ Читает данные из файла в виде потока байтов """
    with open(embeddings_file_path, "rb") as fil:
        data = pickle.loads(fil.read())
        return data


face_cascade = cv2.CascadeClassifier(os.path.join(SRC_DIR, 'classificator.xml'))
embeddeds_file_path: str = os.path.join(SRC_DIR, "embeddeds")
embedded_data = load_embeddings_data(embeddings_file_path=embeddeds_file_path)

video_capture = cv2.VideoCapture(0)


def reconize_faces_service()

while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(60, 60),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    # convert the input frame from BGR to RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
       # Compare encodings with encodings in embedded_data["encodings"]
       # Matches contain array with boolean values and True for the embeddings it matches closely
       # and False for rest
        matches = face_recognition.compare_faces(embedded_data["encodings"],
         encoding)
        # set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                # Check the names at respective indexes we stored in matchedIdxs
                name = embedded_data["names"][i]
                # increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            # set name which has highest count
            name = max(counts, key=counts.get)
        # update the list of names
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(int(1000/12)) & 0xff == ord("q"):
        break
video_capture.release()
cv2.destroyAllWindows()
