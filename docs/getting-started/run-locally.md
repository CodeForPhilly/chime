# Getting Started: Run Locally

This guide aims to provide the easiest and most reliable method for getting a copy of the application running locally.

If you're a developer looking to do heavier work on the application, check out the [Contributing: Application Development](../contributing/app-dev.md) for a more advanced guide covering practical developer workflows.

## Quickstart with Docker

From the root directory of the repository, you should be able to get up and running with one command:

```bash
./script/server
```

This script will:

- Verify that `docker` and `docker-compose` are available on your system
- Initialize `.env` if needed from `.env.example`
- Use `docker-compose up` to build and start an instance of the application as a background daemon
- Print out the URL you can open the app at (usually [http://localhost:8000](http://localhost:8000))

### Running on a Different Port

If you need to run the server on a different, edit the `PORT` option in your `.env` file. You might need to do this if you have something else already running on the default port (8000).

## Updating After Changing Code

If you edit code, or checkout a new branch, the update script will handle all needed steps to refresh your running instance:

```bash
./script/update
```

## Shutdown and Cleanup

From the same directory, run this command to shut down the Docker container and clean up any volumes:

```bash
docker-compose down -v
```
