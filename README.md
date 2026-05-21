# Comprobot

Comprobot is a highly-customizable, open-source Discord bot that you can run on your own server.

It’s built with Python, has a wide range of fun and useful commands, and is designed to be easy to extend. 
You can add new commands, customize outputs, or change the behaviour of existing ones. You can also easily edit the keywords of existing commands and customize their outputs.

The bot also comes with built-in AI capabilities when pinging the bot, with Ollama, Groq and Gemini as available providers.

## Install

**pipx** (All platforms)
```sh
pipx install comprobot
```

**APT** (Ubuntu/Debian/Kali)
```sh
# If add-apt-repository isn't found, run this first:
# sudo apt install software-properties-common
sudo add-apt-repository ppa:badluma/ppa
sudo apt update
sudo apt install comprobot
```

**AUR** (Arch)
```sh
yay -S --noconfirm --nodiffmenu comprobot
```

**Homebrew** (macOS)
```sh
brew tap badluma/tap
brew install comprobot
```

**Winget** (Windows)
```sh
winget install badluma.comprobot
```

**Scoop** (Windows)
```sh
scoop bucket add badluma https://github.com/badluma/scoop-bucket
scoop install comprobot
```

**Docker** (All platforms)

Set up credentials first:
```sh
docker run -it --rm \
  -v comprobot-data:/root/.local/share/Comprobot \
  badluma/comprobot:latest onboard
```

Then start the bot:
```sh
docker run -d \
  -v comprobot-data:/root/.local/share/Comprobot \
  --name comprobot \
  badluma/comprobot:latest
```

## Documentation

You can find the whole documentation [here](https://badluma.github.io/Comprobot-Docs/).

## License

MIT
