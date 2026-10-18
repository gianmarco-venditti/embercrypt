# 2026-10-18 — Fonti e attribuzioni

- **Motore:** Flare 1.15, Flare team e contributori, GPL v3 o successiva.
  Sorgenti: <https://github.com/flareteam/flare-engine/tree/v1.15>.
- **Dati e materiali di gioco:** Flare: Empyrean Campaign / fantasycore,
  Clint Bellanger, Flare team e contributori, CC BY-SA 3.0 o successiva, salvo
  le eccezioni specifiche dichiarate a monte (fra cui i font).
  Sorgenti e dichiarazioni: <https://github.com/flareteam/flare-game/tree/v1.15>.
  Attribuzioni dettagliate e licenze restano nel bundle ufficiale.
- **Bundle Linux:**
  <https://github.com/flareteam/flare-game/releases/download/v1.15/flare-linux64-v1.15.AppImage>.
  Collegato dalla pagina ufficiale <https://flarerpg.org/download/>.
- **Modding:** <https://github.com/flareteam/flare-engine/wiki/Creating-an-empty-mod>.
- **Riferimento dati:** <https://github.com/flareteam/flare-engine/wiki/Attribute-Reference>.

La classe Custode e adattata dalla classe Brute di `engine/classes.txt` del gioco
ufficiale. I nostri nemici e la Lama riutilizzano definizioni, sprite, animazioni e
suoni del gioco tramite INCLUDE. Il prototipo mantiene queste attribuzioni e
adotta CC BY-SA 3.0 per i dati di `mods/ember_slice/`. I file indicano le modifiche;
mappe, testi e configurazione della campagna sono parte di questo esperimento.

`mods/ember_slice/images/menus/game_over.png` e una copia non modificata di
`fantasycore/images/menus/modal_window.png`, CC BY-SA 3.0, usata anche come immagine
di fallback per il menu di morte del motore 1.15.

Le dipendenze scaricate non sono incluse nei sorgenti della nostra mod.
`.runtime/manifest.json` registra versione, URL e SHA-256 del file locale:
questa impronta serve a identificare il download, non e una firma upstream
verificata indipendentemente.

Gli script Python e shell di questo progetto sono distribuiti sotto licenza MIT:

Copyright (c) 2026, autori di La Cripta della Brace.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
