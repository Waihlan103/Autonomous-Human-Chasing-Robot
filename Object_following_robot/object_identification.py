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

cv_scaler = 1

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0:
        objects = classNames

    center_x = None
    center_y = None
    max_area = 0
    largest_object = None

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                area = box[2] * box[3]
                if area > max_area:
                    max_area = area
                    largest_object = (box, className, confidence)

        if largest_object:
            box, className, confidence = largest_object
            if (draw):
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                cv2.putText(img, className.upper(), (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                # Draw center point
                center_x = box[0] + box[2] // 2
                center_y = box[1] + box[3] // 2
                cv2.circle(img, (center_x, center_y), 5, (0, 0, 255), cv2.FILLED)
            return img, [[box, className]], center_x, center_y, max_area
    return img, [], center_x, center_y, max_area

def main():
    # cap.set(10,70)
    cap = cv2.VideoCapture(0)
    #cap.set(3, 480)
    #cap.set(4, 360)
    prev_time = time.time()
    print("frame width : ", cap.get(3))
    print("frame height : ", cap.get(4))

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
        line_1 = (width // 2) - 50
        line_2 = (width // 2) + 50

        # Resize the frame using cv_scaler to increase performance (less pixels processed, less time spent)
        resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))

        frame, objectInfo, cx, cy, max_area = getObjects(resized_frame, 0.5, 0.2, objects=['person'])
        print(objectInfo)
        # Display FPS on frame
        cv2.rectangle(frame, (0,0), (width, 30), (0,0,0), thickness=-1)
        cv2.putText(frame, f'(x,y): ({cx},{cy})', (375, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 255), 2)
        cv2.putText(frame, f'FPS: {fps:.2f}', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 255), 2)
        cv2.line(frame, (line_1, 0), (line_1, height), (255, 0, 0), 2)
        cv2.line(frame, (line_2, 0), (line_2, height), (255, 0, 0), 2)

        #finding area
        closed_area = 260000
        print("area of object : ", max_area)

        if cx is not None:
           if line_1 < cx < line_2:
               if max_area > closed_area:
                   cv2.putText(frame, 'RPM: {15}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                   cv2.putText(frame, 'Backward', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
               elif 240000 < max_area < 260000:
                   cv2.putText(frame, 'RPM: {0}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                   cv2.putText(frame, 'Stop', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
               else:
                   cv2.putText(frame, 'RPM: {15}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                   cv2.putText(frame, 'Forward', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

           elif cx < line_1:
               cv2.putText(frame, 'RPM: {10}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
               cv2.putText(frame, 'Left', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

           elif cx > line_2:
              cv2.putText(frame, 'RPM: {10}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
              cv2.putText(frame, 'Right', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        else:
            cv2.putText(frame, 'RPM: {0}', (150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(frame, 'Stop', (545, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
