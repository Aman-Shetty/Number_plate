import cv2
import easyocr
import re

# Predefined toll rates and state names
TOLL_RATES = {
    "AP": (40, "Andhra Pradesh"), "AR": (35, "Arunachal Pradesh"), "AS": (30, "Assam"),
    "BR": (45, "Bihar"), "CG": (40, "Chhattisgarh"), "DL": (50, "Delhi"),
    "GA": (50, "Goa"), "GJ": (65, "Gujarat"), "HR": (50, "Haryana"),
    "HP": (40, "Himachal Pradesh"), "JH": (45, "Jharkhand"), "KA": (55, "Karnataka"),
    "KL": (60, "Kerala"), "MH": (60, "Maharashtra"), "MP": (50, "Madhya Pradesh"),
    "PB": (50, "Punjab"), "RJ": (35, "Rajasthan"), "TN": (45, "Tamil Nadu"),
    "UP": (40, "Uttar Pradesh"), "WB": (50, "West Bengal"),
}

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

def extract_plate_and_toll(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, None, None
    
    processed_image = preprocess_image(image)
    reader = easyocr.Reader(['en'])
    results = reader.readtext(processed_image)

    # Regex for Indian number plates
    regex = r'^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{4}$'

    for _, text, _ in results:
        plate = text.replace(" ", "").upper()
        if re.match(regex, plate):
            state_code = plate[:2]
            toll_info = TOLL_RATES.get(state_code, (100, "Unknown State"))
            return plate, toll_info[1], toll_info[0]
    return None, None, None
