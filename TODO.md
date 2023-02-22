
    - Can we use a database? What for? SQL or NoSQL?

    No CLOUD: WE can use a database (SQL) to have a log of queries and we can save the results to posterior data analysis. Another option has a kind of cache(but in this case isn´t useful, because isn´t an abnormal situation that a user makes a few times the same query). Another utility is security, I will speak about that in this document.

    CLOUD: Isn´t necessary to use a database, but if you want to save each response of the GitHub API you could implement one(the same as without the cloud)
-------------------------------------------------

    - How can we protect the API from abusing it?

    No Cloud: We could use an AUTH system. Another option is to save in a DB for each service request and create a limit of queries per day limited for IP(it is not recommendable, we have better options like the cloud). we could do this with the middleware but I'm speaking from my experience with Django, I don't know if we can with flask.

    Cloud: We can use services similar to ASS(Amazon Shield Satndart) to protect against DDos attacks, in the cloud we can put rules about the quantity connection per hour we will allow.

-------------------------------------------
    - How can we deploy the application in a cloud environment? 
    YES !! :D  and we could do it in the free tier(we don't need to pay). We could use de S3 service to save the files, we can use Lambda to control errors or bad requests, and the SNS services to warn us (via mail, or SMS) when the system has problems. In addition, we could configure the ELASTIC LOAD BALANCING service to balance the traffic between our Dockers containers that will be running in AMAZON ELASTIC CONTAINER SERVERS. 

    We can do a lot in the cloud! :)

-------------------------------------------
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment? We could use the ACW(Amazon)

    As explained in the last point, we could use a few services to have a notification in real-time in our cellphones or mail when the system has any problems. And we can make an asynchronous process to confirm the correct function of the API each x time.


--------------------------------------------

    - Any other topics you may find interesting and/or important to cover

    We have more APIs in GitHub to use for this objective. I choose the most simple because is enough to meet the requested results but we could improve this system by showing a piece of code where we find the coincidence of searched text.
    I only show a few fields of each result to see a more ordered interface, but if you want more information we can do it in a few lines more of code.

    
    P.S.: But we need to be realistic, this API doesn't need all things that I told you about. But in realistic projects, I highly recommend the cloud. 