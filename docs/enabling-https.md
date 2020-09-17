## Enabling HTTPS
By default, TorchServe accepts unencrypted HTTP requests, which is not optimal for privacy reasons, when sending real-life images over unencrypted HTTP. Because of this, we recommend configuring TorchServe to use HTTPS. You can provide your own SSL certificate, or create a self-signed one using [TorchServe's guide](https://pytorch.org/serve/configuration.html#id3).
