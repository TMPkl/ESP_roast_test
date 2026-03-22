#pragma once

#include <QTcpServer>

class HttpServer : public QTcpServer {
    Q_OBJECT

public:
    explicit HttpServer(QObject *parent = nullptr);
    bool start(quint16 port);

protected:
    void incomingConnection(qintptr socketDescriptor) override;
};