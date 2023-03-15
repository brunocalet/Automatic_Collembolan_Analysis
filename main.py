'''
This is the main Python file which contains functions for
particle size analysis.
'''

import imagej
import numpy as np
import pandas as pd
from scyjava import jimport
from sklearn.cluster import KMeans
from statistics import mean, stdev
import os
import matplotlib.pyplot as plt

ij = imagej.init()

def analyzeParticles (sampleImage, scale = 1, knownDistance = 1, distinguishJuveniles = False):
    '''
    Uses ImageJ API to analyze image and create CSV file containing the analysis results.
    
    sampleImage (string): path of input image containing particles
    scale (float): number of pixels measured
    knownDistance (float): known distance of measured pixels in milimeters
    distinguishJuveniles (boolean): if true, KMeans clustering will be used to
                                    distinguish juvenile from adult individuals. This
                                    can be used if input image contains Collembolans.
    '''
    
    # Initialize ImageJ2
    ij
    
    analyzedDirectory = "img/analyzed"
    resultsDirectory = "results"
    os.makedirs(analyzedDirectory, exist_ok=True)
    os.makedirs(resultsDirectory, exist_ok=True)
    
    # Open image and convert from Dataset to ImagePlus
    img = ij.io().open(f"img/{sampleImage}")
    imp = ij.py.to_imageplus(img)

    # Analyze image: after color processing size parameters are displayed in ResultsTable
        # Color processing
    
    Prefs = jimport("ij.Prefs")
    Prefs.blackBackground = True
    ij.IJ.setAutoThreshold(imp, "Otsu dark") #Li dark
    mask = imagej._ImagePlus()("cells-mask", imp.createThresholdMask())
    imp.close()

    # Clean up the binary mask.
    ij.IJ.run(mask, "Dilate", "")
    ij.IJ.run(mask, "Fill Holes", "")

        # Size analysis
    # Scale calibration
    scaleMeasurement = scale
    ij.IJ.run(mask, "Set Scale...", f"distance={scaleMeasurement} known={knownDistance} pixel=1 unit=mm")

    # Particle analysis
    ij.IJ.run("Set Measurements...", "area perimeter shape feret's  redirect=None decimal=3")
    ij.IJ.run(mask, "Analyze Particles...", "show=Overlay display exclude clear include summarize overlay")

    # Save enumerated picture of the sample
    ij.IJ.run(mask, "Invert", "")
    ij.IJ.save(mask, f"img/analyzed/{sampleImage.rsplit('.')[0]}-analyzed.png")
    mask.close()

    # Put ResultsTable into variable rt
    rt = ij.ResultsTable.getResultsTable()

    # Extract values from ResultsTable and Convert them from  Java string datatype to numpy array
    feretsDiameter = np.array(rt.getColumn(rt.getColumnIndex("Feret")))
    animalArea = np.array(rt.getColumn(rt.getColumnIndex("Area")))
    animalCircularity = np.array (rt.getColumn(rt.getColumnIndex("Circ.")))
    animalRoundness = np.array(rt.getColumn(rt.getColumnIndex("Round")))

    # Value standardization: standardizedValues = (originalValues - meanValue) / standardDeviation
    feretsDiameterSt = (feretsDiameter - np.mean(feretsDiameter)) / np.std(feretsDiameter)
    animalArea = (animalArea - np.mean(animalArea)) / np.std(animalArea)
    animalCircularity = (animalCircularity - np.mean(animalCircularity)) / np.std(animalCircularity)
    animalRoundness = (animalRoundness - np.mean(animalRoundness)) / np.std(animalRoundness)

    # Get the ID index of every measurement
    animalID = np.arange(1, (len(feretsDiameter) + 1), 1, dtype=int)

    # Create data table containing animal ID and corresponding Feret's diameter
    dataTable = np.vstack((animalID, feretsDiameter, animalArea, feretsDiameterSt, animalCircularity, animalRoundness)).T
    dataFrame = pd.DataFrame(dataTable)
    dataFrame.columns = ["animal ID", "Feret\'s diameter", "area", "standardized Feret\'s diameter", "Circularity", "Roundness"]

    if distinguishJuveniles == True:
        # K-means clustering to distinguish juvenile from adult animals
        kMeans = KMeans(init = "k-means++", n_clusters = 2, n_init = 12)
        kMeans.fit(dataTable[:, 2:dataTable.shape[1]])
        kMeansLabels = kMeans.labels_

        # Save data to .csv format
        dataFrame["k-mean labels"] = kMeansLabels.tolist()
        dataFrame = dataFrame.sort_values("Feret\'s diameter", ascending=True)
        dataFrame.to_csv(f"results/{sampleImage.rsplit('.')[0]}.csv", index = False)
    else:
        dataFrame = dataFrame.sort_values("Feret\'s diameter", ascending=True)
        dataFrame.to_csv(f"results/{sampleImage.rsplit('.')[0]}.csv", index = False)
    
    ij.window().clear()

def getSummary(variable):
    '''
    Takes variable as input which is 1D array containing
    univariate data, and outputs summary statistics inside
    pandas DataFrame containing mean, standard deviation,
    minimum and maximum values, and percent of particles
    that are smaller than 60 micrometers.
    
    variable: input univariate data (1D array)
    '''
    count = 0
    for var in variable:
        if var <= 60:
            count += 1
    
    summary = pd.DataFrame({
        'Mean Feret\'s diameter' : [mean(variable)],
        'Standard Deviation' : [stdev(variable)],
        'Min' : [min(variable)],
        'Max' : [max(variable)],
        '<60μm [%]' : [count / len(variable) * 100]
    })
    
    return summary
    
def savePlots(variable):
    '''
    Creates and saves plot based on input univariate data (variable).
    
    variable: input univariate data (1D array)
    '''
    # Calculating ticks to display them on x axis of a histogram
    ticks = np.arange(min(variable), max(variable), (max(variable) - min(variable)) / 4)
    ticks = np.append(ticks, [60, max(variable)])
    ticks = np.sort(ticks)

    # Plot histogram of microplastics sizes in a sample
    plt.hist(variable, bins = 4)
    plt.title('Collembolan (F. candida) body length distribution')
    plt.xlabel("size interval")
    plt.ylabel("frequency")

    plt.xticks(ticks, rotation = 45, fontsize = 6)
    plt.yticks(np.arange(0, len(variable), 50), fontsize = 6)
    plt.savefig("results/size_distribution_histogram.png")
    plt.ylim((0.0, len(variable)))
    plt.clf()

    plt.boxplot(variable)
    plt.title('Collembolan (F. candida) body length distribution')
    plt.xlabel("F. candida")
    plt.ylabel("size [μm]")
    plt.savefig("results/size_distribution_boxplot.png")
    plt.clf()