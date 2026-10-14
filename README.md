# Biblionx Libraskê Processor

*Pose and gesture evaluation processor for the Biblionx ecosystem.*

![Version](https://img.shields.io/badge/version-v2.3.0-blue.svg)
![License](https://img.shields.io/badge/license-LGPLv3-blue.svg)

> **Note — Biblionx-Project:** this repository is an adaptation of the Libraskê Processor kept as an architecture reference for the Biblionx thesis project (Dominican Sign Language, LSRD). The project's active, functional component is [`biblionx-lsrd-translator`](https://github.com/Biblionx-Project/biblionx-lsrd-translator); this repo provides pose extraction and holistic scoring for sign language gesture evaluation. See the [Biblionx-Project](https://github.com/Biblionx-Project) organization.

## Table of Contents

- [Introduction](#introduction)
  - [System Requirements](#system-requirements)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Usage](#usage)
  - [Development Mode](#development-mode)
  - [Production Mode](#production-mode)
- [Architecture & Workflow](#architecture--workflow)
- [Contributors](#contributors)
- [License](#license)

## Introduction

Biblionx Libraskê Processor consumes video frame landmark data from RabbitMQ queues, evaluates user performance against reference keypoint annotations using MediaPipe Holistic pipelines, and calculates accuracy pontuation.

### System Requirements

* OS: A modern Linux distribution, Windows, or macOS with Python 3.10+ / 3.12+
* MediaPipe, OpenCV, and RabbitMQ

### Prerequisites

Before starting the installation, ensure [RabbitMQ](https://www.rabbitmq.com/) is installed and running:

```sh
sudo apt-get update
sudo apt-get install -y rabbitmq-server
```

Start the RabbitMQ service:

```sh
sudo systemctl enable --now rabbitmq-server
```

### Installing

To install the project dependencies, create a virtual environment and install from `requirements.txt`:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively, use the Makefile:

```sh
make install
```

## Usage

### Development Mode

Run the worker in development mode:

```sh
make dev
```

Or execute directly with Python:

```sh
python src/worker.py
```

### Production Mode

Run the worker in production mode:

```sh
make start
```

## Architecture & Workflow

1. **Queue Consumer (`queueconsume.py`)**: Listens on the configured RabbitMQ queue for frame payloads containing base64 images, session IDs, and frame indices.
2. **Holistic Callback (`holistic_callback.py`)**: Decodes image frames and passes them to MediaPipe Holistic to extract pose and hand landmarks.
3. **Pontuation Evaluator (`holistic_pontuation.py`)**: Compares detected landmarks against ground-truth reference data stored in `references_data/` and computes likeness score.
4. **Queue Publisher (`queuepublisher.py`)**: Emits the evaluated score back onto RabbitMQ with session identification for upstream services.

## Environment Variables

Copy `.env.example` to `.env`. Both `BIBLIONX_*` and standard variables are supported:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `BIBLIONX_AMQP_HOST` / `AMQP_HOST` | RabbitMQ broker host | `localhost` |
| `BIBLIONX_AMQP_PORT` / `AMQP_PORT` | RabbitMQ broker port | `5672` |
| `BIBLIONX_AMQP_USER` / `AMQP_USER` | RabbitMQ username | `guest` |
| `BIBLIONX_AMQP_PASS` / `AMQP_PASS` | RabbitMQ password | `guest` |
| `BIBLIONX_AMQP_PREFETCH_COUNT` / `AMQP_PREFETCH_COUNT` | Consumer prefetch count | `1` |
| `BIBLIONX_RECEIVE_QUEUE` / `RECEIVE_QUEUE` | Queue for receiving pose/frame generation tasks | `frame_sender` |

## Contributors & Attribution

Originally developed by the VLibras team (Laboratório de Aplicações de Vídeo Digital - LAVID / UFPB and Brazilian Ministry of Planning/Management). Adapted, modernized, and maintained as an architectural reference for Dominican Sign Language (LSRD) avatar motion processing by the Biblionx team (UNICDA thesis project).

## License

This project is licensed under the LGPLv3 License - see the [LICENSE](LICENSE) file for details. Derived from the open-source VLibras project, maintaining full compliance with the GNU Lesser General Public License v3.0.