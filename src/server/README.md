# Server Setup

This document describes the configuration of the server for the GifyBox.

## Additional Packages

The server part uses PHP and a web server, normally Apache. We don't provide installation instructions here.

Install the following additional packages:

* php-imagick
* imagemagick

```console
$ sudo apt update
$ sudo apt install php-imagick imagemagick
```

## Install the Software

Install the software from the GitHub repository.

```console
$ cd
$ git clone https://github.com/informatik-mannheim/gify-box.git
```

Copy the directory `src/server` to the web root of your server, e.g. `/var/www/gifybox`. Configure the web server to serve the directory.


## Upload directory

Ensure that the `uploads` directory is writeable by the web server. Therefore execute the following command:

```console
$ cd /var/www/gifybox
$ sudo chown www-data uploads
$ sudo chmod ug+rwx uplods
```
