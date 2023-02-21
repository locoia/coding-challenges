Database? It does not seem likely to have a need for a database, if the purpose of the api is to just serve data.
if however there is a need to cache the data, if, for example, while handling large gist files, there is a significant delay, it could be saved.
I think noSQL would fit the best, due to arbitrary nature of gist files. SQL would require more strict structure (even though it can save data in either json, byte, etc, column)


To prevent API abuse, it would need at least rate limiter functionality (for example, middleware).
by recording device data and IP from where request is coming from, it's possible to add rate limiting. if rate limit is exceeded - reject requests early

Deploying to cloud. It is possible to use dockerized version of this project and send to a Kubernetes cluster.
or without it - deploy to cloud servers, that has load balancers for traffic redirection towards various instances of the app.
usually it's done through CI/CD pipelines, like, Jenkins to do the deployment.

Seeing if service is alive in a cloud? It can be done in a few ways. 
obvious one would be to try and access the API and see if it is alive.
another - access the logs of both CI/CD pipelines and/or service that deploys the service to the cloud. could be for example Jenkins tool used to deploy it.



