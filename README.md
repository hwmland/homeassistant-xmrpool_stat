# XMR Pool Statistics integration for Home Assistant

![GitHub](https://img.shields.io/github/license/hwmland/homeassistant-xmrpool_stat?style=plastic)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-ltgreen.svg?style=plastic)](https://github.com/custom-components/hacs)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/hwmland/homeassistant-xmrpool_stat?style=plastic)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/hwmland/homeassistant-xmrpool_stat/latest?style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hwmland/homeassistant-xmrpool_stat/Validate%20with%20HACS?label=Validate%20with%20HACS)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hwmland/homeassistant-xmrpool_stat/Validate%20with%20hassfest?label=Validate%20with%20hassfest)

[![buymeacoffee_badge](https://img.shields.io/badge/Donate-Buy%20Me%20a%20Coffee-ff813f?style=plastic)](https://www.buymeacoffee.com/hwmland)

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
