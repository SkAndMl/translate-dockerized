# translate-dockerized

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
