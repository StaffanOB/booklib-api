
    port_server=5000
    port_ex=80
    image_name=booklib_api_img
    container_name=BooklibAPI 


    #docker build -t flask-smorest-api .
    #docker run -dp $port_ex:$port_server -w /app -v "$PWD:/app" $image_name
docker run -d --name $container_name -dp $port_ex:$port_server -w /app -v "$(pwd):/app" $image_name sh -c "flask run --host 0.0.0.0"
#docker run --name $container_name-queue -w /app $image_name sh -c "rq worker -u rediss://red-cm2mioi1hbls73fqc35g:YFyYOAgLnwsltYk6yBOrtNzYowTvDlTV@frankfurt-redis.render.com:6379 emails"
