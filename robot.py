# TODO: insert robot code here
import wpilib
import wpilib.drive
import wpimath.filter
import math


from drivetrain import Drivetrain

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.controller = wpilib.XboxController(0)
        self.drive = Drivetrain()
        
        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.speedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

    # every fraciton of a second, check everything
    def autonomousPeriodic(self):
        self.teleopPeriodic()
        self.drive.updateOdometry()

    # example stuffs
    # def stuffs():
        
    # while human is driving
    def teleopPeriodic(self):
        myRight = -self.controller.getRightTriggerAxis()
        myLeft = -self.controller.getLeftTriggerAxis()
        mySpeed = myRight - myLeft
        myTurn = self.controller.getRightX()
        deadzone = 0.15
        #if (myRight<0.1):
         #   myRight = 0
        #if (myLeft<0.1):
         #   myLeft = 0
        if (mySpeed > - deadzone) and (mySpeed < deadzone):
            mySpeed = 0
        mySpeed = math.pow(abs(mySpeed),2) * mySpeed
        if (myTurn > - deadzone) and (myTurn < deadzone):
            myTurn = 0
        myTurn = math.pow(abs(myTurn),3) * myTurn
        
    
        

        

        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        xSpeed = (
            -self.speedLimiter.calculate(mySpeed)
            * Drivetrain.MAX_SPEED
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rotLimiter.calculate(myTurn)
            * Drivetrain.MAX_ANGULAR_SPEED
        )

        self.drive.drive(xSpeed, rot)