import sys,os 
import time,random
import numpy as np 
import wave,argparse,pygame
from collections import deque
from matplotlib import pyplot as plt

gShowPlot=False # show plot of algorithm in action?

pmNotes={'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}

#write out WAVE file
def writeWAVE(fname,data):
    file=wave.open(fname,'wb')
    # wav file parameters
    nChannels=1 
    sampleWidth=2
    frameRate=44100
    nFrames=44100
    #set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames,
                    'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

#generate note of given frequency
def generateNote(freq):
    nSamples=44100
    sampleRate=44100
    N=int(sampleRate/freq)
    # initialize ring buffer
    buf=deque([random.random()-0.5 for i in range(N)])
    # plot of flag set
    if gShowPlot:
        axline,=plt.plot(buf)
    # init sample buffer
    samples=np.array([0]*nSamples,'float32')
    for i in range(nSamples):
        samples[i]=buf[0]
        avg=0.995*0.5*(buf[0]+buf[1])
        buf.append(avg)
        buf.popleft()
        if gShowPlot:
            if i % 1000==0:
                axline.set_ydata(buf)
                plt.draw()
    samples=np.array(samples*32767,'int16')
    return samples.tobytes()

# play a wav file
class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100,-16,1,2048) # 初始化：采样率44100，16位有符号值，单声道，缓冲区大小2048
        pygame.init()
        # dictionary of notes
        self.notes={} # create a notes dictionary 
    # add a note
    def add(self,fileName):
        self.notes[fileName]=pygame.mixer.Sound(fileName)
    # play a note
    def play(self,fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName+'not found')
    # play a random note
    def playRandom(self):
        index=random.randint(0,len(self.notes)-1)
        note=list(self.notes.values())[index]
        note.play()

def main():
    global gShowPlot

    parser=argparse.ArgumentParser(description='generating sounds with Karplus String Algorithm')
    parser.add_argument('--display',action='store_true',required=False)
    parser.add_argument('--play',action='store_true',required=False)
    parser.add_argument('--piano',action='store_true',required=False)
    args=parser.parse_args() 

    #show plot if flag set
    if args.display: # 如果使用了display命令行选项
        gShowPlot=True 
        plt.ion() #启动matplotlib中的交互模式

    #create note player
    nplayer=NotePlayer()

    print('creating notes...')
    for name,freq in list(pmNotes.items()):
        fileName=name+'.wav'
        if not os.path.exists(fileName) or args.display:
            data=generateNote(freq) #生成五声音阶的音符
            print('creating'+fileName+'...')
            writeWAVE(fileName,data)
        else:
            print('fileName already created. skipping...')

        #add note to player
        nplayer.add(name+'.wav')

        #play note if display flag set
        if args.display:
            nplayer.play(name+'.wav')
            time.sleep(0.5)

    #play a random tune
    if args.play:
        while True:
            try:
                nplayer.playRandom()
                rest=np.random.choice([1, 2, 4, 8], 1, 
                                        p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

    if args.piano:
        while True:
            for event in pygame.event.get():
                if (event.type==pygame.KEYUP):
                    print('key pressed')
                    nplayer.playRandom()
                    time.sleep(0.5)

if __name__=='__main__':
    main()





















