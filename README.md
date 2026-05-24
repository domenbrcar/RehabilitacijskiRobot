# RehabilitacijskiRobot

Urejena verzija projekta za rehabilitacijski robot Panda. Glavni program je
`src/main`; stare razvojne verzije so odstranjene iz
delovne strukture.

## Struktura

- `src/` - koda za snemanje, DMP/CMP ucenje in izvedbo rehabilitacijskega cikla.
- `src/trajectories/` - ociscene trajektorije, CMP signali in manifest podatkov.
- `pictures/` - fotografije robota/projekta; v `pictures/converted/` so HEIC
  datoteke pretvorjene v JPG za porocilo.
- `report/` - clanek, literatura in figure, uporabljene v clanku.

## Uporaba

1. Odpri `src/main_sposobnost_v4.ipynb`.
2. Za zagon uporabi isto ROS/robot okolje kot pri prvotnem projektu.
3. V celici z nastavitvami spremeni `SPOSOBNOST` med `0` in `100`.
4. Notebook sam najde `src/trajectories`, zato ga lahko odpres iz korena
   projekta ali neposredno iz mape `src`.

`SPOSOBNOST = 0` pomeni najvec robotske pomoci, `SPOSOBNOST = 100` pa najmanj.

## Fotografije

HEIC fotografije so pretvorjene z `pillow-heif` v `pictures/converted/*.jpg`.
Kontaktna slika `robot_fotografije_kontakt.jpg` je kopirana tudi v
`report/figures`, zato je vključena v `report/article.pdf`.
