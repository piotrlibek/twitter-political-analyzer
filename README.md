# twitter-political-analyzer
Analizuj poglądy polityczne, religijne, ideologiczne osób z Twittera

### Przyklady

Analizuj poglądy osoby @majakstasko Maja Staśko:

```
twitterpoliticalanalyzer.py majakstasko pl_PL.json

Found a Bearer Token!
Successfully created the directory
Done!
```

<img src="https://i.imgur.com/pVawP2Y.png" width="655" alt="Skrzydło polityczne" />
<img src="https://i.imgur.com/r1FUqeE.png" width="655" alt="Partie polityczne" />
<img src="https://i.imgur.com/3iazbtD.png" width="655" alt="Kompas polityczny" />
<img src="https://i.imgur.com/L8EecIa.png" width="655" alt="Ideologie" />

Po uruchomieniu skryptu zostanie stworzony katalog użytkownika, w środku niego znajdziesz 4 obrazki przedstawiające analizy
- Skrzydła politycznego
- Poparcia partii politycznej
- Symulowanego kompasu politycznego
- Ideologii

### Użycie

* Do używania skryptu potrzebny jest plik językowy który zawiera listę ideologii, partii politycznych, i danych potrzebnych do
stworzenia statystyki wyjściowej. Podstawowy plik w języku polskim jest załączony w repozytorium.

* twitterpoliticalanalyzer.py [twitter_name] [language_filename]

* Help: twitterpoliticalanalyzer.py -h

```
usage: twitterpoliticalanalyzer.py [-h] [--width WIDTH] [--height HEIGHT]
                                   [--dontUseFollowersData]
                                   [--useOnlyFollowersData]
                                   [--bearerToken BEARERTOKEN]
                                   [--usePartyPatterns]
                                   twitterName languageFilename

positional arguments:
  twitterName           Twitter username here
  languageFilename      Language filename here

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH         Output image width
  --height HEIGHT       Output image height
  --dontUseFollowersData
                        Do not use data about the people who follow the user
  --useOnlyFollowersData
  --bearerToken BEARERTOKEN
                        Bearer Authentication token
  --usePartyPatterns    Experimental, improve the ideologies results
```
