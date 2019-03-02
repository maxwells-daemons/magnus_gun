/*
 * motor_control.ino
 * Arduino-side code for receiving commands and controlling motors
 */

#include <Servo.h>

#define PIN_LEFT  9
#define PIN_RIGHT 10

#define CALIBRATION_DELAY 3000
#define MOTOR_MAX_US 2000
#define MOTOR_MIN_US 700

Servo motorLeft;
Servo motorRight;

void setup() {
    Serial.begin(9600);

    Serial.println("Attaching motors");
    motorLeft.attach(PIN_LEFT);
    motorRight.attach(PIN_RIGHT);

    /* calibrate(); */
}

void loop() {
    if (Serial.available() >= 2 * sizeof(int)) {
        int speedLeft = Serial.parseInt();
        int speedRight = Serial.parseInt();

        if (speedLeft <= 0 || speedRight <= 0) { // Detect timeout
            return;
        }

        motorLeft.writeMicroseconds(speedLeft);
        motorRight.writeMicroseconds(speedRight);

        Serial.print("Set speeds: ");
        Serial.print(speedLeft, DEC);
        Serial.print(", ");
        Serial.print(speedRight, DEC);
        Serial.println("");
    }

    delay(10);
}

void calibrate() {
    // Calibrate
    Serial.println("Forward calibration");
    motorLeft.writeMicroseconds(MOTOR_MAX_US);
    motorRight.writeMicroseconds(MOTOR_MAX_US);
    delay(CALIBRATION_DELAY);

    Serial.println("Zero calibration");
    motorLeft.writeMicroseconds(MOTOR_MIN_US);
    motorRight.writeMicroseconds(MOTOR_MIN_US);
    delay(CALIBRATION_DELAY);

    Serial.println("Spinning up and down");
    motorLeft.writeMicroseconds(1000);
    motorRight.writeMicroseconds(1000);
    delay(500);
    motorLeft.writeMicroseconds(790);
    motorRight.writeMicroseconds(790);

    Serial.println("Done with setup");
}
