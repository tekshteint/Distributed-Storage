# Distributed Storage
 
### Project structure
  * Client can upload files to Master node through PUT request
    * Client will recieve ID for a file and can retrieve it with that key

  * Master needs two parts:
    * Upload files via put request from client
        * This will split the file into X portions where X = number of storageNodes
        * Generate an ID for a file
    * Retrieve files via GET request
        * This request needs the file ID

  
