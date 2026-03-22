#include "HttpServer.h"

#include <QTcpSocket>
#include <QHostAddress>
#include <QDebug>

HttpServer::HttpServer(QObject *parent) : QTcpServer(parent) {}

bool HttpServer::start(quint16 port) {
    const bool ok = listen(QHostAddress::Any, port);
    if (ok) {
        qDebug() << "Server started on port" << port;
    } else {
        qDebug() << "Server failed to start:" << errorString();
    }
    return ok;
}

void HttpServer::incomingConnection(qintptr socketDescriptor) {
    QTcpSocket *socket = new QTcpSocket(this);
    if (!socket->setSocketDescriptor(socketDescriptor)) {
        socket->deleteLater();
        return;
    }

    connect(socket, &QTcpSocket::readyRead, this, [socket]() {
        const QByteArray data = socket->readAll();

        if (data.startsWith("GET /hello")) {
            static const QByteArray response =
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Hello, World!";
            socket->write(response);
        } else if (data.startsWith("GET /data")) {
            static const QByteArray response =
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Data response";
            
            socket->write(response);
        }

        socket->disconnectFromHost();
    });

    connect(socket, &QTcpSocket::disconnected, socket, &QTcpSocket::deleteLater);
}