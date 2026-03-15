from deepface import DeepFace
from capture import capture_face, capture_single_face
from database import get_all_users, log_event, save_user
import os

def register_user(username):
    image_paths = capture_face(username, sample_count=3)

    if image_paths is None:
        return False, "no_face"

    saved = save_user(username, image_paths)
    if saved:
        log_event(username, "REGISTERED")
        return True, "ok"
    else:
        # clean up saved images
        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)
        return False, "duplicate"

def authenticate():
    image_path = capture_single_face("temp_auth")

    if image_path is None:
        return None, "no_face"

    users = get_all_users()
    match_scores = {}

    for username, stored_path in users:
        if not os.path.exists(stored_path):
            continue
        try:
            result = DeepFace.verify(
                img1_path=image_path,
                img2_path=stored_path,
                enforce_detection=False
            )
            if result["verified"]:
                distance = result["distance"]
                if username not in match_scores or distance < match_scores[username]:
                    match_scores[username] = distance
        except Exception as e:
            print(f"[ERROR] Comparing with {username}: {e}")
            continue

    if os.path.exists(image_path):
        os.remove(image_path)

    if match_scores:
        best_match = min(match_scores, key=match_scores.get)
        log_event(best_match, f"LOGIN_SUCCESS (dist={match_scores[best_match]:.3f})")
        return best_match, "success"

    log_event("unknown", "LOGIN_FAILED")
    return None, "failed"