import os
import cv2
import pickle
import face_recognition

folderPath = "FR_webapp_main\FR_IMAGE"
enc_file_location ="FR_webapp_main"
valid_ext = (".jpg", ".jpeg", ".png")

pathList = [f for f in os.listdir(folderPath) if f.lower().endswith(valid_ext)]
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is None:
        print(f"Could not read {path}, skipping...")
        continue
    imgList.append(img)
    id = os.path.splitext(path)[0]
    studentIds.append(id)

print("Student IDs:", studentIds)

def findEncodings(imagesList, ids):
    encodeList = []
    for img, sid in zip(imagesList, ids):
        if img is None:
            print(f"Skipping {sid} - could not read image")
            continue
        
        # Ensure 8-bit unsigned integers
        if img.dtype != 'uint8':
            print(f"Converting {sid} to uint8 format")
            img = cv2.convertScaleAbs(img)

        # Remove alpha channel if present
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img_rgb)

        if encodes:
            encodeList.append(encodes[0])
        else:
            print(f"No face found for {sid}, skipping...")
    return encodeList

print("Encoding Started >>>")
encodeListKnown = findEncodings(imgList, studentIds)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")



with open(os.path.join(enc_file_location, "EncodeFile.p"), 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print('File Saved >>>')

