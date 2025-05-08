# qurandl
﷽

Simple Python CLI script for mass downloading Qur'an from [QuranicAudio](https://www.quranicaudio.com).

**Features**:
- Download the entirety of the Qur'an in under two minutes.
- Choose any filename format you prefer.
- Choose whichever reciter you prefer.

## Installation
All that is necessary is the [`quran.py`](./quran.py) file; you additionally must download the two dependencies in [`requirements.txt`](./requirements.txt).

Ensure that you have Python installed. Execute the program with `/path/to/quran.py`.

## Usage

- Call the program with `python quran.py`.
- Your first argument should be the surah number(s) or "all". This is required. `55` to download Ar-Rahman; or `ar-rahman`. You may also do `all` to download the entire Qur'an, or `55-75` to download every Surah from Ar-Rahmān to Al-Qiyāmah.
- `-r` or `--reciter` to specify reciter. A list of possible reciter names is within the `reciters` dictionary at the top of [`quran.py`](./quran.py). Defaults to `yasser_ad-dussary`.
- `-o` or `--output`: This *must* be a directory. E.g. `--output ~/media/audio/quran`. This option is not required and will default to the current directory.
- `-f` or `--file-name`: You may format the filename in any fashion you wish. Any instance of `number` will be replaced with the Surah's respective number, and any instance of `name` will be replaced with the Surah's name. Defaults to `number - name.mp3`. Do not forget to add `.mp3`! This option is not required.

Example usage: `python quran.py 42-46 -r idrees_abkar -o ~/media/audio/quran/idrees_abkar -f "number.name.mp3"`.

## License
Licensed under [GNU GPLv3](./LICENSE).