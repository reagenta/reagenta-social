import sys, json, subprocess, wave
from vosk import Model, KaldiRecognizer, SetLogLevel
SetLogLevel(-1)
src, out = sys.argv[1], sys.argv[2]
wav = out + '.16k.wav'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-ar','16000','-ac','1',wav],check=True)
m = Model('/tmp/vosk-model-small-it-0.22')
wf = wave.open(wav,'rb'); rec = KaldiRecognizer(m, wf.getframerate()); rec.SetWords(True)
words=[]
while True:
    d = wf.readframes(4000)
    if not d: break
    if rec.AcceptWaveform(d): words += json.loads(rec.Result()).get('result',[])
words += json.loads(rec.FinalResult()).get('result',[])
json.dump([(w['word'],w['start'],w['end']) for w in words], open(out,'w'), ensure_ascii=False)
print(len(words),'words')
