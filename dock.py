import sys
import shutil

if len(sys.argv) == 1:
    service_endpoint = input("What's your service endpoint? Examples: 'my_app/frontend' or 'react_app/home'?\n>>>")
    docker_compose_version = input("What's your docker compose version (x.x format, e.g. v2.12.2 -> '2.12')? Run 'docker compose version' to know it.\n>>>")
    host_port = input("What required external (HOST) port to use? If you will deploy on Gcloud Run, use 8080.\n>>>")
    container_port = input("What's the EXPOSED Docker container port?\n>>>")
    server_port = input("What's the production web server port? E.g. nginx uses port 80.\n>>>")
    docker_image_name = input("Choose a Docker image name:\n>>>")
    gcloud_project_id = input("What's your Gcloud project ID? Run 'gcloud projects list' to list all GCloud projects.\n>>>")
    gcloud_run_service = input("What's your Cloud run service name? Run 'gcloud run services list' to list all cloud run services.\n>>>")
    with open(".templates/dock.settings", "w") as file:
        file.write("service_endpoint="+service_endpoint+"\n"+\
                "docker_compose_version="+docker_compose_version+"\n"+\
                    "host_port="+host_port+"\n"+\
                    "container_port="+container_port+"\n"+\
                    "server_port="+server_port+"\n"+\
                    "docker_image_name="+docker_image_name+"\n"+\
                    "gcloud_project_id="+gcloud_project_id+"\n"+\
                    "gcloud_run_service="+gcloud_run_service)
else:
    with open(".templates/dock.settings", "r") as file:
        content = file.read().split("\n")
        for value in content:
            line = value.split("=")
            if line[0] == "service_endpoint":
                service_endpoint = line[1]
            if line[0] == "docker_compose_version":
                docker_compose_version = line[1]
            if line[0] == "host_port":
                host_port = line[1]
            if line[0] == "container_port":
                container_port = line[1]
            if line[0] == "server_port":
                server_port = line[1]
            if line[0] == "docker_image_name":
                docker_image_name = line[1]
            if line[0] == "gcloud_project_id":
                gcloud_project_id = line[1]
            if line[0] == "gcloud_run_service":
                gcloud_run_service = line[1]   
               



with open(".templates/cloudbuild.yaml", "r") as file:
    content = file.read()
    content = content.replace("<service-endpoint>", service_endpoint)

with open("cloudbuild.yaml","w") as file:
    file.write(content)


with open(".templates/docker-compose-dev.yaml", "r") as file:
    content = file.read()
    content = content.replace("<docker-compose-version>",docker_compose_version)
    content = content.replace("<host-port>", host_port)
    content = content.replace("<container-port>", container_port)
with open("docker-compose-dev.yaml","w") as file:
    file.write(content)


with open(".templates/docker-compose-prod.yaml", "r") as file:
    content = file.read()
    content = content.replace("<docker-compose-version>",docker_compose_version)
    content = content.replace("<host-port>", host_port)
    content = content.replace("<server-port>", server_port)
with open("docker-compose-prod.yaml","w") as file:
    file.write(content)

shutil.copyfile(".templates/Dockerfile.prod", "Dockerfile.prod")
shutil.copyfile(".templates/Dockerfile.dev", "Dockerfile.dev")
shutil.copyfile(".templates/.dockerignore", ".dockerignore")

with open(".templates/gcloud_run_instructions.txt", "w") as file:
    file.write("docker buildx build -f Dockerfile.prod --platform linux/amd64 -t "+docker_image_name+" .\n"+\
               "docker tag "+docker_image_name+" gcr.io/"+gcloud_project_id+"/"+service_endpoint+"\n"+\
               "docker push gcr.io/"+gcloud_project_id+"/"+service_endpoint+"\n"+\
               "gcloud builds submit\n"+\
               "gcloud run deploy "+gcloud_run_service+" --image gcr.io/"+gcloud_project_id+"/"+service_endpoint+" --region=us-central1 --port="+server_port
        )





