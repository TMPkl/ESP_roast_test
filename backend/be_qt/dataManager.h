#pragma once
#include <QVector>

class DataManager {
public:
    DataManager() = default;
    ~DataManager() = default;

    double AddDataRecord(double time, double value);
    double GetValue(double time); // trzeba bedzie robic interpolacje jakby nie bylo wartosci w danym czasie
    //QVector<double> GetRecordedTime(); // zwroci wektor z czasami ktore zostaly realnie pobrane
    int len(); // ilość rekordów

private:
    QVector<QVector<double>> dataRecords; // [[czas, wartość], [czas, wartość], ...]
};