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

### Onimages

Onimages are designed to run applications in proxy mode, which means that they don't work with how OnionShare works.

OnionShare calls `create_ephemeral_hidden_service`, which sends an [`ADD_ONION`](https://spec.torproject.org/control-spec/commands.html#add_onion) command with the private key (or a new key is generated). There's no way to get the tor daemon to load in the key outside of the process (as of writing).

### Onion v3 Keys

`service_id` is the onion address without the `".onion"` TLD ([spec](https://spec.torproject.org/rend-spec/encoding-onion-addresses.html))

You can derive the public key from the onion address (`service_id`) and vice versa.

`private_key` is the base64 "expanded" private key. Tor uses "expanded" private keys instead of the actual private keys. The process of "expanding" the private key isn't reversible (involves hashing and bit clamping). You can't derive the public key from the "expanded" private key.

I have scripts that convert `hs_ed25519_secret_key` and `hs_ed25519_public_key` files into partial OnionShare config (and vice versa).

### Synology DSM

If you're running Docker on Synology and you want to run the container rootless, then you need to make sure that your bind mounts have explicit user permissions via the Permission Inspector (GUI).
