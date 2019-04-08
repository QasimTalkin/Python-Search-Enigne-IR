### Set up virtual env
On mac type 
> pip install virtualenv
 virtualenv search_ve -p python3.7
 source search_ve/bin/activate

here "search_ve" is my virtual environment. 

### Install project dependencies
>$pip install -r requirements.txt












## learn
#### we used a templating language. Jinja2 comes with Flask, so there is no extra setup needed.
* A templating language works in conjunction with a web server. It takes the output of your Python scripts (the back-end code), and makes it easy to output to the user using HTML (the front-end). It’s important to note that templates should not be used for logic! Keep the logic in Python, and use templates only for displaying the data. It gets very messy if you start trying to get complex with the template.