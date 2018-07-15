#############################
##  Evan Firoozi - July 2017
##  Cozmo by Anki - Find charger
#############################

#############################
## Find faces, find cubes, scan the surrounding
## find the charger, locate it based on other objects
#############################

import cozmo
import time
from cozmo.util import degrees, distance_mm, speed_mmps
import asyncio

def follow_faces(robot: cozmo.robot.Robot):
    '''The core of the follow_faces program'''

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    face_to_follow = None

    print("Exit with CTRL+C")
    while True:
        turn_action = None
        if face_to_follow:
            # start turning towards the face
            turn_action = robot.turn_towards_face(face_to_follow)
            cozmo.faces.FACIAL_EXPRESSION_HAPPY = 'happy'
        if not (face_to_follow and face_to_follow.is_visible):
            # find a visible face, timeout if nothing found after a short while
            try:
                face_to_follow = robot.world.wait_for_observed_face(timeout=30)
                cozmo.faces.FACIAL_EXPRESSION_HAPPY = 'happy'
            except asyncio.TimeoutError:
                print("Didn't find a face - exiting!")
                return

        if turn_action:
            # Complete the turn action if one was in progress
            turn_action.wait_for_completed()

        time.sleep(.1)


cozmo.run_program(follow_faces, use_viewer=True, force_viewer_on_top=True)
