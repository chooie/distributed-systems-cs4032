Distributed File Server
=======================
# 3 Implemented Services
## Distributed Transparent File Access
A client can create a DistributedFile object which allows it to open a file on
another server and perform operations on it as if it was stored locally:

- open
    - Return a local file handle after downloading the file and opening a local
    one. Read and write operations can be performed on this file.
- close
    - Upload the local file to the file server and close it locally. 
- write
    - Write to the local file.
- read
    - Read the contents of the local file. 

## Directory Service
A client initially sends a request to a directory service. The directory service
then returns a response to direct the client to the appropriate file server:
        
        Direct\n
        <IP address>\n
        <Host>\n

## Replication
