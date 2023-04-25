import os
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

from parse_creds import *

# The config contains information such as paths and file locations, ports and more...
web_server_config = {
    "serve": {
        "/": "paths/index.html"
    },
    "port": 80,
    "connection_attempts": 60,
};

def add_path(path, file_path):
    web_server_config["serve"].update({path: file_path});
    
def open_socket(ip):
    # Open a socket
    connection = socket.socket();
    connection.bind((ip, 80));
    connection.listen(1);
    return connection;
    
def serve(connection):
    while True:
        client = connection.accept()[0];
        request = client.recv(1024);
        request = str(request);
        try:
            request = request.split()[1];
        except IndexError:
            pass;
        if request in web_server_config["serve"].keys():
            client.send(open(web_server_config["serve"][request]).read());
        client.close();
    
def connect_to_wifi(ssid, password):
    ssid = ssid.strip()
    password = password.strip()
    wlan = network.WLAN(network.STA_IF);
    wlan.active(True);
    print(f"SSID: {ssid}, Password: {password}")
    wlan.connect(ssid, password);
    maximum_attempts = web_server_config["connection_attempts"];
    attempts = 0;
    state = False;
    print('Waiting for connection...');
    while wlan.isconnected() == False:
        if attempts >= maximum_attempts:
            return None;
        
        sleep(1);
        if state:
            pico_led.off();
            state = not state;
        elif not state:
            pico_led.on();
            state = not state;
        attempts += 1;
    ip = wlan.ifconfig()[0];
    return ip;

def start():
    # Get credentials
    credentials = get_credentials("creds.info");
    # Check if we are connected to the internet
    ip = connect_to_wifi(credentials["2.4Ghz"][0], credentials["2.4Ghz"][1]);
    if ip == None:
        print("Failed to connect to the wifi network... Exceeded maximum wait time.");
        pico_led.off();
        return;
    print(f"Connected on: {ip} and port: {web_server_config["port"]}");
    connection = open_socket(ip);
    pico_led.on();
    try:
        serve(connection);
    except KeyboardInterrupt:
        connection.close();
        print("Closed connection.");
        pico_led.off();
    
start();
    
    
    

