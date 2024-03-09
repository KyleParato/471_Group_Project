FTP server and client
  gathers all files in directory for both client and server
  txt files used for quick test
  pdf used for medium test
  image files used for big test

How to run: (run program in its folder)
  server
    python3 serv.py <PORTNUM>
  client
    python3 cli.py <servermachine(IP)> <serverport>

Requirments
  ftp> get <file name> (downloads file <file name> from the server)
  ftp> put <filename> (uploads file <file name> to the server)
  ftp> ls(lists files on theserver)
  ftp> quit (disconnects from the server and exits)

  Grading Guideline:
   • Protocol design 10’
   • Program compiles: 5’
   • Correct get command: 25’
   • Correct put command: 25’
   • Correct ls command: 10’
   • Correct format: 5’
   • Correct use of the two connections: 15’
   • README file included: 5

Current issues
  -handling files with spaces in name
  -any sort of packet loss
  -both server and client handle input breakdown(can probably remove some of the servers error checking for the input)
