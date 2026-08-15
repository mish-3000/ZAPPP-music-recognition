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
        input_melxx=np.where(melxx[minFreqBin:,:]>minDB, melxx)
        Pxx=ndimage.maximum_filter(input_melxx, size=5, mode='reflect')
        for i in range (time.shape[0]):
             peaks=np.where(Pxx[:,i]==input_melxx[:,i], input_melxx[:,i])    
             if len(peaks)>maxPeaksPerTimeframe:
                sortedPeaks=peaks[np.argsort(peaks)[3:][::-1]]
                Pxx[:,i]=sortedPeaks

 