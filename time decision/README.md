## Time Decision  
### Get Frozen Period
Use “get_freeze_period.py” to get times when video is frozen. Output is used in anomaly candidate selection to ignore candidates that appear when video is frozen  
### Tracking ID Matching  
Fix ID switching with “track_ID_match.py”.  
Match tracking ID with anomaly candidate with “get_anomaly_ID.py”. Takes path to byway/parkway segmentation mask as input. Takes path to “anomalyCandidate_processed.txt”. Outputs “anomalyCandidate_processed2.txt” which removes false positives with byway/parkway mask. Outputs “anomaly_candidate_ID.txt” with [video #] [part #] [ID #]. Outputs trajectory of anomaly IDs into folder “anomaly_candidate_trajectory”.  
### Stop Time Estimation  
Get slow down time with “get_slowdown_time.m”. Takes path to “anomaly_candidate_trajectory” as input. Uses function in “anomalyStart.m”. Outputs “anomaly_candidate_curvefit.txt” which has [video #] [part #] [ID #] [slowdown time].  
Get stop time with “get_stop_time.py”. Takes “anomaly_candidate_curvefit.txt” as input. Takes path of processed SCT results (With track_ID_match) as input
Outputs “stop_time.txt”.
### Enter Grass Time Estimation
Get enter grass time with “enter_grass_time.py”. Takes “stop_time.txt” as input
Takes path of processed SCT results (With track_ID_match) as input. Takes path of grass masks. Outputs enter grass time for videos that have a stop time.
### Anomaly Start Time Estimation
Gets anomaly start time with “get_start_time.py”. Takes “anomaly_candidates_processed2.txt”, “enter_grass_time.txt”, and “stop_time.txt”. Outputs “anomaly_start_time.txt”



