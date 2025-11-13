from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_left(10)
tello.rotate_clockwise(90)
tello.move_forward(10)

tello.land()