import RPi.GPIO as GPIO
import time
import pigpio # Jittering(모터 떨림) 해결을 위해 서보 모터에는 pigpiod 모듈 사용
import OLED

# 실제 동작 코드

GPIO.setwarnings(False) ; GPIO.setmode(GPIO.BCM)

def set_angle(tmp,on_angle,off_angle):
    angle = 0 # 모터의 동작 각도
    if(tmp == True):
        a = on_angle
    else:
        a = off_angle
    return 600 + (10 * a)

def move_motor(now_status, on_angle, off_angle):
    pi.set_servo_pulsewidth(18, set_angle(now_status, on_angle, off_angle)) # 서보 모터 동작
    time.sleep(0.5)
    pi.set_servo_pulsewidth(18, 1500) # 모터의 각도를 90도로 초기화
    time.sleep(1)
    return not now_status

trig = 23 ; echo = 24 #센서에 연결한 Trig와 Echo 핀의 핀 번호 설정
reset_button_pin = 26 # 거리 초기화 버튼의 핀번호 선정
motor_button_pin = 13 # 모터 동작 버튼 핀번호 설정
led_pin = 19 # 센서가 감지됐을때 켜지는led의 핀번호
location_led_pin = 12 # 초음파 센서 위치를 알려주는 led의 핀번호
SERVO_PIN = 18 # 서보모터를 PWM으로 제어할 핀 번호 설정
hour_button_pin = 6 # 1시간 추가 버튼 핀번호
minute_button_pin = 5 # 10분 추가 버튼 핀번호
oled_button_pin = 11 # 잔여 알람을 표시해주는 버튼
plus_angle_button_pin = 21 ; minus_angle_button_pin = 20 # 각도 조절 핀 번호 설정
time_reset_button_pin = 16 # 알람 초기화 버튼 핀 번호 설정

on_angle = 152 ; off_angle = 40 # 모터가 동작했을때의 각도
cnt=0
now_status = True # 현재 모터의 상태 True = On, False = Off
basic_dis=0 #기본세팅 거리값
pi = pigpio.pi() #먼저 사용할 pigpio.pi를 매칭

motor_power = 5 # 모터의 파워 기본이 5단계
least_time = -1 # 모터 동작까지 남은 시간

print ("start")

GPIO.setup(reset_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motor_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(hour_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(minute_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(oled_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(plus_angle_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(minus_angle_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(time_reset_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(trig, GPIO.OUT) ; GPIO.setup(echo, GPIO.IN) #Trig와 Echo 핀의 출력/입력 설정
GPIO.output(trig, False) #Trig핀의 신호를 0으로 출력
GPIO.setup(led_pin, GPIO.OUT) # ledpin Out으로 설정
GPIO.setup(location_led_pin, GPIO.OUT) 

print("Waiting for sensor to settle")

GPIO.output(location_led_pin, 1) # 어둠속에서도 초음파 센서의 위치를 알 수 있도록 항상 led가 켜져있도록 함


try :
    while True :
        if least_time > 0: # least time이 0보다 큰경우 즉, 알람이 맞춰져있는 경우 알람시간 까지 대기
            least_time -= 1
            if(least_time == 0):
                print("Alarm On!")
                least_time = 0
                now_status=move_motor(now_status, on_angle, off_angle) # 모터 동작
            
            
        GPIO.output(trig, True) # Triger 핀에 펄스신호를 만들기 위해 1 출력
        time.sleep(0.00001) # 10µs 딜레이
        GPIO.output(trig, False)
        
        while GPIO.input(echo) == 0 :
            pulse_start = time.time() # Echo 핀 상승 시간 (펄스가 출력되는 시점)
        while GPIO.input(echo) == 1 :
            pulse_end = time.time() # Echo 핀 하강 시간 (반사되어 돌아온 시점)
        pulse_duration = pulse_end - pulse_start # 거리 측정을 위한 식
        distance = pulse_duration * 34300/2
        distance = round(distance, 2)
        
        if GPIO.input(reset_button_pin)==GPIO.HIGH: # 리셋 버튼이 눌렸을때의 거리로 초기화
            OLED.DIS_VIEW(basic_dis, distance)
            print("Reset Distance! Before : ", basic_dis,"Now : ",distance)
            basic_dis = distance
            
        elif GPIO.input(plus_angle_button_pin)==GPIO.HIGH: # 모터가 더 큰 각도로 돌게함 = 파워 단계 상승
            if motor_power < 10: # 모터의 파워단계 10을 초과하지 않도록 즉 서보모터의 최대각을 초과하지 않을때 파워 상승
                print("Power Up!")
                on_angle += 5
                off_angle -= 5
                motor_power += 1
                OLED.CHANGE_POWER((motor_power - 1), motor_power)
            else:
                OLED.WARNING_POWER(motor_power)
                
            
        elif GPIO.input(minus_angle_button_pin)==GPIO.HIGH: # 모터가 더 작은 각도로 돌게함
            if motor_power > 1: # 모터의 파워단계 1 아래로 내려가지 않도록,즉 너무 작은 각도로 돌지않게 제한
                print("Power Down!")
                on_angle -= 5
                off_angle += 5
                motor_power -= 1
                OLED.CHANGE_POWER((motor_power + 1), motor_power)
            else:
                OLED.WARNING_POWER(motor_power)
            
        elif GPIO.input(hour_button_pin)==GPIO.HIGH: # a만큼 알람 시간 추가
            a = 3601 # 1시간
            if least_time<0: # 남은 시간이 초기화 상태인 경우
                least_time = 0 # 0으로 다시 초기화
            least_time+=a
            OLED.ADD_TIME(a, least_time)
        
        elif GPIO.input(minute_button_pin)==GPIO.HIGH: # b만큼 알람 시간 추가
            b = 600 # 10분
            if least_time<0: # 남은 시간이 초기화 상태인 경우
                least_time = 0 # 0으로 다시 초기화
            least_time+=b
            OLED.ADD_TIME(b, least_time)
        
        elif GPIO.input(oled_button_pin)==GPIO.HIGH:
            OLED.On_OLED((least_time / 3600),((least_time % 3600) / 60),basic_dis) # OLED에 알람 잔여 시간 출력 및 기준 거리 표기
            
        elif GPIO.input(motor_button_pin)==GPIO.HIGH: # 모터 동작
            print("Motor On!")
            now_status=move_motor(now_status, on_angle, off_angle)

        elif GPIO.input(time_reset_button_pin)==GPIO.HIGH: # 알림 시간 초기화
            print("Alarm Time Reset!")
            OLED.RESET_ALARM(least_time)
            least_time = 0
            
            
        if distance < (basic_dis-5): #기준 거리보다 5cm이상 줄어들었을때 출력
            print("distance is changed!")
            GPIO.output(led_pin, 1)
            cnt+=1
        else: # 다시 기준 거리가 측정됐을때 LED와 cnt변수 초기화
            GPIO.output(led_pin, 0)
            cnt=0
            
        if cnt>5: # 모터 동작 -> 불이 켜지거나 꺼지게
            print("Motor On!")
            now_status=move_motor(now_status, on_angle, off_angle)
            cnt=0 # 입력횟수 초기화
            
        time.sleep(1) # 1초 간격으로 센서 측정
        
except KeyboardInterrrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
