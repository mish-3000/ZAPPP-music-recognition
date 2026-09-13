from peak import allDicts
from mp3_to_wav import wavFilesPaths
import numpy as np

def combinations():
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

def hashes():
    hashinfo={}
    for file in wavFilesPaths:
        combinations=combinations()[file]
        for i in range(len(combinations)):
            freqA, freqB, timeA, deltaT, file = combinations[i]
            hash=((freqA& 0x3FF)<< 22) | ((freqB & 0x3FF) << 12) | (deltaT & 0xFFF)

            hashinfo[file] = (hash, timeA)

    return hashinfo
