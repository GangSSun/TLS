import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

def On_OLED(hours, minutes,dis):
    if minutes < 0:
        minutes = 0
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "Touch Less Switch", font=font, fill=255)
    draw.text((0, 16), "After " + str(int(hours)) + "h " + str(int(minutes)) + "m", font=font, fill=255)
    draw.text((0, 32), "The Right Up!" , font=font, fill=255)
    draw.text((0, 48), "Now Distance : " + str(dis) + "cm", font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(5)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()

def DIS_VIEW(before, after):
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "Touch Less Switch", font=font, fill=255)
    draw.text((0, 16), "Distance Changed!", font=font, fill=255)
    draw.text((0, 32), str(before) + "cm  ->  " + str(after) + "cm", font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(5)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()
    
def ADD_TIME(num, ltime):
    time_str = " "
    hours = int(ltime / 3600)
    minutes = int((ltime % 3600) / 60)
    alarm_str = str(hours) + "H " + str(minutes) + "M"
    if num > 3599: # 1시간 추가한경우
        time_str = "1 Hour!"
    else:
        time_str = "10 Minutes!" 
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)


    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "Touch Less Switch", font=font, fill=255)
    draw.text((0, 16), "Add " + time_str, font=font, fill=255)
    draw.text((0, 32), "After " + alarm_str, font=font, fill=255)
    draw.text((0, 48), "The Right Up!" , font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(3)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()

def RESET_ALARM(ltime):
    if ltime < 0:
        hours=0
        minutes=0
    else:
        hours = int(ltime / 3600)
        minutes = int((ltime % 3600) / 60)
        
    alarm_str = str(hours) + "H" + str(minutes) + "M"
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)


    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "The time is Reset!", font=font, fill=255)
    draw.text((0, 16), "Alarm was " + alarm_str , font=font, fill=255)
    draw.text((0, 32), "Now Alarm is 0!" , font=font, fill=255)


    # Display image
    oled.image(image)
    oled.show()
    time.sleep(3)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()


def CHANGE_POWER(before_power, after_power):
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)
    #font = ImageFont.load_default()


    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "Motor Power Changed!", font=font, fill=255)
    draw.text((0, 16), str(before_power) + " -> " + str(after_power) , font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(3)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()
    
def WARNING_POWER(now_power):
    if now_power == 10:
        mes = "Now Power is 10!"
    else:
        mes = "Now Power is 1!"
    
    print("OLED ON!")
    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Display Parameters
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    font = ImageFont.truetype('PixelOperator.ttf', 16)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Pi Stats Display
    draw.text((0, 0), "     Warning!", font=font, fill=255)
    draw.text((0, 32), mes , font=font, fill=255)
    draw.text((0, 48), "Can't change power!" , font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(3)# 10초동안 OLED 보여주다가 종료

    print("OLED OFF")
    oled.fill(0)
    oled.show()
    
