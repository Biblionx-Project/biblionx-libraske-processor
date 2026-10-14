# Biblionx Libraske Processor

*Pose evaluation worker for Dominican Sign Language (LSRD) practice in the Biblionx ecosystem.*

![License](https://img.shields.io/badge/license-LGPLv3-blue.svg)

Biblionx is a UNICDA thesis project (Trabajo de Grado) that translates written Spanish (Dominican
Republic) into Dominican Sign Language (LSRD, Lengua de Señas Dominicana). The active product is
[`biblionx-lsrd-translator`](https://github.com/Biblionx-Project/biblionx-lsrd-translator). This
repository is one of the Biblionx architecture reference components: a RabbitMQ worker that scores how
closely a signer's pose in a video frame matches a recorded reference sign. See the
[Biblionx-Project](https://github.com/Biblionx-Project) organization for the other components.

## Table of Contents

- [How it works](#how-it-works)
- [Message format](#message-format)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the worker](#running-the-worker)
- [Generating reference data](#generating-reference-data)
- [Project layout](#project-layout)
- [Known limitations](#known-limitations)
- [Team](#team)
- [Origins](#origins)

## How it works

1. **Consume** (`src/queues/queueconsume.py`): the worker listens on the receive queue
   (`frame_sender` by default) and acknowledges messages automatically.
2. **Extract landmarks** (`src/utils/holistic_callback.py`): the base64 frame is decoded with OpenCV
   and run through MediaPipe Holistic (`static_image_mode=True`) to get pose and hand landmarks.
3. **Score** (`src/utils/holistic_pontuation.py`): the detected landmarks are compared with the
   reference landmarks in `references_data/<videoId>.txt` for the same frame. The keypoints compared
   are defined in `src/utils/scheme/SchemeEvaluation.py` (shoulders, elbows, hips and wrists from the
   pose, plus all 21 landmarks of each hand). The mean x/y distance is computed per group and
   weighted (pose 1, each hand 2) into a likeness value between 0 and 1.
4. **Publish** (`src/queues/queuepublisher.py`): `src/worker.py` turns the likeness into an integer
   score, computed as `(two-decimal likeness percentage + 100) // 3` (so a perfect match gives 66 and
   no match gives 0), and publishes it to the `frame_receiver` queue.

## Message format

Input, published to the receive queue (JSON). Messages with two or fewer keys are ignored.

```json
{
  "idSession": "game-session-id",
  "videoId": "3",
  "idFrame": "1",
  "frameImage": "<base64-encoded JPEG/PNG>"
}
```

- `videoId` selects the reference file `references_data/<videoId>.txt` (the repo ships `0` to `6`).
- `idFrame` must be a string that matches a frame key in that file (`"1"`, `"2"`, ...).

Output, published to `frame_receiver` (queue name is fixed in `src/worker.py`):

```json
{ "idGameSession": "game-session-id", "pontuation": 52 }
```

## Requirements

- Python 3.10 to 3.12 (the Docker image uses Python 3.12)
- A reachable RabbitMQ broker
- Debian or Ubuntu if you use `install.sh` (it installs packages with `apt-get`)
- Python packages from `requirements.txt`: `pika`, `numpy`, `opencv-python-headless`, `mediapipe`,
  plus `fire` and `tqdm` for the test script

To run RabbitMQ locally on Debian/Ubuntu:

```sh
sudo apt-get update
sudo apt-get install -y rabbitmq-server
sudo systemctl enable --now rabbitmq-server
```

Or with Docker:

```sh
docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3
```

## Installation

`make install` runs `install.sh`, which installs `build-essential`, `python3-venv` and `python3-pip`
via `apt-get` (as root or with `sudo`), creates `.venv/` and installs `requirements.txt` into it:

```sh
make install
```

To skip the system packages, create the virtual environment yourself. The Makefile expects it at
`.venv/`:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Configuration

The worker reads an INI file whose path is given by the `CORE_CONFIG_FILE` environment variable. The
Makefile sets it for you.

| File | Used by | Contents |
| :--- | :--- | :--- |
| `src/config/settings-dev.ini` | `make dev` | Fixed values: `localhost:5672`, `guest`/`guest`, queue `frame_sender` |
| `src/config/settings.ini` | `make start`, `make stage` | Values interpolated from the environment variables below |

Environment variables for `settings.ini`. All of them must be set, since the file has no fallback
values. Each one can also be given with a `BIBLIONX_` prefix (for example `BIBLIONX_AMQP_HOST`); the
prefixed form is used only when the unprefixed one is not set.

| Variable | Description | Example |
| :--- | :--- | :--- |
| `AMQP_HOST` | RabbitMQ host | `localhost` |
| `AMQP_PORT` | RabbitMQ port | `5672` |
| `AMQP_USER` | RabbitMQ user | `guest` |
| `AMQP_PASS` | RabbitMQ password | `guest` |
| `AMQP_PREFETCH_COUNT` | Prefetch count (read from config, not yet applied to the channel) | `1` |
| `RECEIVE_QUEUE` | Queue to consume frames from | `frame_sender` |

`.env.example` lists these variables. Nothing loads `.env` automatically, so export it into your
shell first:

```sh
cp .env.example .env
set -a; . ./.env; set +a
```

## Running the worker

Run every command from the repository root. The worker opens `references_data/` and writes annotated
frames to `processed_frames/` using paths relative to the current directory. Create that directory
first, or the annotated images will not be saved:

```sh
mkdir -p processed_frames
```

Development, against a local broker with `settings-dev.ini`:

```sh
make dev
```

Production, with `settings.ini` and the environment variables above:

```sh
set -a; . ./.env; set +a
make start
```

To run the script without the Makefile, set `CORE_CONFIG_FILE` yourself. Without it no configuration
is loaded and the worker cannot start consuming:

```sh
CORE_CONFIG_FILE=src/config/settings-dev.ini .venv/bin/python src/worker.py
```

### Docker

The image copies the repo to `/mediapipe`, runs `install.sh` and starts with `make start`, so pass
the broker settings as environment variables:

```sh
docker build -t biblionx-libraske-processor .
docker run --rm --env-file .env -e AMQP_HOST=<broker-host> biblionx-libraske-processor
```

`localhost` inside the container is the container itself. Point `AMQP_HOST` at the broker's
reachable address, or use `--network host` on Linux.

## Generating reference data

`src/reference_generator.py` builds a reference file from a recorded sign video. It samples one frame
every 3 seconds, saves the selected landmarks as JSON keyed by frame number (`"1"`, `"2"`, ...), and
writes annotated images to `reference_frames/`:

```sh
.venv/bin/python src/reference_generator.py -i path/to/7.mp4 -o references_data/7.txt
```

Name the output `<videoId>.txt` so incoming messages with that `videoId` can find it. If the output
file already exists, new frames are merged into it.

## Project layout

```
src/
  worker.py                 # Entry point: consume, score, publish
  reference_generator.py    # Builds references_data/<id>.txt from a video
  config/                   # settings.ini (env-driven) and settings-dev.ini
  queues/                   # RabbitMQ consumer and publisher (pika)
  utils/
    configreader.py         # INI loader + BIBLIONX_* env aliases
    holistic_callback.py    # Frame decoding + MediaPipe Holistic
    holistic_pontuation.py  # Landmark comparison and likeness score
    scheme/SchemeEvaluation.py  # Keypoints used for scoring
references_data/            # Reference landmarks per video id (JSON in .txt files)
tests/
  frame_extractor.py        # Video frame publisher (see limitations)
  videos_sample/            # Sample videos 01.mp4, 02.mp4
```

## Known limitations

- `tests/frame_extractor.py` publishes an older payload (`video_id`, `frame_id`, `frame_link`) that
  the current worker does not accept. Use it as a starting point for a test publisher, not as a
  working end-to-end test. It also expects an `input_frames/` directory.
- The worker logs the RabbitMQ connection settings, including the password, at startup.
- The output queue (`frame_receiver`) is fixed in code and cannot be configured.
- Messages are auto-acknowledged, so a frame that fails during processing is not redelivered.

## Team

Biblionx is developed by [@MiraP7](https://github.com/MiraP7),
[@Jose-hub-design](https://github.com/Jose-hub-design) and
[@wilkinvasquez](https://github.com/wilkinvasquez) as a UNICDA thesis project.

## Origins

This project was initially forked from the open-source VLibras project. It has since evolved enough
to stand as an independent project of its own. Licensed under LGPLv3. See [LICENSE](LICENSE).
