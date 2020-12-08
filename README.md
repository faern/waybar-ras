# waybar-ras (Reliability, Availability and Serviceability) plugin

A [Waybar](https://github.com/Alexays/Waybar) plugin showing the error status as reported by the
`ras-mc-ctl` command (successor to `mcelog`).

Currently this only supports monitoring the number of correctable and uncorrectable memory
errors that has occured in your ECC RAM.

## Installation and configuration

1.  Clone this repo into the waybar modules directory

    ```bash
    cd ~/.config/waybar/modules/
    git clone https://github.com/faern/waybar-ras
    ```

1. Configure waybar (`~/.config/waybar/config`):

    ```json
    "custom/ras": {
        "format": "{}",
        "return-type": "json",
        "interval": 30,
        "exec": "~/.config/waybar/modules/waybar-ras/ras.py"
    }
    ```