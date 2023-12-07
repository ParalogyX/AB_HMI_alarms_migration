# AB_HMI_alarms_migration
## Script to migrate alarms from old to new Rockwell View Designer

To perform conversion, replace filename in line 37 to the actual xml with Original (old version) alarms. Xml should be exported from old version of View Designer.
Download all files (the script, the requirements.txt and the exported xml) in the same folder. Create Python or Conda virtual environment (e.g. https://docs.python.org/3/library/venv.html), activate it and install the libraries with "pip install -r requirements.txt". 
Run the script in the environment and it will produce the file with the name "new_alarms_generated.xml" which can be used for importing "new HMI" alarms.
