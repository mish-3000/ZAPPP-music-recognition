from peak import allDicts
from mp3_to_wav import wavFilesPaths
import numpy as np

def hashes():
    allCombinations={}
    for file in wavFilesPaths:
        peaks = allDicts(file)
        combinationsPerFile=[]
        for i in range(len(peaks)):
            freqA, timeA = peaks[i]
            combinationsPerPeak=[]
            if freqA<1000:
                for j in range(i+1, len(peaks)):
                    freqT, timeT = peaks[j]
                    if freqT<1000 :
                        if timeT-timeA>50:
                            break
                        if timeT-timeA>0:
                            combinationsPerPeak.append((freqA, freqT, timeA, timeT-timeA, file))
                            if len(combinationsPerPeak)>10:
                                break
            if len(combinationsPerPeak)>0:
                combinationsPerFile.extend(combinationsPerPeak)            
            
        
        allCombinations[file] = combinationsPerFile
    return allCombinations


        

            