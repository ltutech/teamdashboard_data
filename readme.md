# Team Dashboard data

This is an rough JSON api for Team Dashboard to plug different api on it.

## How to:

+ Install Team Dashboard
+ Configure team dashboard data python/config.py
+ Create your env (virtualenv env)
+ Source it (source env/bin/activate)
+ Setup your environment (python setup.py develop)
+ Run it (python main.py)
+ In your dashboard interface add a graph widget
+ Select http_proxy for the source
+ Put the team dashboard data url in proxy url like this: http://127.0.0.1:9990/getOpenByProduct/?engine=python/ltu-clients,ltuProduction&cloud=python/ltu-clients
+ Specify the targets, in our example: engine, cloud

## Gerrit Module

+ Graph or count reviews on gerrit.


### Link to the dashboard tool

[Team Dashboard Homepage](http://fdietz.github.io/team_dashboard/)


### List of available methos

*   /gerrit?user=YOUR_USER
    > nb reviews for a user
*   /getOpenByProduct/?product1=repo1,repo2&product2=repo1,repo3
    > get one graph by product

### Example
![Alt text](/images/gerrit_example.jpg)
