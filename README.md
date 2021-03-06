# myProject

This project is about creating a docker container on RHEL 7.7 to setup and run Tomcat web sever with a sample web application deployed listening on port 8080

Layout
======

	test_url.py
	conftest.py
	Dockerfile
	tomcat_sample_setup.yml
	hosts
	
- Pytest script
```
test_url.py
conftest.py
```

  Script test_url.py checks whether accessing an URL is successfull or not through an HTTP GET  
  File conftest.py defines fixtures for the parameters of the test_url.py script

  Script can be executed individually as a separate command for any URL to check  
    It accepts 2 arguments --url and --status  
    If --url is not specified it defaults to "http://localhost:8080/sample"  
    If --status is not specified it defaults to "found"  
    If --status is not in [found, not_found] the test will fail  

  
	py.test test_url.py --tb=no --url <URL_to_check> --status found|not_found

  Example:  
  ```
    py.test test_url.py --tb=no --url "http://localhost:8080/sample" --status "found"  
    py.test test_url.py --tb=no --url "http://localhost:8080/sample" --status "not_found"
```

- Dockerfile

  This file contains the set of docker instructions :  
    * To build an image of Tomcat (pick up version 9.0)  
    * To add a sample web application (pick up latest version of "sample" war file) into the web server directory of Tomcat so it is automatically deployed at runtime  
    * To expose web server to listen to port 8080  
    * To run Tomcat web server  


- tomcat_sample_setup.yml

  This YAML file is the ansible playbook that automates the following configuration steps in this order :  

  * Check whether sample web application is accessible at "http://localhost:8080/sample" calling Pytest script test_url.py  
  * If above URL is not reachable :  
        => builds docker image using Dockerfile file named samplewebapp that basically enables tomcat and sample web app to deploy  
        => runs docker container named samplewebapp to run built image samplewebapp and map TCP port 8080 in the container to port 8080 on the docker host  
  * Check whether sample web application deployed in Tomcat is accessible at "http://localhost:8080/sample" calling Pytest script test_url.py


- hosts 

  Ansible inventory file required to operate playbook on localhost  
  


Requirements
============

Setup an host running RHEL 7.7 with following setup (execute commands as non root user) :
  
  Example 
  ```
  mkdir -p ~/myProject ; cd ~/myProject
  ```
  
  * Python3 and Pytest :
```    
  sudo yum install python3-pip
  pip3 install --user  pytest
``` 
  * Docker :  
```
  Follow setup at https://docs.docker.com/ee/docker-ee/rhel/ or https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html-single/getting_started_with_containers/index#getting_docker_in_rhel_7
  pip3 install --user docker
  sudo groupadd docker
  sudo gpasswd -a $USER docker
  newgrp docker
```
  * Ansible for Python3 :
```
  pip3 install --user ansible
```


How to run 
==========

From you host, clone or download git repository https://github.com/jjfr38760/myProject.git

Example :
```
 cd ~
 sudo yum install git
 git init
 git config --global user.email "<your email>"
 git config --global user.name "<your name>"
 git clone https://github.com/jjfr38760/myProject.git
 cd ~/myProject
```


(execute commands as non root user)
```
ansible-playbook -i hosts tomcat_sample_setup.yml
```

Note1:

  The ansible playbook is idempotent meaning it can be run multiple times without failures  
  If sample application is already accessible it assumes the process to create related docker image and container has been run  
  If sample application is not accessible it will go to the process of creating related docker image and container 


Note2 : 

  To check sample app is [not] running you can run individual script separately 

    py.test test_url.py --tb=no --url "http://localhost:8080/sample" --status "found"
    py.test test_url.py --tb=no --url "http://localhost:8080/sample" --status "not_found"



How to cleanup
==============
  
  (execute commands as non root user)
  ```
  docker container ps
  docker container stop samplewebapp
  docker container rm samplewebapp

  docker image ls
  docker image rm samplewebapp tomcat:9.0
 ``` 
  
  
  
  
  Issues
  ======
  
  - It looks like there is intermittent issue while running Ansible playbook in the scenario of docker container and image to build from scratch 
    * In the playbook final step of call to script test_url.py to check sample app is reachable, it will fail hitting exception reason "Presumably, the server closed the connection before sending a valid response"  
    * Issue does not hurt as in this scenario it is just final double check not mandatory  
    * At this final stage, sample application does hit successfully which can be cross-checked by running the Pytest script individually outside playbook  
    * At this time, screening various forums on topic/issue it looks like a known bug in lib urllib3 with no clear workaround I could found  
      => using different methods to connect and trigger HTTP GET did not fix it  
      => both using urllib or urllib3 duplicates same issue, see other flavor in file test_url_lib3.py)  
      => adding sleep time after Connect / GET calls did not fix it  
      => plan to raise an hand in the community to share on that issue  
