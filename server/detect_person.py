'''
Code for the person detection model.
See: https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
'''

import cv2

detector = cv2.HOGDescriptor()
detector.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())


def detect_people(image, do_nonmax_suppression=True):
    '''
    Get all human bounding boxes in an image.

    Parameters
    ----------
    image : opencv bgr image
        The image.
    do_nonmax_suppression : bool
        Whether or not to apply nonmaximum suppression.
    '''
    # TODO: nms
    return detector.detectMultiScale(image,
                                     scale=1.05)
