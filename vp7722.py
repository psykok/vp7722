#!/usr/bin/python

import sys
import time
import pyvisa
import string

class audio:
    def __init__(self,dev_id):
      self.dev_id=dev_id
      self.rm = None
      self.inst = None
      self.log_scale =[ 10,20,50,100,200,300,500,1000,2000,3000,5000,10000,20000,30000,50000,100000 ]


    def send_measurement(self,channel, meas, unit, freq, amp, filters):
        samp=""
        delay=1
        #source_freq = ("FR%.4EHZ" % freq)
        #source_ampl = ("AP%.4EDB" % amp)
        source_freq = ("FR%sHZ" % freq)
        source_ampl = ("AP%sDB" % amp)
            
        payload = source_freq + source_ampl + meas + filters + unit #+ "RS2"
        if freq <= 100:
            payload += "RS2" 
            delay = 10

#        print(payload)
        
        self.inst.write(payload)
        time.sleep(delay)
        samp = self.inst.read()
        
        return(samp)
    
    def main(self):
      rm = pyvisa.ResourceManager()
      devices = rm.list_resources()
      
      instid=""
      for x in devices:
          if self.dev_id in x:
            instid=x
       #inst = rm.open_resource('GPIB0::28::INSTR')
       #print(inst.query("*IDN?"))
    
      if instid:
          print(instid)
          self.inst = rm.open_resource(instid)
          #FR 10HZ to 110KZ
          #
          #AP -85.9DB to 14.0DB
          #
          # LEVEL :MM1
          # DISTN : MM4
          # TH1 : MM5
          #
          # DE1 : rms
          # DE2 : Avr
          # RS1 : fast resp
          # RS2 : slow resp
          # under 100HZ always use SLOW
          #
          # IN1 : L channel
          # IN2 : R channel
          # IN3 : L&R channel
          # L&R may not give correct data 
          #
          # LOG : V,%
          # LIN : dB
          #
          #
    
    
    
          #print("\nSet AMP and FREQ")
          #inst.write("AP1DBFR1KZ")
          #inst.write("FR5KZ")
          #mesure THD in %
          #self, channel, meas, unit, freq, amp, filters
          #for fstep in self.log_scale:
          #    res=self.send_measurement("L","MM4","LIN",fstep,1,"")
          #    print("%s;%s" % (fstep,res)) 
          
          res=self.send_measurement("L","MM4","LIN",1000,0,"")
          print(res) 
           
          #inst2 = Gpib.Gpib(0,22)
          #inst2.write("*IDN?")
          #strRead2 = inst2.read(100)
          #file = open("/root/gpib/gpsdo.txt", "a")
          #file.write( arrRead[1][2:] + ' ; ' + strRead2 )
          #file.close()
    
    
      else:
          print("device id is invalid")
    
    

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        objAudio = audio(sys.argv[1])
        objAudio.main()
    else:
        print("Usage: python myscript.py <device_id>, fe: 12")

