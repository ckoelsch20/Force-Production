# Force Production
Device to track force production during barbell movements.

This device is comprised of an Arduino Nano and an MPU6050 breakout board. This is used to track acceleration of a barbell during weightlifting movements, which allows for a rough estimate of force production to be calculated. Athletes can track progress over time and compare past lifts. This can help athletes gain an understand of their stong points, weak points, and how quickly they are progressing. 

The script running on the Arduino is taken from Jeff Rowberg's MPU6050 library. Python is used to receive and handle the data. 

Future improvements include using Bluetooth to transmit data wirelessly and a web app to collect, view, and compare the data so that the device is easy to use.

Device housing was designed in Fusion 360 and printed on an Ender 3 3D printer. 