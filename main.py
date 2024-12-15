import cv2
import threading
import queue
import time
import uuid

rtsp_server_list = ["rtsp://ydbx:ec4aau@192.168.1.10:554/user=ydbx&password=ec4aau&channel=1&stream=0.sdp",
                    "rtsp://jsjt:7hfahc@192.168.1.28:554/user=jsjt&password=7hfahc&channel=1&stream=0.sdp",
                    "rtsp://xanh:ah57c8@192.168.1.15:554/user=xanh&password=ah57c8&channel=1&stream=0.sdp",
                    "rtsp://tcey:cy6kfn@192.168.1.14:554/user=tcey&password=cy6kfn&channel=1&stream=0.sdp"]

class Camera:
    instances = []
    def __init__(self, rtsp_server : str):
        self.frame_queue = queue.Queue()
        self.width = 800
        self.height = 600
        self.rtsp_server = rtsp_server
        self.id = uuid.uuid1().__str__()
        self.__class__.instances.append(self)

def loadImage(camera : Camera):
    video_capture = cv2.VideoCapture(camera.rtsp_server)
    if(video_capture.isOpened()):
        while True:
            try:
                _, frame = video_capture.read()
                frame = cv2.resize(frame, (camera.width, camera.height))
                if(_):
                    camera.frame_queue.put(frame)
                time.sleep(0.1)
            except:
                print("Error Video:" + camera.id)
                break
    else:
        print("Failed to load RTSP SERVER: " + camera.rtsp_server)

def display():
    while True:
        for camera in Camera.instances:
            if not camera.frame_queue.empty():
                frame = camera.frame_queue.get()
                cv2.namedWindow(camera.id, flags=cv2.WINDOW_FULLSCREEN)
                cv2.setWindowProperty(camera.id, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(camera.id, frame)
            cv2.waitKey(1)

def init():
    try:
        image_loaders : list[threading.Thread] = []

        for rtsp_server in rtsp_server_list:
            image_loaders.append(threading.Thread(target=loadImage, args=(Camera(rtsp_server),)))
        display_thread = threading.Thread(target=display)

        for image_loader in image_loaders:
            image_loader.start()
        display_thread.start()

        for image_loader in image_loaders:
            image_loader.join()
        display_thread.join()

    except KeyboardInterrupt:
        exit()

    except Exception as ex:
        print("An error occurred! Details: \n" + ex.__cause__())
        exit()

init()