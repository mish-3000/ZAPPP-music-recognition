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
        freq, time, melxx = get_Sxx(file)
        input_melxx=np.where(melxx[minFreqBin:,:]>minDB, melxx[minFreqBin:,:], -np.inf); '''only consider frequencies above minFreqBin and power above minDB. powers below minDB are set to -inf so they will never be considered as peaks'''

        Pxx=ndimage.maximum_filter(input_melxx, size=5, mode='reflect'); '''creating a 2d array of the same shape as input_melxx where each element is the maximum value in a 5x5 neighborhood around the corresponding element in input_melxx.'''

        PxxFinalIndices=np.where(Pxx==input_melxx);  '''getting indices only where the local max is the original element itself. i.e. only local maximas survive in noise'''

        def get_peaks_for_file():
            for i in range(Pxx.shape[1]):
                if i in PxxFinalIndices[1]:
                    dictValueIndices=np.where(PxxFinalIndices[1]==i)[0]; '''storing all indices where there is a peak for this particular time bin'''
                    dictValues=Pxx[PxxFinalIndices[0][dictValueIndices], PxxFinalIndices[1][dictValueIndices]]
                    if np.all(dictValues == -np.inf):
                        continue; '''if all peaks are -infinity skip this iteration'''
                    if len(dictValues)>maxPeaksPerTimeframe:
                        sortedIndices=np.argsort(dictValues)[-maxPeaksPerTimeframe:][::-1]
                        dictValuesSorted=dictValues[sortedIndices]

                    else:
                        sortedIndices=np.argsort(dictValues)[::-1]
                        dictValuesSorted=dictValues[sortedIndices]
                    
                    freqTimeArr=[]; '''creating array of tuples of freq and time for which there ia a peak in this time bin'''
                    for j in sortedIndices:
                        freqTimeTuple1=(freq[PxxFinalIndices[0][dictValueIndices[j]]+minFreqBin],time[i])
                        freqTimeArr.append(freqTimeTuple1)
                
                
                    if -np.inf in dictValuesSorted:
                        indicesWithoutNegInf=np.where(dictValuesSorted!=-np.inf)[0]; '''-inf can be considered as a peak if there were no other higher values in its neighbourhood, so excluding it'''
                        dictValuesSorted=dictValuesSorted[indicesWithoutNegInf]
                    
                        freqTimeArr=[]
                        for j in indicesWithoutNegInf:
                            freqTimeTuple2=(freq[PxxFinalIndices[0][dictValueIndices[sortedIndices][j]]+minFreqBin],time[i])
                            freqTimeArr.append(freqTimeTuple2)
                    for j in range(len(dictValuesSorted)):  
                        dictkeyTuple=freqTimeArr[j] ; '''for every peak in this time bin, a freq, time tuple and the peak value is yielded'''
                        yield dictkeyTuple, dictValuesSorted[j]
        peaksDict={}; '''for all time bins and all their respective peaks, freq, time tuple and peak value is yielded and stored in a dictionary with the key as tuple'''
        for dictKeyTuple, dictValuesSorted in get_peaks_for_file():
            peaksDict.update({dictKeyTuple:dictValuesSorted}) 
        allPeaks[file]=peaksDict ; '''for all the n-songs, n dictionaries are created with the file name as key that contain dictionary of peak infos of that song'''            
    return allPeaks


        

