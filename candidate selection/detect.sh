#!/bin/bash

for i in {6..6}
do

	cp "data/aic19-track3-test-data/"$i".avi" ./
	mkdir "data/track3_test_bg_detection/"$i
	./darknet detector demo visdrone.data yolov3-voc.cfg yolov3-voc-25310.backup $i".avi" -thresh 0.80

done
