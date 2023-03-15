# Automatic_Collembolan_Analysis
This repository contains code, example files and results files for the automatic image recognition of *Folsomia candida* species. Using this code it is possible to recognize *F. candida* individuals placed on a black background. The routine is used to count individuals in a sample, differentiate adult from juvenile individuals, and to get a data table with different size parameters for each individual animal. It is possible to calibrate the scale of the images, which allows for obtaining measurements in different units of size.

This routine was created using [PyImageJ](https://github.com/imagej/pyimagej), a Python wrapper for ImageJ2, and [scikit-learn](https://scikit-learn.org/stable/), a machine learning library for Python that provides tools for data analysis and modeling.

Steps to run the analysis:

1. Create conda environment and install needed dependencies:

Create new environment:
```
conda create -n collembolanRecognition python=3.9
```

Activate the environment:
```
conda activate collembolanRecognition
```

Install dependencies:
```
conda install -c conda-forge pyimagej
```

```
conda install -c conda-forge scyjava
```

```
conda install -c anaconda scikit-learn
```

```
conda install numpy pandas matplotlib
```

2. Put the sample image in PNG format inside the `img` folder: image should be named liek this: `sample1.png`

Folder structure looks like this:

```bash
├── collembolaAnalysis.py
├── img
│   ├── sample1.png
│   └── scale_calibration_results.csv
├── __init__.py
├── main.py
```

Sample image looks like this:

<img src="https://user-images.githubusercontent.com/92308626/225318694-4780fcfd-eab3-4267-a1f9-e5d89cf88910.png" width="500">

Source: [Mallard et al. 2013](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0064387)

3. Run the `collembolaAnalysis.py` file

```
python collembolaAnalysis.py
```

After the run, new files are created and the folder structure now looks like this:

```bash
├── collembolaAnalysis.py
├── img
│   ├── analyzed
│   ├── sample1.png
│   └── scale_calibration_results.csv
├── __init__.py
├── main.py
└── results
    ├── collembolan_size_analysis.xlsx
    ├── size_distribution_boxplot.png
    └── size_distribution_histogram.png
```

Inside the `img` folder, the `analyzed` folder is created, where analyzed image contains drawn polygons around original animals with the associated id number:

<img src="https://user-images.githubusercontent.com/92308626/225320468-90d2b292-1a64-48ee-93ac-b5d8e398fb6c.png" width="500">

As a result of the polygons (i.e. each individual animal) size parameters measurement (diameter, area, circularity, roundness) the data table is created. This data table is used in machine learning method K-means clustering to derive two clusters: one representing juvenile animals and the other representing adult animals. It is also possible to deactivate juveniles from adult animals differentiation if the image only contains adult animals or juvenile animals.

In the `results` folder, size parameters of animals are stored in an Excel file. The file includes the following parameters for each animal: animal ID (from the previous analyzed image), Feret's diameter and area of each animal, standardized Feret's diameter, circularity, and roundness parameters, k-mean labels (0 or 1) - 0 being juvenile animal and 1 being adult animal, Sample Image Index - the index of image if there are more than 1 analyzed image, Feret's Diameter [μm]. The Excel file sheet `summary` contains basic descriptive statistics of given data (mean, minimum and maximum body size with standard deviation). Also, boxplot and histogram charts are created to visualize given data.

<img src="https://user-images.githubusercontent.com/92308626/225331144-0d9aa451-9d56-4990-96af-19a3194c1a48.png" width="250"><img src="https://user-images.githubusercontent.com/92308626/225331173-14d7cd05-16b5-4509-9636-19d04ccbc52d.png" width="250">

This routine can be used not only for automatization of the counting and measuring of collembolans, but for the automatization of microplastics particles quantitative and qualitative analysis. For the analysis of microplastics, the same logic applies as described above. Here are sample images that can be loaded into this routine:

<img src="https://user-images.githubusercontent.com/92308626/225340832-4513b506-559c-46dc-8eae-725934a06688.jpg" width="500">

The image is part of our research on soil microplastics. The microplastics on this image are artificialy made by using electric knife sharpener to hone HDPE bottle. Size distribution of the particles is roughly from 4 μm to 1 mm.

The analysis derived the following image:

<img src="https://user-images.githubusercontent.com/92308626/225340444-15dbc4af-3280-4f11-ac1f-298f47a74b63.png" width="500">

The analysis derived the following size distribution charts:

<img src="https://user-images.githubusercontent.com/92308626/225341167-737e789e-9ba6-4463-9e51-efd2a70c5e44.png" width="250"><img src="https://user-images.githubusercontent.com/92308626/225341173-1c0b665f-879f-4290-b8d0-27f6901afbc7.png" width="250">

It is also possible to differentiate between microplastics fragments and fibers by activating K-means clustering.

This routine is the part of the ongoing research of soil microplastics conducted at the Subdepartment of Quantitative Ecology, Department of Biology, University of Josip Juraj Strossmayer in Osijek, Croatia.

For any further information please contact: bruncaleta@gmail.com.
