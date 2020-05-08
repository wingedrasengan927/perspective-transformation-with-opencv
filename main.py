import cv2
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Application to crop an image and get it's perspective transformation")
    parser.add_argument("--image", default="images/Road_in_Norway.jpg", type=str, help="path of Input Image")
    args = parser.parse_args()
    return args

def four_point_transform(image, points):
    (tl, tr, br, bl) = points

    # compute width
    # it will be maximum of bottom width and top width
    bottom_width = np.sqrt(np.square(br[0] - bl[0]) + np.square(br[1] - bl[1]))
    top_width = np.sqrt(np.square(tr[0] - tl[0]) + np.square(tr[1] - tl[1]))
    max_width = max(int(top_width), int(bottom_width))

    # compute height
    # it will be maximum of left height and right height
    left_height = np.sqrt(np.square(tl[0] - bl[0]) + np.square(tl[1] - bl[1]))
    right_height = np.sqrt(np.square(tr[0] - br[0]) + np.square(tr[1] - br[1]))
    max_height = max(int(left_height), int(right_height))

    # construct destination points (boundary coordinates of our new image)
    dst = np.array([[0, 0], [max_width - 1, 0], [max_width-1, max_height - 1], [0, max_height-1]], dtype="float32")

    # compute perspective transform and then apply it
    M = cv2.getPerspectiveTransform(points, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    return warped


def main():

    args = parse_args()
    # read the image
    img = cv2.imread(args.image)
    # copy the image
    img_copy = img.copy()
    points = []

    def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 5, (255, 255, 0), -1)
            # points should be in the order top left, top right, bottom right, bottom left
            points.append((x, y))

    # name the window
    cv2.namedWindow(winname='my window') 

    # set callback
    cv2.setMouseCallback('my window', draw_circle)

    # show the image
    while len(points) < 4:
        cv2.imshow('my window', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # exit the window
    cv2.destroyAllWindows()

    pts = np.array(points, dtype="float32")
    warped_image = four_point_transform(img_copy, pts)

    # save the warped image
    cv2.imwrite("output/" + args.image.split("/")[-1].split(".")[0] + "_warped.jpg", warped_image)

    # show the warped image
    cv2.imshow("Warped Image", warped_image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()    