# Google images scraper
![Logo](https://mma.prnewswire.com/media/2376904/PastedGraphic_1_Logo.jpg?p=facebook)
## Installation guide:
```bash
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirments.txt
```

## Usage:
Headless - black subaru 10 photos example:
```bash
  python3 main.py --how_many 10 --prompt "black subaru"
```

Regular - black subaru 10 photos example:
```bash
  python3 main.py --how_many 10 --prompt "black subaru" --hard
```