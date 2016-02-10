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
A client initially sends a request for a file to a directory service: 

        Directory\n
        Connect\n
        <File Name>\n

The directory service then returns a response to direct the client to the 
appropriate file server:
        
        Directory\n
        Direct\n
        <Host Address>\n
        <Port>\n
        <File Name>\n

## Replication
A file server can be a primary or a replica. Each primary has associated
replicas which it writes its contents to. When requesting a file from a
directory server, the directory server can direct the client to a primary or
one of its replicas. All writes are still done at the primary.

## Lock Service
When a client opens a distributed file, it queries the lock service to see if 
the file is unlocked and thus available to be opened. The lock service contains 
an array of files that are all currently locked in the system. 

If the lock service receives a request for a locked file, the lock service sends
the client a denial message and so the client's attempt to open the file fails. 
Alternatively, the client could poll the lock service intermittently until the 
file is unlocked. However, this could introduce deadlock to the system.

Otherwise, the service accepts the request and stores the file name.
The client will then proceed with downloading the file from a primary via the
directory service.

When a client closes a file, it uploads the file to the associated primary via
the directory server. The primary then sends the lock service a message to
unlock the file.
