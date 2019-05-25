function [frame, err] = anomalyStart(T, Y, interval, period)
    startpoints = 10000*[1, 1, 1; 1, 1, -1; 1, -1, 1; -1, 1, 1; 1, -1, -1; -1, 1, -1; -1, -1, 1; -1, -1, -1];
    count = 1;
    [f1, gof] = fit(T, Y, 'rat11', 'Start',startpoints(1,:));
    A(1) =  gof.rmse;
    [f2, gof] = fit(T, Y, 'rat11', 'Start',startpoints(2,:));
    A(2) =  gof.rmse;
    [f3, gof] = fit(T, Y, 'rat11', 'Start',startpoints(3,:));
    A(3) =  gof.rmse;
    [f4, gof] = fit(T, Y, 'rat11', 'Start',startpoints(4,:));
    A(4) =  gof.rmse;
    [f5, gof] = fit(T, Y, 'rat11', 'Start',startpoints(5,:));
    A(5) =  gof.rmse;
    [f6, gof] = fit(T, Y, 'rat11', 'Start',startpoints(6,:));
    A(6) =  gof.rmse;
    [f7, gof] = fit(T, Y, 'rat11', 'Start',startpoints(7,:));
    A(7) =  gof.rmse;
    [f8, gof] = fit(T, Y, 'rat11', 'Start',startpoints(8,:));
    A(8) =  gof.rmse;
    [x,y]=find(A==min(A));
    for i = 1:interval:size(T, 1)- period+1
        T1 = T(i:i+period-1,1);
        Y1 = Y(i:i+period-1,1);
        [f1, gof] = fit(T1, Y1, 'rat11', 'Start',startpoints(y,:));
        err(count) =  gof.rmse;
        count = count + 1;
    end
    max(err(1,3:end))
    for i = 3:size(err,2)-1
        if(err(1, i) >= 0.7*max(err(1, 3:end)))
            frame = (i-1)*interval+1;
            break
        end
    %[x,y]=find(err==max(err(1,2:end-1)));
    %frame = (y-1)*interval+1;
end