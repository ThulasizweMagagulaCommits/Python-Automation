"""
Writing instractions and sending them over serial communication to printer - Junior Python Developer Portfolio
Author: Thulasizwe Magagula
Purpose: Automation - Writing instractions and sending them over serial communication to printer
Demonstrates working with serial module, automating communication  printing on thermal printers and other micro control devices
"""
import serial
ser = serial.Serial("/dev/ttyUSB0", 19200, timeout=10)

ESC = b'\0x1b 0x3D 0x01'
LF = b'x0a'

def left(): return ESC + b'a' + b'\x00'
def center(): return ESC + b'a' + b'\x01'
def right(): return ESC + b'a' + b'\x02'
def normal(): return ESC + b'!' + b'\x00'
def big(): return ESC + b'!' + b'\x38'

#Generate the barcode
def barcode(data):
    return ESC + b'k' + b'x05' + data.encode() + LF

#Rotate the Validation number
def rotate_cid(text):
    return ESC + b'V' + b'\x01' + text.encode() + LF

#reset the printer
ser.write(ESC + b'@' + LF)

#Venue
ser.write(center())
ser.write(normal())
ser.write(b'Galaxy River Square' + LF)
ser.write(b'cc ID: 000012' + LF + LF)

#Ticket type
ser.write(big())
ser.write(b'CASHOUT TICKET' + LF)
ser.write(normal() + LF)

#Barcode
validation = "00-0999-6525-7058-2421"
ser.write(center())
ser.write(barcode(validation))
ser.write(LF)

#Validation Text
ser.write(center())
ser.write(b'VALIDATION' + LF)
ser.write(validation.encode() + LF)
ser.write(b'FORTY NINE RANDS AND SEVENTY FIVE CENTS' + LF + LF)

#Amount (large)
ser.write(big())
ser.write(b'R49.75' + LF)
ser.write(normal() + LF)

#Footer Data
ser.write(left())
ser.write(b'Ticket #0770' + LF)
ser.write(b'ASSET #30704                            Void After 30 Days' + LF + LF)

ser.write(b'Date         Time' + LF + LF)

ser.write(LF*2) #Move text two Line Feeds down
ser.write(right())
ser.write(rotate_cid(validation))

#Cut Ticket
ser.write(ESC + b'i')

ser.close()
