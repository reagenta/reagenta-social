import json, subprocess, sys
# cut.py <id> <kind> <out>  kind: teaser | mid
vid, kind, out = sys.argv[1:4]
ENDO = float(sys.argv[4]) if len(sys.argv) > 4 else None
T = json.load(open(f'/home/claude/work/out/{vid}.times.json'))
st = T['scenes'] + [T['outro']]
n = len(T['scenes'])
def span(i0, mn=9.0, mx=17.0):
    j = i0 + 1
    while j < n and st[j] - st[i0] < mn: j += 1
    j = min(j, n)
    while j - 1 > i0 and st[j] - st[i0] > mx: j -= 1
    return i0, j
if kind == 'teaser': i0, j = span(0, 9.0)
else: i0, j = span(max(1, n // 2 - 1), 9.0)
s = st[i0] + (0.0 if i0 == 0 else 0.31); e = (ENDO if ENDO else st[j] - 0.16)
d = e - s
print(vid, kind, f'{s:.2f}-{e:.2f} ({d:.1f}s) scenes {i0}..{j-1}')
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{s:.3f}','-i',f'/home/claude/work/out/{vid}.mp4','-t',f'{d:.3f}',
  '-vf',f'fade=t=out:st={d-0.3:.2f}:d=0.3','-af',f'afade=t=out:st={d-0.3:.2f}:d=0.3','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',out],check=True)
