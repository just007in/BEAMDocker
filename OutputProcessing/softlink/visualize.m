file = importdata("trips_data/0.trips-iter-50-1sec.csv");

% scatter(file.data(:,3),file.data(:,4))

N = 50;
data = int32.empty;
for i = 1:N
    a = file.data(:,1) == i - 1;
    data = cat(3,data,file.data(a,2:end));
end

a = size(data);
a = a(1);
c = linspace(1,10,length(data));
hPlot = scatter(NaN, NaN, 'g', 'filled');
axis([-2000 1000 -1000 0])
for i = 1:a
    set(hPlot, 'XData', data(i,2,:), 'YData', data(i,3,:));
    drawnow limitrate
    pause(0.04)
end