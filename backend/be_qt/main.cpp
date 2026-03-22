#include <QCoreApplication>
#include "HttpServer.h"
#include "dataManager.h"
#include <iostream>

#define API_PORT 5555

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    DataManager dataManagerTest; // Inicjalizacja DataManagera
    dataManagerTest.AddDataRecord(1.0, 10.0);
    dataManagerTest.AddDataRecord(2.0, 15.0);
    dataManagerTest.AddDataRecord(3.0, 30.0);

    std::cout << "Value at time 1.5: " << dataManagerTest.GetValue(1.5) << std::endl; // Test interpolacji
    std::cout << "Value at time 2.5: " << dataManagerTest.GetValue(2.5) << std::endl; // Test interpolacji
    std::cout << "Value at time 0.5: " << dataManagerTest.GetValue(0.5) << std::endl; // Test wartości poza zakresem
    std::cout << "Value at time 3.5: " << dataManagerTest.GetValue(3.5) << std::endl; // Test wartości poza zakresem

    HttpServer server;
    server.start(API_PORT);

    return app.exec();
}
