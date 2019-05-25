myFolderInfo = dir('anomaly_candidate_trajectory');
outPath = "anomaly_candidate_curvefit.txt";
out = fopen(outPath,'w');
for i = 3:size(myFolderInfo,1)
    M = csvread(strcat('anomaly_candidate_trajectory/',myFolderInfo(i).name));
    name = strsplit(myFolderInfo(i).name,'_');
    start = 1;
    if size(M,1)>30
        T = M(1:end,1);
        Y = M(1:end,2);
        if size(M,1)>400
            T = M(1:400,1);
            Y = M(1:400,2);
        end
        [start, err]=anomalyStart(T, Y, 2, 20);
    end 
    if T(start,1)<200
        start = 1;
    end
    fprintf(out, "%d %d %d %d\n",str2double(name(1,1)),str2double(name(1,2)),str2double(extractBetween(name(1,3),"",".csv")), T(start,1))
end