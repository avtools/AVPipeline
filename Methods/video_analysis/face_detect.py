from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import mtcnn
import cv2
import tensorflow as tf
from tensorflow.python.framework import ops


class FaceExtract:
    # construct the argument parse and parse the arguments
    def argument_parser(self):
        args = argparse.ArgumentParser()
        args.add_argument("-v", "--video", required=True,
                          help="path to input video file")
        return args.parse_args()

    def read_frames(self):
        # start the file video stream thread and allow the buffer to
        # start to fill
        print("[INFO] starting video file thread...")
        args = vars(self.argument_parser())
        fvs = FileVideoStream(args["video"]).start()
        time.sleep(1.0)

        # start the FPS timer
        fps = FPS().start()
        detector = mtcnn.MTCNN()
        # loop over frames from the video file stream
        while fvs.more():
            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale (while still retaining 3
            # channels)
            frame = fvs.read()
            try:
                frame = imutils.resize(frame, width=450)
            except:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
            results = detector.detect_faces(frame)
            print(results)
            # display the size of the queue on the frame
            # cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
            #            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # show the frame and update the FPS counter
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        fvs.stop()


if __name__ == "__main__":
    face_extract = FaceExtract()
    face_extract.argument_parser()
    face_extract.read_frames()
