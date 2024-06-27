FLASK_APP_NAME = app
IMAGE_NAME = booklib_api_img
CONTAINER_NAME = BooklibAPI

DB_CONTAINER_NAME = BooklibDB
DB_NAME = booklibdb
DB_USER = postgres
DB_PASSWORD = password

.PHONY: setup run start stop clean

setup:
    # Build and run the Docker containers
	docker build -t $(IMAGE_NAME) .


run:
	# Run the Docker containers
	#docker run -d --name $(DB_CONTAINER_NAME) -e POSTGRES_DB=$(DB_NAME) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_PASSWORD=$(DB_PASSWORD) 
#	docker run -d --name $(DB_CONTAINER_NAME) -p 5432:5432 -e POSTGRES_PASSWORD=$(DB_PASSWORD) -e postgres_db=$(DB_NAME) -e postgres_user=$(DB_USER) -e postgres_password=$(DB_PASSWORD) postgres:14
	docker run -d --name $(CONTAINER_NAME) -dp 80:5000 -w /app -v "$(CURDIR):/app" $(IMAGE_NAME) 
	#docker run -d --name $(CONTAINER_NAME) -dp 80:5000 -w /app -v "$(CURDIR):/app" --link $(DB_CONTAINER_NAME):postgres $(IMAGE_NAME) 

start:
    # Start the Flask application
	#docker start $(DB_CONTAINER_NAME) 
	docker start $(CONTAINER_NAME) 
	docker exec -it $(CONTAINER_NAME) flask run --host=0.0.0.0

deploy:
	# Deploy and start the application
	#docker run -d --name $(CONTAINER_NAME) -dp 80:5000 -w /app -v "$(CURDIR):/app" --link $(DB_CONTAINER_NAME):postgres $(IMAGE_NAME) sh -c "flask run --host 0.0.0.0"
	

stop:
	# Stop the Docker containers
	docker stop $(CONTAINER_NAME) 
	#$(DB_CONTAINER_NAME)

clean:
	# Remove the Docker containers
	docker rm $(CONTAINER_NAME) #$(DB_CONTAINER_NAME)

	# Remove the Docker image
	docker rmi $(IMAGE_NAME)

