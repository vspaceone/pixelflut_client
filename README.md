# Client for Pixelflut
This is a client for the pixelflut server [https://github.com/defnull/pixelflut](https://github.com/defnull/pixelflut). It got two main features:
+ getting the current visualized image (due to the super slow protocol better only get every fourth pixel and interpolate)
+ setting images in various modes

## Setup the environment

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Testing
```
source venv/bin/activate
```

Note: Not implemented yet.

## Get Image
```
source venv/bin/activate
python src/getimage.py localhost 1234 output.png
```

This download the image from `localhost:1234` and saves it to `output.png`. 

```
usage: getimage.py [-h] [--mode m] [--debug] server port imagefile

This is a Pixelflut Client that receives the current canvas

positional arguments:
  server      The server running Pixelflut
  port        The port of the Pixelflut server
  imagefile   The path to the file to send. Relative or Absolute. Use transparent pixels for pixel that should not be send to the server.

options:
  -h, --help  show this help message and exit
  --mode m    Mode in which the image is send. Use 'random' or 'ordered'.
  --debug     Set the logging to debug
```


## Send Image
```
source venv/bin/activate
python src/pixelflut_client_dump.py images/dog.jpeg localhost 1234
```

This send the image `images/dog.jpeg` to `localhost:1234` in an endless loop. 

```
$ python src/pixelflut_client_dump.py -h
usage: pixelflut_client_dump.py [-h] [--mode m] [--debug] imagefile server port

This is a Pixelflut Client that send images to the server

positional arguments:
  imagefile   The path to the file to send. Relative or Absolute. Use transparent pixels for pixel that should not be send to the server.
  server      The server running Pixelflut
  port        The port of the Pixelflut server

options:
  -h, --help  show this help message and exit
  --mode m    Mode in which the image is send. Use 'random' or 'ordered'.
  --debug     Set the logging to debug
```

Use `-m` or `--mode` set to `random` or `ordered` to define how the image is send. Default is `random` and sends the pixels in random order. `ordered` is sending the pixels line by line.