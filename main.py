import cv2
import easyocr
import re

# Predefined toll rates and state names for all Indian states
TOLL_RATES = {
    "AP": (40, "Andhra Pradesh"),
    "AR": (35, "Arunachal Pradesh"),
    "AS": (30, "Assam"),
    "BR": (45, "Bihar"),
    "CG": (40, "Chhattisgarh"),
    "GA": (50, "Goa"),
    "GJ": (65, "Gujarat"),
    "HR": (50, "Haryana"),
    "HP": (40, "Himachal Pradesh"),
    "JH": (45, "Jharkhand"),
    "JK": (50, "Jammu and Kashmir"),
    "KA": (55, "Karnataka"),
    "KL": (60, "Kerala"),
    "LA": (45, "Ladakh"),
    "MH": (60, "Maharashtra"),
    "ML": (35, "Meghalaya"),
    "MN": (35, "Manipur"),
    "MP": (50, "Madhya Pradesh"),
    "MZ": (30, "Mizoram"),
    "NL": (35, "Nagaland"),
    "OD": (45, "Odisha"),
    "PB": (50, "Punjab"),
    "PY": (40, "Puducherry"),
    "RJ": (35, "Rajasthan"),
    "SK": (30, "Sikkim"),
    "TN": (45, "Tamil Nadu"),
    "TR": (30, "Tripura"),
    "TS": (40, "Telangana"),
    "UP": (40, "Uttar Pradesh"),
    "UK": (45, "Uttarakhand"),
    "WB": (50, "West Bengal"),
    "DL": (50, "Delhi"),
}

def preprocess_image(image):
    """
    Preprocess the image to enhance the number plate region.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

def extract_plate_text(image_path):
    """
    Detect text from the image using EasyOCR and filter for Indian number plates.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return None

    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Initialize EasyOCR Reader
    reader = easyocr.Reader(['en'])

    # Perform OCR on the preprocessed image
    results = reader.readtext(preprocessed_image)

    # Regular expression for Indian number plates
    indian_plate_regex = r'^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{4}$'

    # Filter text results
    plate_number = None
    for _, text, confidence in results:
        cleaned_text = text.replace(" ", "").upper()
        if re.match(indian_plate_regex, cleaned_text):
            print(f"Detected Plate: {cleaned_text} (Confidence: {confidence:.2f})")
            plate_number = cleaned_text
            break

    return plate_number

def calculate_toll(plate_number):
    """
    Calculate toll based on the state code from the number plate.
    """
    state_code = plate_number[:2]  # Extract the first two letters (state code)
    toll_info = TOLL_RATES.get(state_code)

    if toll_info:
        toll_amount, state_name = toll_info
        return state_name, toll_amount
    else:
        return "Unknown State", 100  # Default toll for unknown state

if __name__ == "__main__":
    # Path to the image
    IMAGE_PATH = "test_images/number_plate.jpg"  # Replace with the image path

    # Detect number plate
    print("Detecting Indian number plate...")
    number_plate = extract_plate_text(IMAGE_PATH)

    # Calculate toll
    if number_plate:
        state_name, toll = calculate_toll(number_plate)
        print(f"Detected Number Plate: {number_plate}")
        print(f"The vehicle is registered from {state_name}. The toll charge is rupees {toll}.")
    else:
        print("No valid Indian number plate detected.")
