#                                          
# #    #  ####  #####   ##   #        ##   
# #    # #    #   #    #  #  #       #  #  
# #    # #    #   #   #    # #      #    # 
# #    # #    #   #   ###### #      ###### 
#  #  #  #    #   #   #    # #      #    # 
#   ##    ####    #   #    # ###### #    # 
# Votala is the definitive solution for online polling.
# This is the file that states the database schema the entire system.
# Author : Lucas Sousa Silva.

launch_production:
	docker compose -p votala \
		-f docker_configuration/votala.production.docker-compose.yaml \
		--env-file docker_configuration/production.env \
		up --build

launch_development:
	docker compose -p votala \
		-f docker_configuration/votala.development.docker-compose.yaml \
		--env-file docker_configuration/development.env \
		up --build

prettify_source:
	black .; isort votala/*

