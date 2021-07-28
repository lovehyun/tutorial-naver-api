# author : shpark
# pip install opencv-python
import requests
import cv2


client_id = "KR2SGiYgWfN7l79DeNU8"
client_secret = open("secret.txt", "r").read()

url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
# url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식


def show_photo(image, data):
    if (data['info']['faceCount'] > 0):
        for face in data['faces']:
            x = face['roi']['x']
            y = face['roi']['y']
            width = face['roi']['width']
            height = face['roi']['height']
            print("\nx={}, y={}, width={}, height={}".format(x, y, width, height))

            x1 = x
            y1 = y
            x2 = x1 + width
            y2 = y1 + height

            text = face['gender']['value'] + " (" + str(face['gender']['confidence']) + ")"
            text2 = "age: " + face['age']['value'] + " (" + str(face['age']['confidence']) + ")"
            text3 = face['emotion']['value'] + " (" + str(face['emotion']['confidence']) + ")"

            # Color = BGR (255,255,255)  = white, (0,0,0) => black, (255,0,0)
            cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255), 2)
            cv2.putText(image, text, (x1-10,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(image, text2, (x1-10,y1+0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(image, text3, (x1-10,y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            
            cv2.imshow("MyFace", image)


def process_image(image):
    filename = 'capture.jpg'
    cv2.imwrite(filename, image)

    files = {'image': open(filename, 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }

    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code

    if (rescode==200):
        print(response.text)
        data = response.json()
        show_photo(image, data)
    else:
        print("Error Code:" + rescode)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: # ESC
            break
        elif key == ord('c'):
            process_image(frame)

    cap.release()
    cv2.destroyAllWindows()
