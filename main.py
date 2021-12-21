class main(Exception):
    def __init__(self):
        from threading import Thread
        self.pose = None
        self.poseatt = {}
        self.framecount = 0
        Thread(target=self.run).start()
        self.get()

    def run(self):
        import cv2
        import mediapipe as mp
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture("out.mp4")
        #resize cap
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                self.framecount += 1
                #if self.framecount < 1000:
                #    if self.framecount % 100 == 0:
                #        #Skip the frame
                #        cap.grab()
                #        print("Passed {frame}".format(frame=self.framecount))
                #    continue
                success, image = cap.read()
                #resize image
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
                image = cv2.resize(image, (1600, 900))
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    self.results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('w', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
        # Destroy all windows
        cv2.destroyAllWindows()
    
    def get(self):
        while True:
            r = input()
            if r == "exit":
                f = open("pose.json", "w")
                from json import dumps
                f.write(dumps(self.poseatt))
                f.close()
                print("Exiting")
                return
            sec = 0
            try:
                keypoints = []
                for data_point in self.results.pose_landmarks.landmark: keypoints.append({'X': data_point.x, 'Y': data_point.y, 'Z': data_point.z, 'Visibility': data_point.visibility,})
            except:
                print("Error on frame {frame}".format(frame=self.framecount))
                pass
            
            sec = self.framecount / 25

            self.poseatt.update({str(sec): keypoints})
            print("OK {sec}".format(sec=sec))



if __name__ == "__main__":
    main()