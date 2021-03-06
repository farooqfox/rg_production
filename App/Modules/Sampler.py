import ctcsound
import os

class CsoundSampler:
  
    def __init__(self):
        print("init Csound")
        self.cs = ctcsound.Csound()
        # self.audio_dir =  "../resources/audiodata/"
        self.audio_dir = "/Users/leofltt/Documents/Github/rg_production/resources/audiodata/"
        sample = "42.wav"
        self.sample_path = self.audio_dir + sample
        
  
    def compileAndStart(self):
        print("Starting Sampler")
        csd = f'''

  <CsoundSynthesizer>

  <CsOptions>
    -d -M0 -o dac -m0
    -+rtmidi=portmidi
    --midi-key-cps=6 --midi-velocity-amp=4
  </CsOptions>

  <CsInstruments>
  sr = 22000
  ksmps = 32
  nchnls = 2
  0dbfs = 1.0

  massign 0, 1

    instr 1 ; Sampler

    ;Sname chnget "gSname"
    Sname = "{self.sample_path}"

    iNum notnum
    {self.stringPitch2File()}


    ivol = p4
    ipb = 1
    inchs = filenchnls(Sname)


    if inchs == 1 then

    aLeft diskin2 Sname, ipb
    
    aL = aLeft*p4
    aR = aLeft*p4

    else

    aLeft, aRight diskin2 Sname, ipb

    aL =  aLeft*p4
    aR = aRight*p4

    endif

    outs aL,aR

    endin
    

  </CsInstruments>

  <CsScore>

  f 0 3600    ; 1 hour long empty score

  </CsScore>

  </CsoundSynthesizer>


  '''
        self.cs.setStringChannel("gSname", self.sample_path)
        self.cs.compileCsdText(csd)
        self.cs.start()
        self.pt = ctcsound.CsoundPerformanceThread(self.cs.csound())
        self.pt.play()

    def playSample(self):
        sco = "i 1 0 1 1 " + '\"' + self.sample_path + '\"' + " 40"

        self.cs.readScore(sco) 
        print(self.stringPitch2File())

    def cleanup(self):
        self.pt.stop()
        self.pt.join()
        self.cs.reset()
    
# ==============================

    # 
    def stringPitch2File(self):
      s = f'''
      if iNum == 40 then
      Sname = "{self.sample_path}"
      '''

      for i in range(0, 24):
        root = 40-12 # e2 is 40
        note = i + root
        s += f'''
         elseif iNum == {note} then
          Sname = "{self.audio_dir}{note}.wav"
        '''

      s += "endif\n"

      return s