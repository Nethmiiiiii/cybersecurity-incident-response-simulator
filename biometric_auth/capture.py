import cv2
import os

FACES_DIR = "data/faces"

def capture_face(username, sample_count=3):
    os.makedirs(FACES_DIR, exist_ok=True)
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    image_paths = []
    sample_num = 1

    print(f"[INFO] Capturing {sample_count} face samples. Press SPACE each time.")

    while sample_num <= sample_count:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, f"Sample {sample_num}/{sample_count} — Press SPACE",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow("Biometric Capture", frame)
        key = cv2.waitKey(1)

        if key == 32:  # SPACE
            if len(faces) > 0:
                image_path = f"{FACES_DIR}/{username}_{sample_num}.jpg"
                cv2.imwrite(image_path, frame)
                print(f"[INFO] Sample {sample_num} saved.")
                image_paths.append(image_path)
                sample_num += 1
            else:
                print("[WARN] No face detected. Try again.")

        elif key == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()
    return image_paths if len(image_paths) == sample_count else None

def capture_single_face(label="temp_auth"):
    os.makedirs(FACES_DIR, exist_ok=True)
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("[INFO] Press SPACE to scan your face.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, "Press SPACE to authenticate",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow("Biometric Authentication", frame)
        key = cv2.waitKey(1)

        if key == 32:  # SPACE
            if len(faces) > 0:
                image_path = f"{FACES_DIR}/{label}.jpg"
                cv2.imwrite(image_path, frame)
                cam.release()
                cv2.destroyAllWindows()
                return image_path
            else:
                print("[WARN] No face detected. Try again.")

        elif key == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()
    return None