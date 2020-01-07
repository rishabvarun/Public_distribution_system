import serial

def give():
    arduino=serial.Serial("COM3",9600)
    a=str(arduino.readline())
    return(a[2:10])

def give1(id):
    arduino=serial.Serial("COM3",9600)
    str(arduino.readline())
    str(arduino.readline())
    for i in range(4):
        a=str(arduino.readline())
        print(a[2:-5])
    
    
    while True:
        a=str(arduino.readline())
        print(a[12:14])
        if a[12:14]==id:
            return(a)



def give3():
    arduino=serial.Serial("COM3",9600)
    print()
    a=(str(arduino.readline()))
    print(a[-43:-5])
        
    x=input()
    y=x.encode('raw_unicode_escape')
    arduino.write(y)
    if x=='1':
        for i in range(7):
            a=str(arduino.readline())
            print(a[2:-5])
        x=input()
        y=x.encode('raw_unicode_escape')
        arduino.write(y)
        a=str(arduino.readline())
        print(a[2:-5])
        while True:
            a=str(arduino.readline())
            print(a[12:14])
            if a[12:14]=='22':
                arduino.close()
                return(a)

    else:
        for i in range(3):
            a=str(arduino.readline())
            print(a[2:-5])
        x=input()
        y=x.encode('raw_unicode_escape')
        arduino.write(y)
        for i in range(1):
            a=str(arduino.readline())
            print(a[2:-5])
        a=str(arduino.readline())
        print(a[2:-5])
        arduino.close()
        return(a[2:-5])
        



    
    
    

