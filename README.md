# About

Testing cross domain login by setting third party cookies via XHR.  
And, by redirect chain.

# Quickstart

    python server.py #needs Flask

Then, go to: http://local.example:5000/?sites=local.example.com:5000,local.example2.com:5000,local.example3.com:5000


Assumes dns or hosts file is set up so that local.example.com, local.example2.com, ... etc point to the same ip/application.




