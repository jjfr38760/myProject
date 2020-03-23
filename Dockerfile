FROM tomcat:9.0
LABEL maintainer="azureuser@myRHVM"
ADD https://tomcat.apache.org/tomcat-9.0-doc/appdev/sample/sample.war /usr/local/tomcat/webapps/
EXPOSE 8080
CMD ["catalina.sh", "run"]
