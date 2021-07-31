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

# Porady i uwagi

Skrypt jest bardzo eksperymentalny, nie daje on idealnych statystyk i wyników. Działa tylko i wyłącznie na dużych danych i osobach związanych z poglądami choć trochę (a nie np. do użytkowników którzy używają Twittera tylko i wyłącznie do pisania tweetów pod Elonem Muskiem).

Aby skrypt działał dobrze, skonfiguruj odpowiednio parametry. Nie używaj go kiedy masz przeczucie czy pewność co do poglądów osoby bo mogą być to wyniki sprzeczne z tym co wiesz.

UWAGA!:
Statystyki są wyświetlane w formie natężenia poglądu, w podstawowym pliku językowym znajdziesz ideologie które mają również swoje alternatywy. Dla przykładu:
* Kapitalizm ma alternatywę w postaci socjalizmu
* Konserwatyzm ma alternatywę w postaci progresywizmu
* Monarchizm ma alternatywę w postaci demokracji
* Pro-Gun nie ma swojej alternatywy
* Minarchizm nie ma swojej alternatywy, ale zwróć uwagę na wyniki socjalizmu czy anarchizmu
* Pro-Life ma alternatywę w postaci Pro-Choice
* Militaryzm ma alternatywę w postaci Pacyfizmu
* Nacjonalizm ma alternatywę w postaci Internacjonalizmu

I zwróć uwagę na poparcie obu alternatyw. Kiedy kapitalizm przewyższa wynik socjalizmu można powiedzieć że osoba jest bardziej o poglądach kapitalistycznych czy wolnorynkowych.

# Jak to działa

Skrypt opiera się na hipotezie że użytkownicy zazwyczaj obserwują osoby z danymi poglądami częściej niż osób z przeciwnymi poglądami. Skrypt bierze pod uwagę też to jakie osoby obserwują tą właśnie osobę przez tak samo brzmiącą hipotezę jak powyżej. Oczywiście nie może to działać w przypadku popularnych lub marketingowych
kont Twittera gdzie nie są to konta prywatne użytkownika.
