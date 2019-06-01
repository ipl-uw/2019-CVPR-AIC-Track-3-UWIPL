# 2019 CVPR AI City Challenge Track 3
This repository is used to do traffic anomaly detection, including lane violation, traffic accident, emergency stop on highway, etc.

## Updates
*For Collaborators: Please write your summary of your updates in the following format:*  
**5/31/2019&emsp;Update four pre-trained models, update time decision.**  
**4/9/2019&emsp;Update scripts for candidate selection and models**

## Introduction
This is an overall description of the repository. Detailed descriptions could be found under each folders.  
Under **candidate selection** are the scripts for getting anomaly candidate video IDs.  
Scripts under **time decision** are used to get the exact startting time of the anomaly cases.  
**util** includes all necessary scripts for processing the output from detection to get tracking result using [TNT][1].  
All the models used should be placed under **model**, and you can find the download link for all three models in a txt file under that folder.  
You should run the scripts under **candidate selection** first, and then run TNT to get tracking result. After that please run codes under **time decision** to get the exact starting time of the anomaly.   

Xinyu (Xavier) Yuan  
4/9/2019

[1]: https://github.com/GaoangW/TNT/tree/master/AIC19
