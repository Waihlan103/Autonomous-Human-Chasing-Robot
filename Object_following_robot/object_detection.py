import cv2
import time

classNames = []
classFile = "/home/waihlan/PycharmProjects/Opencv/Object_following_robot/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/waihlan/PycharmProjects/Opencv/Object_following_robot/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/waihlan/PycharmProjects/Opencv/Object_following_robot/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0:
        objects = classNames
    objectInfo =[]
    center_x = None
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo,

def main():
    #cap.set(3, 720)
    #cap.set(4, 640)
    # cap.set(10,70)
    cap = cv2.VideoCapture(0)
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()

        #Define frame rate
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Draw vertical middle line
        height, width, _ = frame.shape
        line_1 = (width // 2) - 30
        line_2 = (width // 2) + 30

        result, objectInfo = getObjects(frame, 0.45, 0.2)
        # print(objectInfo)
        # Display FPS on frame
        cv2.putText(frame, f'FPS: {fps:.2f}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2)

        cv2.line(result, (line_1, 0), (line_1, height), (255, 0, 0), 2)
        cv2.line(result, (line_2, 0), (line_2, height), (255, 0, 0), 2)

        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
