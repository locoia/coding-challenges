# Not implemented parts

- We should implement a proper client for Github gist handling
- searching for the GIST in `is_matching_gist` should be async via asyncio or gevent or other libraries 
- the API logic should be decoupled form the endpoints
- We should use pydantic and dataclasses to enforce typehints
- For handling larger gists I would go wit the following approach. Simple divide the gist under endpoint, so users 
could query that
```
{
  "matches":[
    "download_link_for_gist_1",
    ...,
    ...,
    ...,
    "download_link_for_gist_n
  ],
  "pattern": "\\d\\d\\d\\d",
  "status": "success",
  "username": "user"
}
```

# Architecture
- Can we use a database? What for? SQL or NoSQL?
  - Some Gist file could be large, so for long term analytical purposes I would pick
  some popular SQL db like, MongoDB or PostgreSQL
  - For caching, I would go with Redis and try to reduce the value sizes 

- How can we protect the api from abusing it?
Zero line of defense: enforcing secure coding practices and setting up a secure infra. 
First line is add some authentication with CMS, rate limiting, load balancer,etc 
Second line is using a custom or a popular CDN like Cloudflare 
Third line could be some active monitoring tool which checks in API call given for us. (probably never needed in this case)

- How can we deploy the application in a cloud environment?
Depending on the business need and the current load / team size / cloud provider. From the easiest to the more complex solution:
jenkins, teamcity or circle CI with autodeploy or AWS Opsworks/Chef or  AWS EBS for ad-hoc deployment 

- How can we be sure the application is alive and works as expected when deployed into a cloud environment?
Many ways exist:
  - Add a proper Healtcheck endpoint ot the container
  - Add proper logging and setup alerts for that 
  - Add proper metric or monitoring metrics to the api, collect metrics for each request then,
  store them in ElasticSearch and setup a Grafana/PagerDuty workflow

- Any other topics you may find interesting and/or important to cover
