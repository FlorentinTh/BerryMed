<span align="center">
    <h1>BerryMed</h1>
</span>

<p align="center">
    <img src="https://cdn-shop.adafruit.com/970x728/4582-02.jpg" alt="BM100" height="400px" />
</p>

Projet to use BerryMed BM100 finger pulse oximeter with a Raspberry Pi using Bluetooth Low Energy.

[https://www.adafruit.com/product/4582](https://www.adafruit.com/product/4582)

## Authors

- [**Florentin Thullier**](https://github.com/FlorentinTh) - 2025

## Data

Example of recorded data can be found [here](/data/data.csv).

## Configuration

### Setup the Raspberry Pi

1. Install required dependencies
    ```sh
    $ sudo apt update && sudo apt upgrade -y
    $ sudo apt install git python3-pip -y
    ```
2. Configure static IP
    ```sh
    $ sudo nmcli -p connection show
    ```
    ```sh
    ======================================
    NetworkManager connection profiles
    ======================================
    NAME                UUID                                  TYPE      DEVICE
    ----------------------------------------------------------------------------
    Wired connection 1  bd220d18-7d6a-36a5-9820-4f67de2c01fc  ethernet  eth0
    mywifi              2359440b-8991-4c86-a905-b011dced4587  wifi      wlan0
    lo                  c29ba7c5-98ff-4fa0-8d8e-06b30b8ec384  loopback  lo
    ```

    ```sh
    $ sudo nmcli c mod "Wired connection 1" ipv4.addresses 192.168.1.85/24 ipv4.method manual
    $ sudo nmcli con mod "Wired connection 1" ipv4.gateway 192.168.1.1
    $ sudo nmcli con mod "Wired connection 1" ipv4.dns 192.168.1.1
    ```

    ```sh
    $ sudo nmcli c down "Wired connection 1" && sudo nmcli c up "Wired connection 1"
    ```

### Setup the Project
1. Initialization
    ```sh
    $ git clone https://github.com/FlorentinTh/BerryMed.git
    $ cd BerryMed
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt
    ```
3. Configure the environment
    ```sh
    # update the content of the .env.example file then run:
    $ mv .env.example .env
    ```
4. Install the service
    ```sh
    $ chmod +x start.sh
    $ sudo mv ./berry-med.service /etc/systemd/system/berry-med.service
    $ sudo systemctl start berry-med.service
    $ sudo systemctl enable berry-med.service
    $ sudo systemctl status berry-med.service
    ```

## License

This project is licensed under the APGL-3.0 License - see the [LICENSE](LICENSE) file for details.