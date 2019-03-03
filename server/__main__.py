from server import hardware, aruco_markers, detect_person

import time
import numpy as np
import cv2

# Parameters
# 0: laptop
# 2: usb webcam
camera_idx = 2
hysteresis_frames = 20

def main():
    '''
    Server main program.
    '''
    print('Connecting to hardware...')
    hardware.init()

    # Example from:
    # https://stackoverflow.com/questions/2601194/
    # displaying-a-webcam-feed-using-opencv-and-python/11449901#11449901
    print('Starting video feed and window...')
    camera = cv2.VideoCapture(camera_idx)
    if not camera.isOpened():
        raise RuntimeError('failed to open camera')
    camera_success, frame = camera.read()
    cv2.namedWindow('Video')

    # Zero motors
    time.sleep(1)
    hardware.set_speeds(700, 700)
    frames_since_marker = hysteresis_frames + 1

    while True:
        if not camera_success:
            raise RuntimeError('failed to get next frame')

        # Fetch frame
        camera_success, frame = camera.read()
        preview = np.copy(frame)

        # Find and draw aruco markers
        marker_corners, marker_ids, _ = aruco_markers.get_all_markers(frame)
        cv2.aruco.drawDetectedMarkers(preview, marker_corners, marker_ids)

        # Compute zone
        if marker_corners:
            marker = marker_corners[0][0]
            marker_x = np.mean(marker[:, 0])
            print('Marker_x:', marker_x)
            frames_since_marker = 0
        else:
            frames_since_marker += 1

        if frames_since_marker < hysteresis_frames:
            if marker_x < 220:  # Far left
                hardware.set_speeds(700, 2000)
                zone_name = 'far left'
            elif marker_x > 325:  # Far right
                hardware.set_speeds(2000, 800)
                zone_name = 'far right'
            else:  # Center
                hardware.set_speeds(2000, 2000)
                zone_name = 'center'
            cv2.putText(preview, 'Marker at: {}'.format(zone_name), (30, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            hardware.set_speeds(700, 700)
            cv2.putText(preview, 'No marker visible', (30, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

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
