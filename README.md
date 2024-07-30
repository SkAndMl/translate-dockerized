# translate-dockerized

## Table of Contents
- [Model Configuration](#model-configuration)
- [Using the Repo](#using-the-repo)
- [Creating a TAR File](#creating-a-tar-file)
- [Running Docker Image from a TAR File](#running-docker-image-from-a-tar-file)
- [Specs](#specs)

## Model configuration
- `facebook/seamless-m4t-v2-large` is used for translating from **Chinese** to **English**
- The model used or the source and target languages can be changed by changing the variables in the `config.json` file

## Using the repo
1. Install docker using following [link](https://docs.docker.com/engine/install/)
2. Clone the repo
```bash
git clone https://github.com/SkAndMl/translate-dockerized.git 
```
3. cd into the repo
```bash
cd translate-dockerized
```
4. Create the docker container and run the translation api using
```bash
docker-compose up --build
```
5. Verify and use the api at `https://localhost:8000/docs` , the translate api expects a list of sentences along with the source and target languages

## Creating a TAR file
1. Build the image
```bash
docker-compose build
```
2. Tag the image
```bash
docker tag translate-dockerized-translate:latest your_dockerhub_username/translate-dockerized:latest
```
3. Save Docker to a TAR file
```bash
docker save -o translate-dockerized.tar your_dockerhub_username/translate-dockerized:latest
```
## Running docker image from a TAR file
1. Load the image
```bash
docker load -i translate-dockerized.tar
```
2. Run the image
```bash
docker-compose up
```

## Specs
- Expected image size - ~ 19.4GB (obtained from docker hub)
- Expect RAM usage - ~ 9.5GB (SeamlessM4T is 9.4GB)
- Device:
    *  CPU: Apple M2
    *  RAM: 16GB
    *  Storage: 256GB
