import serial, time, logging

class SerialCounterReader():

    def __init__(self, config):
        self.port = config['serialport']
        self.baudrate = config['baudrate']
        self.bytesize = config['bytesize']
        self.parity = config['parity']
        self.stopbits = config['stopbits']
        self.timeout = config['timeout']
        self.serial = None


    def create_serial(self):
        ser = serial.Serial()
        ser.port = self.port
        ser.baudrate = self.baudrate
        ser.bytesize = self.bytesize
        ser.parity = self.parity
        ser.stopbits = self.stopbits
        ser.timeout = self.timeout
        return ser


    def write_to_serial(self, ser, payload):
        time.sleep(.1)
        #n = ser.write(b'/?!\r\n')
        n = ser.write(payload.encode('ascii'))
        print("{} bytes written".format(n))
        time.sleep(0.1)


    def read_counter(self):
        # open serial communication
        ser = self.create_serial()
        ser.open()

        # requst register from counter
        self.write_to_serial(ser, '/?!\r\n')
        
        # read response    
        loop = True
        log = ""
        while(loop):
            # read next line
            response = ser.readline().decode('ascii')

            # if something could be read
            if response != '':
                # check if end of communication
                # was sent by counter            
                for c in response:
                    if ord(c) == 3:
                        loop = False
                logging.info(response)
                # append to counter log
                log = log + response.strip() + "\n"
        ser.close()
        return log
