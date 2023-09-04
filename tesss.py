import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from RPLCD import i2c
from time import sleep

EMULATE_HX711 = False

referenceUnit = 1

if not EMULATE_HX711:
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

# Inisialisasi HX711
hx711 = HX711(5, 6)
hx711.set_reading_format("MSB", "MSB")
hx711.set_reference_unit(1)
hx711.reset()
hx711.tare()

# Inisialisasi driver LCD
lcd = i2c.CharLCD('PCF8574', 0x27)

# Konfigurasi pin GPIO untuk servo
servo_pin = 18  # Ganti dengan nomor pin GPIO yang sesuai
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Inisialisasi PWM (Pulse Width Modulation) untuk servo
pwm = GPIO.PWM(servo_pin, 50)  # Frekuensi PWM 50 Hz (umum untuk servo)
pwm.start(0)  # Awalnya servo berada di posisi awal (sudut 0 derajat)

def set_servo_angle(angle):
    duty_cycle = (angle / 18) + 2  # Menghitung duty cycle berdasarkan sudut (dalam derajat)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)  # Beri waktu servo untuk bergerak

try:
    while True:
        val = max(0, int(hx711.get_weight(5)))
        lcd.write_string("Berat: {} gram".format(val))
        sleep(2) # Tampilkan selam  # Hapus tampilan pada LCD
        
        lcd.clear()
        sleep(0.1)  # Jeda selama 1 detika 2 detik
        print(val)

        if val > 5:
            set_servo_angle(88)  # Jika berat di atas 5 gram, putar servo ke posisi tertentu
        else:
            set_servo_angle(-3)  # Jika berat di bawah atau sama dengan 5 gram, kembalikan servo ke posisi awal

        hx711.power_down()
        hx711.power_up()
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()


