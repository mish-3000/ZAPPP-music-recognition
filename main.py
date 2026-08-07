import subprocess
import os
mp3Files=r'C:\Users\Hp\OneDrive\Desktop\reactjs\shazam\database\mp3Files'
wavFiles=r'C:\Users\Hp\OneDrive\Desktop\reactjs\shazam\database\wavFiles'
pathToffmpeg = r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
for file in os.listdir(mp3Files):
    subprocess.call([pathToffmpeg,'-i', os.path.join(mp3Files, file), os.path.join(wavFiles, str(file.split('.')[0]+'.wav'))]) 
    print(f'Converted {file} to wav format')
    