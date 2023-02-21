1. Can we use a database? What for? SQL or NoSQL?
We could use a database for caching data. For this purpose, we could use Redis.
Potentially we could store search results for further analytical analysis. I would use something like MongoDB
2. How can we protect the api from abusing it?
We could protect our API by putting it in behind the DNS, e.g. Cloudflare
3. How can we deploy the application in a cloud environment?
It Depends on the requirements, but for example, we could use AWS CodeBuild or Jenkins, etc.
4. How can we be sure the application is alive and works as expected when deployed into a cloud environment?
After it is deployed we could use the system endpoint (in our case "/ping") to ensure that the API is alive.
Additionally, we could create a file with the API version and the system endpoint would return the version string. 
In such a case, we could ensure what API version is deployed on the production environment.
5. Any other topics you may find interesting and/or important to cover
Potentially we could solve the bottleneck of our API (requests to GitHub) using async requests.