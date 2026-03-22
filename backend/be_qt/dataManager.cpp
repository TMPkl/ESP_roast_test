#include "dataManager.h"
#include <algorithm>

double DataManager::AddDataRecord(double time, double value) {
    dataRecords.push_back({time, value});
    return dataRecords.size();
}

double DataManager::GetValue(double time){
    for (const auto& record : dataRecords) {
        if (record[0] == time) {
            return record[1];
        }
    }
    std::sort(dataRecords.begin(), dataRecords.end(), [](const QVector<double>& a, const QVector<double>& b) {
        return a[0] < b[0];
    });
    for (int i = 0; i < dataRecords.size() - 1; ++i) { //bardzo porosta interpolacja, poznije zrobic lepiej najlepiej wielomanem tak jak mma w pliku inzynierksim
        if (dataRecords[i][0] < time && time < dataRecords[i + 1][0]) {
            double t1 = dataRecords[i][0];
            double v1 = dataRecords[i][1];
            double t2 = dataRecords[i + 1][0];
            double v2 = dataRecords[i + 1][1];
            return v1 + (v2 - v1) * (time - t1) / (t2 - t1);
        }
        else if (time < dataRecords[0][0] && time > dataRecords[dataRecords.size() - 1][0]) {
            return -1.0; 
        }
    }

    return -1.0;    
}

int DataManager::len() {
    return dataRecords.size()/2;
}