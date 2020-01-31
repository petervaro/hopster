# Hopster's Video Downloading Service

> **Note:** Because of the very short deadline, I had to make shortcuts, i.e.
> the current implementation does not use HTTPS, nor protects the endpoints with
> at least some sort of basic authentication, etc.  Moreover instead of relying
> on some asynchronous scheduler and message broker like `Celery` and SQS it
> uses `hopster.dummy.Task`, as well as instead of using `boto` and the actual
> S3 bucket service, it uses `hopster.dummy.Bucket` to simulate these features.
> I believe the server implementation still demonstrates how the required task
> could potentially be implemented but if the above mentioned shortcuts need to
> be worked on further (e.g. using [`localstack`][103] to emulate AWS services)
> I could work on these later on.  (Also, I only implemented unit level tests,
> higher level ones could be added if required.)


## Dependencies

- Download and install [`ffmpeg`][100]

> **Note:** All of the below instructions assume a UNIX-like environment and a
> POSIX compilant shell, and `python` is version [`3.8+`][101] or an alias of it.

- Create a virtual environment:
  ```bash
  $ python -m venv venv
  $ source ./venv/bin/activate
  ```
- Download and install the `python` dependencies:
  ```bash
  $ pip install --upgrade pip
  # To run the server the release-dependencies are enough to be installed
  $ pip install -r requirements.txt
  # To run the client and/or tests the debug-dependencies need to be installed
  # (which also includes the release dependencies)
  $ pip install -r requirements/debug.txt
  ```

## Run the Server

```bash
$ HOPSTER_SERVER_SECRET_KEY='this-aint-no-secret' python server.py
```

## Run the Client

- Open a new terminal window / tab / region
- Make sure virtual environment is activated:
  ```bash
  $ source ./venv/bin/activate
  ```
- Run the client:
  ```bash
  $ python client.py
  ```

## Tests

```bash
$ python -m pytest -v
```

## Coverage

```bash
# Generate coverage first
$ coverage run -m pytest
# Display coverage information
$ coverage report --include='hopster/*'
```


<!-- LINKS -->
[100]: https://ffmpeg.org/download.html
[101]: https://www.python.org/downloads
[103]: https://github.com/localstack/localstack
