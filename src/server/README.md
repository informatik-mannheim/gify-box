# Server Setup

This document describes the configuration of the server for the GifyBox.

## Additional Packages

The server part uses PHP and a web server, normally Apache. We don't provide installation instructions here.

Required apache setup:
* Add Server name to /etc/apache2/apache2.conf
* Set AllowOverride All for the /var/www directory at the bottom of /etc/apache2/apache2.conf
* Enable Rewrite Mod for Apache2 with ```a2enmod rewrite```

Install the following additional packages:

* ffmpeg

```console
sudo apt update
sudo apt install ffmpeg
```

## Install the Software
 
Install the software from the GitHub repository.

```console
cd
git clone https://github.com/informatik-mannheim/gify-box.git
```

Copy the directory `src/server` to the web root of your server, e.g. `/var/www/gifybox`. Configure the web server to serve the directory.


## Upload directory

Ensure that the `uploads` directory is writeable by the web server. Therefore execute the following command:

```console
cd /var/www/gifybox
sudo chown www-data uploads
sudo chmod ug+rwx uploads
```

# Useful Links
[How to generate ssl certificate for apache2 with certbot](https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-20-04)
