# StreamsPyTopo
Streams Python topology CI Template development.

Build and submit a Streams application in the IBM Clould.

Simple application that works with the StreamsProxy

** Notes
 - Push the tar up of the toolkits not the toolkit. 
 - Need to pull down the toolkit from github todo this right.
 - Use Maven, not shell.

I've bound the script to the job of a stage using the ${IDS_JOB_NAME}. 
The concept is to have the scripts checked in, 
look for the scripts in the ${HOME}/scripts directory. 

### Credenitals
Credentials (VCAP) are necessary for building and running in the Cloud, 
in these situations where we need expand/decrypt the credential's file. 
Before this code starts,
the credential.py is unzipped from credential.pyz. 
This is the 'Build script' for the buildDeploy job of BuildDeployTopo 
pipline. 
```bash
#!/bin/bash
unzip -P <password> -o credential.pyz
source scripts/${IDS_JOB_NAME}
```
When you generate a new credentials file use following command 
to encode it on your local system and checkin the new .pyz file. 
Updating to a new credential file  

```bash
zip --password <password> -e credential.pyz credential.py
```
Verify that the the credential.py is in .gitignore. 
