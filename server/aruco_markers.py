'''
Code for finding and using aruco markers.
'''

import cv2

# Initialize ArUco data
ARUCO_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()


def get_all_markers(image):
    '''
    Get all ArUco markers in an image in the format (corners, ids, rejected).

    Parameters
    ----------
    image : opencv bgr image
        The image.

    Returns
    -------
    3-tuple in the format (corners, ids, rejected) returned by detectMarkers
        All ArUco markers visible in the image.
    '''
    return cv2.aruco.detectMarkers(image, ARUCO_DICTIONARY,
                                   parameters=ARUCO_PARAMETERS)
