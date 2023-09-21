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

launch:
	docker compose -p votala -f docker_configuration/votala.docker-compose.yaml up --build

prettify_source:
	black .; isort votala/*

