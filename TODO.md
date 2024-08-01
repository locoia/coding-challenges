# Questions and Improvements

#### 1. Can we use a database? What for? SQL or NoSQL?
Yes, we can use a database. 
- For repeated queries, we could implement a caching layer using Redis 
(or an in-memory cache) instead of using a full database.
- We could store previously fetched gists in a proper database, minimizing
calls to an external, third-party API. Of course this would still mean
making a database call over a network, but should be "faster" for users 
who have run previous queries.
- If the application allows users save gists or manage the results, then
a database could be necessary.
- If we need to run some analysis on the results over time, a database 
would be necessary.

The choice of SQL or NoSQL depends on the data being saved. 

##### SQL (PostgreSQL, MySQL): 
- Structured data (e.g. Gist attributes like title, description, URL, etc).
- If there's complex querying or relationships (e.g. user profiles, gist metadata).

##### NoSQL (MongoDB):
- Unstructured, or semi-structured data
- If we need a flexible schema (e.g. users gist content structure can be very different).

#### 2. How can we protect the api from abusing it?
There are a couple of ways we can protect the API from abuse:

- **Rate Limit**: Impose a limit on the number of requests a user can make over a period
of time.
- **API Key**: Make users required to provide an API key when making requests to identify
the user.
- **Implement CORS**: Specify domains that are allowed to access the API.
- **Input Validation**: Validate user input to prevent certain attacks like SQL-injection
- **Use HTTPS**: Using this encrypts the data when in transit, avoiding man-in-the-middle
attacks.
- **Logging and Monitoring**: This can help detect patterns that might indicate something 
fishy.

#### 3. How can we deploy the application in a cloud environment?
The application can be deployed to cloud environments like Heroku, AWS (Elastic Beanstalk),
or Google Cloud Platform

To deploy to AWS ElasticBeanstalk:

- Install AWS CLI and EB CLI (Elastic Beanstalk CLI)
- Run aws configure and follow the prompt
- We would need a Procfile (and likely a requirements.txt file)
- Initialize elastic beanstalk using `eb init`
- Create an environment using `eb create`
- Deploy the application using `eb deploy`

Environment variables would need to be added on the platform (e.g. API keys). Some platforms
(e.g. AWS) also offer monitoring (Cloud watch).

#### 4. How can we be sure the application is alive and works as expected when deployed into a cloud environment?
To be sure the application is alive and works as expected we can implement monitoring and testing

- We already have a `/ping` endpoint that can act as a healthcheck endpoint. The provider can use
this endpoint for health checks (Elastic Beanstalk settings has a means to configure this)
- We can implement logging to capture logs (errors, warnings and other important events)
- There are other monitoring tools like Datadog, Sentry, New relic, etc; that help track application
performance, error rates, availability, etc. We can setup alerts when certain thresholds are crossed.
- Automated testing. Tests have been added, but we can also setup CI/CD pipelines to run tests during 
deployments and roll-back deployments if tests fail

#### 5. Any other topics you may find interesting and/or important to cover
- API Documentation: Use tools like Swagger to document the API endpoints
- Code coverage. Ensure a robust testing of the codebase, and maintain high code coverage
- Pre-commit/Post-commit hook(s) to run code quality checks and tests before merging code