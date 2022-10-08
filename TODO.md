## TODOs

* Add a NoSQL DB where we would store the search requests along with the file contents of the relevant results for easier statistics (how many times is certain pattern searched for, or which users gists are most looked at, etc..), I'd suggest ElasticSearch
* Implement api level cache to cache the search results (especially for the big result-sets)
* Limit the api number of requestsset to 100 requests per 100 seconds per user or less to avoid abusive behavior
* Add logging mechanisms (possibly implement a custom logger based on [structlog](https://www.structlog.org/en/stable/))
* Add monitoring mechanisms (like datadog with performance and error monitoring), alerting (pager duty or similar) to constantly be aware of the current state of application or to respond in case of any undesired behavior
* In order to monitor the application status the liveliness probe and self restarting mechanisms should be put into place
* With the requests information in the database it might be possible to create a data model that might predict the possible searches according to the searchers preferences (e.g. if the user is often searching for the data related to a certain programming language or a framework, a predictability model might be used to alleviate the search effort or to even use some of the already saved responses to serve the user faster)
* The application could be deployed on the kubernetes cluster behind a load balancer with a preset number of pods that would increase when the load exceeds a certain set limits
* Also, with the stored search data it would be quite feasible to use it as part of some statistics for any interested party. And the best part is, data collection is anonymous, since there's no record of the request maker nor the purpose of their search.