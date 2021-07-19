# Aluno: Bruno Gomes de Azevedo


import time
import sys
import socket

host = "127.0.0.1" #set to server ip or hostname
port = 30000

pings = 5
timeout = 4
sleep_time = 1
message_bytes = 30

min_ping = 999999
max_ping = 0
ping_count = 0
ping_received = 0
avg_ping = 0

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(timeout)



def show_summary():
    total_time = (time.time() - time_start - 1) * 1000

    print('---  Ping e Pong com o servidor %s ---' % (host))
    print('%d packets transmitted, %d received, %0.0f%% packet loss, time %0.0fms' % (ping_count, ping_received, (ping_count - ping_received) / ping_count * 100, total_time))
    print('rtt min/avg/max/mdev = %0.3f/%0.3f/%0.3f/%0.3f ms' % (min_ping, avg_ping / ping_count, max_ping, max_ping - min_ping))
    sys.exit()

time_start = time.time()

for seq in range(pings):
    try:
        msg = 'ping - envio %d' %seq
        message =  msg.encode("utf-8")
        if len(message) <= 30:
            clientSocket.sendto(message, (host, port))
            start = time.time()
            data, server = clientSocket.recvfrom(2048)
            end = time.time()
            vFinal = (end - start) * 1000
            if vFinal < min_ping: min_ping = vFinal
            if vFinal > max_ping: max_ping = vFinal
            ping_count += 1
            ping_received += 1
            avg_ping += vFinal
            print('recebido %s bytes from %s udp_seq=%d time=%0.1f ms' % (data.decode(), host, seq, vFinal))
            time.sleep(sleep_time)
        else: 
            print('Proibido o envio acima de 30 caracteres!')
    except socket.timeout as e:
        print('Dado = %d REQUEST TIMED OUT' % (seq))
    except KeyboardInterrupt:
        show_summary()

show_summary()