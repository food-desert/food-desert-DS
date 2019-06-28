## Readme.md for Docker Creation files.

(As github ignores some of the files used to create docker images, they have been conviently placed in a zip file for you.)
The commands to build and run are as follows.
(Unzip food_desert to a directory for building the docker image.)
from the directory run the commands 

docker -t build food-desert .
docker run -d -P food-desert
docker ps
(Here you will have to get the port where you need to point your browser to it will be 0.0.0.0:portnumber)
Bring up a web browser to the http://localhost:portnumber

Jason Murph
