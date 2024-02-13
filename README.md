## Description

**Lib used for automation**

- Selenium (assumption is that chrome browser is present on the system, if not the driver in the code needs to be changed to the specific browser)

**Workflow**

- Web page contains a div whose data is fetched dynamically
- XHR call is made to endpoint to receive data filtered based on params
- This div has id `reg-Projects`, req takes a bit to complete 
- Further processing can only take place when the req completes
- The resulting div contains an anchor tag containing a unique id 
- Based on the id on clicking the anchor tag another fetch call is made for data
- A modal opens with a loading state
- Must wait for this fetch to finish as it contains the data of interest
- The modal contains a table with rows containing `td` tags corresponding to the required fields and their values
- Data is extracted and stored as key-value pair in a map that is appended to a list
- The final list is then dumped as json obj to `data.json`


## Run

```
$ python -m venv myenv

# for windows
# myenv/Scripts/activate
$ source myenv/bin/activate

$ pip install -r requirements.txt

$ python scrapper.py
```

Output is stored in *data.json*
