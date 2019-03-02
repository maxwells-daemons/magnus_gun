/*
 * motor_control.ino
 * Arduino-side code for receiving commands and controlling motors
 */

#include <Servo.h>

#define PIN_LEFT  11
#define PIN_RIGHT 10

#define CALIBRATION_DELAY 3000
#define MOTOR_MAX_US 2000
#define MOTOR_MIN_US 700

Servo motor_left;
Servo motor_right;
bool doing_left = false;

void setup() {
    Serial.begin(9600);
    calibrate();
}

void loop() {
    if (Serial.available() > 0) {
        int nextSpeed = Serial.parseInt();

        if (doing_left) {
            Serial.print("Setting left speed: ");
            Serial.println(nextSpeed, DEC);

            motor_left.writeMicroseconds(nextSpeed);
        } else {
            Serial.print("Setting right speed: ");
            Serial.println(nextSpeed, DEC);

            motor_right.writeMicroseconds(nextSpeed);
        }

        doing_left = !doing_left;
    }

    delay(10);
}

void calibrate() {
    // Calibrate
    Serial.println("Attaching motor");
    motor_left.attach(PIN_LEFT);
    motor_right.attach(PIN_RIGHT);

    Serial.println("Forward calibration");
    motor_left.writeMicroseconds(MOTOR_MAX_US);
    motor_right.writeMicroseconds(MOTOR_MAX_US);
    delay(CALIBRATION_DELAY);

    Serial.println("Zero calibration");
    motor_left.writeMicroseconds(MOTOR_MIN_US);
    motor_right.writeMicroseconds(MOTOR_MIN_US);
    delay(CALIBRATION_DELAY);

    Serial.println("Spinning up and down");
    motor_left.writeMicroseconds(1000);
    motor_right.writeMicroseconds(1000);
    delay(500);
    motor_left.writeMicroseconds(790);
    motor_right.writeMicroseconds(790);

    Serial.println("Done with setup");
}
