## ToDo Items

* Can we use a database? What for? SQL or NoSQL?
  * Implemented SQL DB for Caching uses
* How can we protect the api from abusing it?
  * Using token:
    * Authorize trusted identities and then manage access to services and resources by using tokens allocated to those connections individually.
  * Using an API gateway:
    * API gateways act as the dominant point of enforcement for API traffic. A gateway will allow you to authenticate traffic as well as can be used to govern how APIs are used.
  * Using quotas and throttling:
    * Keep quotas on how often API can be requested and track its use. More API calls may indicate that API is being misused. Establish rules for throttling to defend your APIs from spikes and Denial-of-Service strikes.
  * Using encryption and signatures:
    * Encrypt data using a method such as TLS. Demand signatures to ensure that the right users are decrypting and altering data.
  * Keep the operating system, drivers, network and API components updated to the latest level. Understand the intracies of all component operation and determine where possible weak points are in the APIs. Use sniffers to discover security issues and track data leakages.  
* How can we deploy the application in a cloud environment?
  * To deploy our API to the AWS cloud using open source tools to make deployment easier. First we need to 
  * containerize our Flask application using Docker, and deploy it to Amazon Elastic Container Service (Amazon ECS). 
  * To automare this deployment of AWS services we can use Terraform, an open source infrastructure as code software tool. 
* How can we be sure the application is alive and works as expected when deployed into a cloud environment?
  * We can perform basic automated testing of the API using a functional testing tool like SoapUI to confirm viability.
* Any other topics you may find interesting and/or important to cover
