from server import hardware, aruco_markers, detect_person

import numpy as np
import cv2

# Parameters
# 0: laptop
# 2: usb webcam
camera_idx = 0
#  blob_detector = cv2.SimpleBlobDetector()


def main():
    '''
    Server main program.
    '''
    print('Connecting to hardware...')
    #  hardware.init()

    # Example from:
    # https://stackoverflow.com/questions/2601194/
    # displaying-a-webcam-feed-using-opencv-and-python/11449901#11449901
    print('Starting video feed and window...')
    camera = cv2.VideoCapture(camera_idx)
    if not camera.isOpened():
        raise RuntimeError('failed to open camera')
    camera_success, frame = camera.read()
    cv2.namedWindow('Video')

    while True:
        if not camera_success:
            raise RuntimeError('failed to get next frame')

        # Fetch frame
        camera_success, frame = camera.read()
        preview = np.copy(frame)

        # Find and draw aruco markers
        marker_corners, marker_ids, _ = aruco_markers.get_all_markers(frame)
        cv2.aruco.drawDetectedMarkers(preview, marker_corners, marker_ids)

        # Find and draw person bounding boxes
        #  (boxes, weights) = detect_person.detect_people(frame)
        #  for (x, y, w, h) in boxes:
        #      cv2.rectangle(preview, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Filter for balls
        #  low_color = np.array([70, 90, 180])
        #  high_color = np.array([200, 255, 255])
        #  filtered = cv2.inRange(frame, low_color, high_color)
        #  overlay = np.zeros_like(frame)
        #  overlay[:, :, 2] = filtered
        #  preview = (preview * 1.0 / 255) + (overlay * 0.7 / 255)

        # Display frame
        cv2.imshow('Video', preview)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            print('ESC pressed: exiting')
            break


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Exiting with error: {}'.format(e))

    hardware.cleanup()
