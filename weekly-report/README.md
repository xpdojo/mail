# markdown으로 주간업무보고 보내기

## Python으로 바로 보내기

### Setup Python

```sh
python3 -m venv .venv
echo '.venv' >> .gitignore
source .venv/bin/activate
```

```sh
python -m pip install -r requirements.txt
```

### Send mail

```sh
export MAIL_HOST=mail.example.com
export MAIL_DOMAIN=example.com
```

```sh
touch report.md
# edit report.md
```

```sh
python main.py
# Password:
```

## vim에서 pandoc으로 변환 후 복붙

```sh
cd /tmp
curl -LO https://github.com/jgm/pandoc/releases/download/3.1/pandoc-3.1-1-amd64.deb
sudo dpkg -i pandoc-3.1-1-amd64.deb
```

```sh
pandoc -v
sudo apt info pandoc
```

HTML로 복사

```vim
:w !pandoc -f markdown -t html | xclip -sel clip
```

Gmail에 붙여넣어서 보내기
