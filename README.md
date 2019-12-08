# Face matcher project

### Details 

Python 3.5.6
See packages.txt for list of required packages

### Images

https://drive.google.com/open?id=14ZEyWfinmlOw0kaHXIBXXlzkMY0Ds87Z

### Overview

Face recognition (FR) algorithms are becoming more and more commonly used in world today. From fraud detection at passport offices to real-time face recognition at sporting stadiums, you have probably been matched before! Given their increased use, we should also be wondering how accurate they are. Face recognition is a subset of the broader field of [biometrics](https://en.wikipedia.org/wiki/Biometrics) which aims to recognise a person based on anaylsis of their uniquq biological characteristics.

[Open source algorithms](https://github.com/ageitgey/face_recognition) are readily available such as this example written using dlib. dlib is an open source collection of image matching libraries written in C++. The 'face_recognition' module is a wrapper allowing access to this functionality using Python.

[Labelled data sets](https://sites.google.com/view/sof-dataset) can also be found which provide a useful tool to test algorithms and their accuracy before putting them to use. The fact that the data is labelled means the "ground truth" information is available. This allows testers to ensure they are matching pairs of images of the same person's face, or images of different faces at any given time. This means the accuracy of the score produced by an algorithm can be easily measured, since a low score should result if the faces are different, and a high score should result if the images are of the same person. Doing this over a large sample set can give a bigger picture of how accurate the algorithm performs statistically. The labelling of the data set referenced here is explained [in this report](http://www.cse.yorku.ca/~mafifi/TheSpecsonFace.pdf).

Ultimately the [reciever operating characteristics](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) determined from an algoritm will give an overview of its performance. False acceptance rate (FAR) and false rejection rate (FRR) are commonly used to check the performance of an algorithm. In laymans terms:

* False acceptance -> A high score from the algorithm despite the images being of different persons.
* False rejection -> A low score from the algorithm despite the images being of the same person.

