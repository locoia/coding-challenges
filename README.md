### General Info
***
Proyect of an API to search a string in all repository of a person in Github. You can search a specific word or phrase in all public files of a person. 

## Technologies
***
A list of technologies used within the project:
* [Python]: Version 3.10
* [Flask]: Version 2.2.2
* [Docker]: Version 20.10

## Installation
***
To run the container you need Docker, open the terminal ad run:
docker run -it -p 7000:9846 locoiaimg 

To access to server use **localhost:7000**


## FAQs
***

1. **We have a limit to coincidences to find?**
Yes, the GitHub API is limited at 100 results without Authper query. 

2. **What happend if my response is empty with a specific user?**
 On some special occasions github marks certain users as "SPAM". When you try to query those users' repositories, the response will return empty. They are only very specific and unlikely cases. in case that happens, try another user.


## ENDPOINTS

**{host}/api/v1/search (POST)**

* BODY:
        {
            "username": "{username}",
            "pattern": "{pattern}"
        }

* RESPONSE:

A Json response with:
* The objets(files) with coincidence with the "Pattern".
* URL of user profile in Github
* Name of the repository
* User name



**{host}/ping (GET)**
return a somple String ("pong")