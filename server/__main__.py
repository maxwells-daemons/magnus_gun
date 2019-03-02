from server import hardware

import cv2


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
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('failed to open camera')
    camera_success, frame = camera.read()
    cv2.namedWindow('Video')

    while True:
        if not camera_success:
            raise RuntimeError('failed to get next frame')

        camera_success, frame = camera.read()
        cv2.imshow('Video', frame)

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
