from spectrogram import get_Sxx
from scipy import ndimage
import matplotlib.pyplot as plt
from mp3_to_wav import wavFilesPaths
import numpy as np

minFreqBin=23 ;'''approx 250Hz'''
maxPeaksPerTimeframe=3
minDB=-50
def get_peaks(minFreqBin, maxPeaksPerTimeframe, minDB):
    for file in wavFilesPaths:
        freq, time, melxx = get_Sxx(file)
        input_melxx=np.where(melxx[minFreqBin:,:]>minDB, melxx[minFreqBin:,:], -np.inf)
       
        '''only consider frequencies above minFreqBin and power above minDB. powers below minDB are set to -inf so they will never be considered as peaks'''

        Pxx=ndimage.maximum_filter(input_melxx, size=5, mode='reflect')
        '''creating a 2d array of the same shape as input_melxx where each element is the maximum value in a 5x5 neighborhood around the corresponding element in input_melxx.'''

        PxxFinalIndices=np.where(Pxx==input_melxx)
        '''getting indices only where the local max is the original element itself. i.e. only local maximas survive in noise'''

        for i in range(Pxx.shape[1]):
            if i in PxxFinalIndices[1]:
                dictValueIndices=np.where(PxxFinalIndices[1]==i)[0] 
                dictValues=Pxx[PxxFinalIndices[0][dictValueIndices], PxxFinalIndices[1][dictValueIndices]]
                if len(dictValues)>maxPeaksPerTimeframe:
                    dictValuesSorted=dictValues[np.argsort(dictValues)[-maxPeaksPerTimeframe:][::-1]]
                else:
                    dictValuesSorted=dictValues[np.argsort(dictValues)[::-1]]
                '''dictKey=str(PxxFinalIndices[0][dictValueIndices][list(range(len(dictValuesSorted)))] )+'_'+str(i)'''
                if -np.inf in dictValuesSorted:
                    dictValuesSorted=dictValuesSorted[np.where(dictValuesSorted!=-np.inf)]
                    '''dictKey=str(PxxFinalIndices[0][dictValueIndices][list(range(len(dictValuesSorted)))] )+'_'+str(i)'''
                '''-inf can be considered as a peak if there are no other values in that neighborhood. so if -inf is present in the list of peaks, remove it and update the dictKey accordingly.'''

                yield dictKey, dictValuesSorted
        '''for every timeframe column, if any peaks exist, get indices of those peaks. if no. of peaks is more than maxPeaksPerTimeframe, sort the peaks in descending order and return only the top maxPeaksPerTimeframe peaks. else return all peaks sorted in descending order.'''      

def get_peaks_Dict():
    for dictKey, dictValuesSorted in get_peaks(minFreqBin, maxPeaksPerTimeframe, minDB):
        peaksDict={dictKey: dictValuesSorted}
        yield peaksDict

peaksDictArray=[]


for peaksDict in get_peaks_Dict():
    peaksDictArray.append(peaksDict)
'''for every timeframe column where peaks exist, there will be a dictionary with key as time and freq bin reference and value as a list of peak values in descending order.'''