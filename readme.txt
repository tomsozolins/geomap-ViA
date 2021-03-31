Create 2x free-tier oracle instances in same Oracle VCN subnet:
docker-node1
docker-node2
more info - see 'oracle free instance setup'
-------------------------
Allow ports on Oracle VCN subnet:
2377/tcp
2376/tcp
7946/tcp
7946/udp
4789/udp
-------------------------
Update both instances:
# apt update
# apt upgrade
-------------------------
Docker installation - https://docs.docker.com/engine/install/ubuntu/
Docker compose install - apt install docker-compose
-------------------------
Configure firewalld on both instances (else commmunication won't work):
# sudo apt-get install firewalld
# sudo systemctl enable firewalld
# sudo systemctl start firewalld
# sudo firewall-cmd --zone=public --add-port=2377/tcp --permanent
# sudo firewall-cmd --zone=public --add-port=2376/tcp --permanent
# sudo firewall-cmd --zone=public --add-port=7946/tcp --permanent
# sudo firewall-cmd --zone=public --add-port=7946/udp --permanent
# sudo firewall-cmd --zone=public --add-port=4789/udp --permanent
# sudo firewall-cmd --reload
-------------------------
Setup Oracle Load Balancer - see 'oracle load balancer setup' dir
-------------------------
Docker Swarm setup
docker-node1:
# docker swarm init --advertise-addr <instance_private_ip>
Get manager token for node2:
# docker swarm join-token manager
docker-node2:
# docker swarm join --token <token> <instance_private_ip>:2377
Test load balancer:
# docker node update --availability drain docker-node2

# docker node update --label-add node1=true docker-node1
# docker node update --label-add node2=true docker-node2
------------------------
Apex database and app setup (sql files located in 'apex_sql')

Manage Users and Groups -> Create User -> 'geoapi' -> Group Assignments -> Restful Services

SQL Workshop -> SQL Scripts -> Upload -> 1_geomap.sql -> Run
SQL Workshop -> SQL Scripts -> Upload -> 2_restful_service_geojson.sql -> Run
SQL Workshop -> SQL Scripts -> Upload -> 3_restful_service_geoapi.sql -> Run

App Builder -> Import -> 4_geomap_apex_app.sql
-------------------------
Change secrets to your desired values in 'secrets' directory.
Change 'leaflet_data/index.js' Geojson url to your apex workspace url.
-------------------------
Clone project to both nodes

# mkdir /app ; \
cd /app ; \
rm -rf geomap ; \ 
git clone https://github.com/tomsozolins/geomap.git ; \
 cd /app/geomap
-------------------------
Zabbix server installation
# docker stack deploy --compose-file=docker-compose-zabbix.yaml zabbix_stack
-------------------------
Build image on both nodes

# docker-compose -f docker-compose-geomap.yaml build

# docker stack deploy --compose-file=docker-compose-geomap.yaml geomap_stack

Access Leaflet on - http://<load-balancer-ip>:8081

