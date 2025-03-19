# OnionShare(-Docker)

```
docker run \
   -v $HOME/Dropbox:/var/tmp/onionshare \
   -v /volume2/docker/onionshare:/etc/onionshare \
   --name onionshare \
   # -u me:users \
   -d ghcr.io/tcyrus/onionshare:main
```

## Notes

### Onion v3 Keys

`service_id` is the onion address afaik ([spec](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html))

`private_key` appears to be 64 bytes, which means it's the "expanded" key. Onion v3 uses weird key blinding / expansion (I'm having a headache thinking about it) ([spec](https://spec.torproject.org/rend-spec/keyblinding-scheme.html)).

The cryptography is weird, but you can re-derive the public key from the service_id.

You cannot derive the public key from the "expanded" private key because of the key blinding.

I have scripts that convert `hs_ed25519_secret_key` and `hs_ed25519_public_key` files into partial Onionshare config (and the reverse)

### Synology DSM

If you're running Docker on Synology and you want to run the container rootless, then you need to make sure that your bind mounts have explicit user permissions via the Permission Inspector (GUI).
