# XMR Pool Statistics integration for Home Assistant

![GitHub](https://img.shields.io/github/license/hwmland/homeassistant-xmrpool_stat?style=plastic)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Sensors dowloading some statistic data from https://web.xmrpool.eu/
It supports following sensors currently:

- Balance - your current balance on this pool.
- Hashrate - current hashrate. Suitable for using on visualisation.
- Hashrate Raw - current hashrate, but fixed on H/s, better suitable for trending.

---

Perhaps you want to <a href="https://www.buymeacoffee.com/hwmland" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a> or send me some monero donation to **41eUvPgskizFBRJ16TMnvrA2Bph5aqKQFjLAXQM8KJoaAWc2XrT3Fsn6eNBKX1ZSjxCwhksykDYGLcQojoJZkwe2Ud6C8vB** if you like this project.

# Install integration

This integration is distributed using [HACS](https://hacs.xyz/).
Alternatively you can install it manually by copying the contents of `custom_components/xmrpool_stat/` to `<your config dir>/custom_components/xmrpool_stat/`.

# Setup integration

Add new `XMR Pool Statistics` instance configuring name and monero wallet address.