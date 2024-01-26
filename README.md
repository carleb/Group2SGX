# System Setup Requirement

Instruction:
1. Clone/Download Sample Application code base to your local directory

2. Download and install Docker on your machine  
   a. Download relevant version on: https://www.docker.com/products/docker-desktop/  
   b. Follow the instructions to install the app on your machine  
   c. Verify that docker is properly installed by opening your Terminal (Mac) / Command Prompt (Windows)  
   d. `docker --version`  
   e. `docker-compose --version`


   You should see the version of Docker you have installed  
   <img width="457" alt="image" src="https://github.com/nickman112/sampleapp/assets/74636853/47994adb-9aad-4cd6-9eae-b7600f6c924c">
   
3. Run Docker Desktop locally  
   a. Create Docker Hub Account: https://hub.docker.com/  
   b. Open Docker Desktop and log into docker hub account

   You should see the containers you have (which should be nothing)
    <img width="1273" alt="image" src="https://github.com/nickman112/sampleapp/assets/74636853/e9c1bcd7-edee-40ed-8ed3-17f14a6fbbc3">

4. In your Terminal (Mac) / Command Prompt (Windows) or any other tool  
   a. Change directory to your project `cd sampleapp/download/path`  
   b. Build your Docker Image `docker-compose build`  
   c. Run Docker locally `docker-compose up`

   You should see that the app has started  
   ![image](https://github.com/nickman112/sampleapp/assets/74636853/76ddd8ef-4e87-45f1-8e79-1b2d6fbb5ff8)



6. Open your browser and verify that Sample Application is running locally  
    http://127.0.0.1:8000/

