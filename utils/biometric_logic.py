import cv2
import numpy as np
import os

def compare_faces(image_path1, image_path2):
    """
    Compares two face images using ORB feature matching.
    Returns: (bool, float) -> (is_match, similarity_score)
    """
    try:
        # Load images in grayscale
        img1 = cv2.imread(str(image_path1), cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(str(image_path2), cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            return False, 0.0

        # Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=1000)

        # Find keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            return False, 0.0

        # Use BFMatcher to find matches
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Sort matches by distance (lower is better)
        matches = sorted(matches, key=lambda x: x.distance)

        # Calculate a similarity score
        # We look at the top matches that are reasonably close
        good_matches = [m for m in matches if m.distance < 50]
        
        if not kp1 or not kp2:
            return False, 0.0
            
        score = (len(good_matches) / max(len(kp1), len(kp2))) * 100
        
        # In a real forensic system, we'd use deep learning (like FaceNet).
        # For this prototype, a score > 5 indicates reasonable similarity for ORB logic.
        is_match = score > 4.5 
        
        return is_match, round(score, 2)

    except Exception as e:
        print(f"Biometric logic error: {e}")
        return False, 0.0

def save_base64_image(base64_str, output_path):
    """Decodes a base64 string and saves it as an image file."""
    import base64
    try:
        if "base64," in base64_str:
            base64_str = base64_str.split("base64,")[1]
        
        img_data = base64.b64decode(base64_str)
        with open(output_path, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"Failed to save base64 image: {e}")
        return False
