#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

//this article explains orientation of accel gyro and mag
//https://www.lythaniel.fr/index.php/2016/08/20/lsm9ds1-madgwicks-ahr-filter-and-robot-orientation/

Madgwick filter;
const float sensorRate = 119.00;

unsigned long micros_per_reading, micros_previous;

float accelX=1.0;
float accelY=1.0;
float accelZ=1.0;
float gyroX=1.0;
float gyroY=1.0;
float gyroZ=1.0;
float magX=1.0;
float magY=1.0;
float magZ=1.0;
float x, y, z;
float gx, gy, gz;
float mx, my, mz;

BLEService IMUService("1101");
BLEFloatCharacteristic AccZChar("2101", BLERead | BLENotify);

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);  
  pinMode(LED_BUILTIN, OUTPUT);

  if(!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    while(1);
  }
  
  if (!BLE.begin()) {
    Serial.println("BLE failed to initialize");
    delay(500);
    while(1);
  }
  BLE.setLocalName("Arduino Accelerometer");
  BLE.setAdvertisedService(IMUService);
  IMUService.addCharacteristic(AccZChar);
  BLE.addService(IMUService);
  AccZChar.writeValue(accelZ);
  BLE.advertise();
  Serial.println("BLE device now active, waiting for connections... ");

  filter.begin(sensorRate);

  delay(1000);
  Serial.println("Beginning");

  micros_per_reading = 1000000 / 119;
  micros_previous = micros();
}

void loop() {
  
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
    while(central.connected()) {
      unsigned long micros_now;
      micros_now = micros();

      if (micros_now - micros_previous >= micros_per_reading) {
        read_Accel();
        read_gyro();
        read_mag();
        float roll, pitch, heading;
        filter.update(gyroY, gyroX, gyroZ, accelY, accelX, accelZ, magY, -magX, magZ);
        roll = filter.getRoll();
        float roll_rads = roll * PI / 180.0;
        float total_accel = accelX * sin(roll_rads) + accelZ * cos(roll_rads);
        AccZChar.writeValue(total_accel - 1);
        //pitch = filter.getPitch();
        //heading = filter.getYaw();
//        Serial.println("");
//        Serial.print(total_accel);
//        Serial.println("");
//        Serial.print(roll);
//        Serial.print('\t');
//        Serial.print(pitch);
//        Serial.print('\t');
//        Serial.print(heading);
//        Serial.println("");
//        Serial.print(accelX);
//        Serial.print('\t');
//        Serial.print(accelY);
//        Serial.print('\t');
//        Serial.print(accelZ);
//        Serial.print('\t');
//        Serial.print('\t');
//        Serial.print(gyroX);
//        Serial.print('\t');
//        Serial.print(gyroY);
//        Serial.print('\t');
//        Serial.print(gyroZ);
//        Serial.print('\t');
//        Serial.print('\t');
//        Serial.print(magX);
//        Serial.print('\t');
//        Serial.print(magY);
//        Serial.print('\t');
//        Serial.print(magZ);
        micros_previous = micros_previous + micros_per_reading;
      }
      

      

//      AccZChar.writeValue(accelZ);
      
//      Serial.println("");
//      Serial.print(accelX);
//      Serial.print('\t');
//      Serial.print(accelY);
//      Serial.print('\t');
//      Serial.print(accelZ);
//      Serial.print('\t');
//      Serial.print('\t');
//      Serial.print(gyroX);
//      Serial.print('\t');
//      Serial.print(gyroY);
//      Serial.print('\t');
//      Serial.print(gyroZ);
//      Serial.println("");
//      Serial.print(roll);
//      Serial.print('\t');
//      Serial.print(pitch);
//      Serial.print('\t');
//      Serial.print(heading);
    }
  }

  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from central: ");
  Serial.println(central.address());
  
  
}

void read_Accel() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    accelX = x;
    accelY = y;
    accelZ = z;
  }
}

void read_gyro() {
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);
    gyroX = gx;
    gyroY = gy;
    gyroZ = gz;
  }
}

void read_mag() {
  IMU.readMagneticField(mx, my, mz);
  magX = mx;
  magY = my;
  magZ = mz;
}
