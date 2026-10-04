<div align="center">
  <a href="http://www.vlibras.gov.br/">
    <img
      alt="VLibras"
      src="https://vlibras.gov.br/assets/imgs/IcaroGrande.png"
    />
  </a>
</div>

# Biblionx LSRD Processor

*Adapted from [VLibras](https://www.vlibras.gov.br/) Libraskê Processor Core.*

![Version](https://img.shields.io/badge/version-v2.3.0-blue.svg)
![License](https://img.shields.io/badge/license-LGPLv3-blue.svg)
![VLibras](https://img.shields.io/badge/vlibras%20suite-2019-green.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAUCAYAAAC9BQwsAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH4wIHCiw3NwjjIgAAAQ9JREFUOMuNkjErhWEYhq/nOBmkDNLJaFGyyyYsZzIZKJwfcH6AhcFqtCvFDzD5CQaTFINSlJJBZHI6J5flU5/P937fube357m63+d+nqBEagNYA9pAExgABxHxktU3882hjqtd9d7/+lCPsvpDZNA+MAXsABNU6xHYQ912ON2qC2qQ/X+J4XQXEVe/jwawCzwNAZp/NCLiDVgHejXgKIkVdGpm/FKXU/BJDfytbpWBLfWzAjxVx1Kuxwno5k84Jex0IpyzdN46qfYSjq18bzMHzQHXudifgQtgBuhHxGvKbaPg0Klaan7GdqE2W39LOq8OCo6X6kgdeJ4IZKUKWq1Y+GHVjF3gveTIe8BiCvwBEZmRAXuH6mYAAAAASUVORK5CYII=)

> **Note — Biblionx-Project:** this repository is an adaptation of [VLibras](https://www.vlibras.gov.br/) kept as an architecture reference for the Biblionx thesis project (Dominican Sign Language, LSRD, text translator). The project's active, functional component is [`biblionx-lsrd-translator`](https://github.com/Biblionx-Project/biblionx-lsrd-translator); this repo is kept as a historical reference of the original VLibras ecosystem, not as an active dependency of the final product. See the [Biblionx-Project](https://github.com/Biblionx-Project) organization.

## Table of Contents

  - [System Requirements](#system-requirements)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Deploy Tools](#deploy-tools)
  - [Deploying](#deploying)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### System Requirements

* OS: a modern Linux distribution with Python 3.12+ available

### Prerequisites

Before starting the installation, you need to install some prerequisites:

[RabbitMQ](https://www.rabbitmq.com/)

```sh
wget -O - "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo apt-key add -
```

```sh
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | sudo bash
```

```sh
sudo apt install -y rabbitmq-server --fix-missing
```

### Installing

After installing all the prerequisites, install the project by running the command:

From the repository root:

```sh
sudo make install
```

To test the installation, simply start the Translation Core with the following command:

From the repository root:

```sh
make dev
```

## Contributors

Originally developed by the Biblionx team.

## License

This project is licensed under the LGPLv3 License - see the [LICENSE](LICENSE) file for details.