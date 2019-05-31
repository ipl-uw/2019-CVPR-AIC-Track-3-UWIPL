## Model
Please download all four models, which given the download link in txt file. Two YOLO model is for detection, Facenet model is for extracting apperance from vehicles for TNT. TNT model is to combine tracklet into complete trajectory. You can find more details in this link: [Exploit the Connectivity: Multi-Object Tracking with TrackletNet][1]  

For detection, please use YOLO Candidate first to get anomaly candidates, and then use YOLO Robust on selected candidates. Those videos that are detected as candidates but do not detected by robust model will be sent into small object detection.  

[1]: https://arxiv.org/abs/1811.07258
