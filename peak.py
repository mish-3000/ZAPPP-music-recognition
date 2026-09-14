from spectrogram import get_Sxx
from scipy import ndimage
import matplotlib.pyplot as plt
from mp3_to_wav import wavFilesPaths
import numpy as np

minFreqBin=23 ;'''approx 250Hz'''
maxPeaksPerTimeframe=3
minDB=-50
def get_peaks(minFreqBin, maxPeaksPerTimeframe, minDB): 
    allPeaks={}
    for file in wavFilesPaths:
        def get_peaks_for_file(file):
            freq, time, melxx = get_Sxx(file)
            input_melxx=np.where(melxx[minFreqBin:,:]>minDB, melxx[minFreqBin:,:], -np.inf); '''only consider frequencies above minFreqBin and power above minDB. powers below minDB are set to -inf so they will never be considered as peaks'''

            Pxx=ndimage.maximum_filter(input_melxx, size=5, mode='reflect'); '''creating a 2d array of the same shape as input_melxx where each element is the maximum value in a 5x5 neighborhood around the corresponding element in input_melxx.'''

            PxxFinalIndices=np.where(Pxx==input_melxx);  '''getting indices only where the local max is the original element itself. i.e. only local maximas survive in noise'''

        
            for i in range(Pxx.shape[1]):
                if i in PxxFinalIndices[1]:
                    ValueIndices=np.where(PxxFinalIndices[1]==i)[0]; '''storing all indices where there is a peak for this particular time bin'''
                    Values=Pxx[PxxFinalIndices[0][ValueIndices], PxxFinalIndices[1][ValueIndices]]
                    if np.all(Values == -np.inf):
                        continue; '''if all peaks are -infinity skip this iteration'''
                    if len(Values)>maxPeaksPerTimeframe:
                        sortedIndices=np.argsort(Values)[-maxPeaksPerTimeframe:][::-1]
                        ValuesSorted=Values[sortedIndices]

                    else:
                        sortedIndices=np.argsort(Values)[::-1]
                        ValuesSorted=Values[sortedIndices]
                    
                    freqTimeArr=[]; '''creating array of tuples of freq and time for which there ia a peak in this time bin'''
                    for j in sortedIndices:
                        freqTimeTuple1=(time[i],freq[PxxFinalIndices[0][ValueIndices[j]]+minFreqBin])
                        freqTimeArr.append(freqTimeTuple1)
                
                
                    if -np.inf in ValuesSorted:
                        indicesWithoutNegInf=np.where(ValuesSorted!=-np.inf)[0]; '''-inf can be considered as a peak if there were no other higher values in its neighbourhood, so excluding it'''
                        ValuesSorted=ValuesSorted[indicesWithoutNegInf]
                    
                        freqTimeArr=[]
                        for j in indicesWithoutNegInf:
                            freqTimeTuple2=(time[i],freq[PxxFinalIndices[0][ValueIndices[sortedIndices][j]]+minFreqBin])
                            freqTimeArr.append(freqTimeTuple2)
                    for j in range(len(ValuesSorted)):  
                        Tuple=freqTimeArr[j] ; '''for every peak in this time bin, a freq, time tuple and the peak value is yielded'''
                        yield Tuple
        peaks=[]; '''for all time bins and all their respective peaks, freq, time tuple and peak value is yielded and stored in a dictionary with the key as tuple'''
        for Tuple in get_peaks_for_file(file):
            peaks.append(Tuple)
            
        allPeaks[file]=peaks ; '''for all the n-songs, n dictionaries are created with the file name as key that contain dictionary of peak infos of that song'''            
    return allPeaks

def allDicts(file):
    return get_peaks(minFreqBin, maxPeaksPerTimeframe, minDB)[file]
        

