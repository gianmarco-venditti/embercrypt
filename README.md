# 2026-10-18 — Embercrypt: La Cripta della Brace

Prima piccola campagna locale per **Flare 1.15**, costruita come mod sopra
`fantasycore` e `empyrean_campaign`. Il motore e gli asset ufficiali restano separati
dai file della nostra avventura. Nessuna modifica al motore, nessun servizio online.

Obiettivo: attraversare tre sale, trovare un'arma nel forziere, sconfiggere il
Guardiano della Brace e raggiungere l'uscita alle sue spalle. La durata desiderata
e di pochi minuti. La prima partita sul desktop e stata completata dal giocatore;
durata, fluidita e audio non sono stati misurati.

## Avvio su Linux x86_64

Dal terminale, nella directory che contiene il progetto:

```bash
cd embercrypt
./setup.sh
./play.sh
```

`setup.sh` scarica il bundle ufficiale Linux x86_64 1.15, circa 580 MB, se non gia
presente in `.runtime/downloads/flare-linux64-v1.15.AppImage`. Lo estrae localmente:
non richiede sudo, FUSE o pacchetti di sistema. Serve Python 3.11+ e curl.
La prima estrazione richiede ulteriore spazio su disco.

Il supporto Windows di questo progetto resta uno sviluppo futuro: gli script
di installazione e avvio attuali sono predisposti e verificati su Linux.

Nel menu scegli **Gioca**; se compare la lista dei salvataggi, scegli **Nuova
partita**. Lascia la classe **Custode**, inserisci un nome e crea il personaggio.
Il titolo e alcuni elementi dell'interfaccia
rimangono quelli di Flare: e un prototipo con contenuti riutilizzati.

- **Clic sinistro:** movimento; su un nemico vicino, attacco.
- **Clic destro:** abilita speciale iniziale di Flare.
- **Q / E:** pozione di salute / mana, quando disponibili (comandi predefiniti di Flare).
- **I:** inventario; equipaggia la Lama della Brace dopo aver aperto il forziere.
- **L:** registro e obiettivo.
- **Esc:** menu, impostazioni e uscita.

Le associazioni effettive sono consultabili nelle impostazioni di Flare. Si parte
in finestra a 1280×720, con movimento tramite mouse e lingua italiana.
Per una prova con renderer software: `./play.sh --renderer=sdl`.

## Partita e ripartenza

Segui i corridoi tra le tre sale. Il forziere nella sala centrale contiene una
lama piu forte e due pozioni. Nella sala finale, sconfiggi il Guardiano, poi
raggiungi la runa luminosa in fondo: porta alla stanza finale e al messaggio di
vittoria. Puoi raggiungere fisicamente l'uscita prima, ma non usarla.

Salvataggi e impostazioni sono isolati in `.local/`; il prefisso dei salvataggi
e `ember_slice`. La mod usa la gestione della morte e del caricamento di Flare.
Per una nuova prova pulita crea una **Nuova partita** in un altro slot; nessuno
script elimina i salvataggi. I nemici comuni possono ricomparire ricaricando la
mappa; forziere, Guardiano e completamento usano stati persistenti.

## Struttura

| Percorso | Contenuto |
|---|---|
| `mods/ember_slice/` | Campagna, classe, oggetto, nemici, mappe, quest e finale |
| `scripts/build_maps.py` | Sorgente delle due mappe; geometria e incontri espliciti |
| `scripts/check.py` | Controlli statici e verifica dei riferimenti agli asset |
| `scripts/runtime.py` | Estrazione del bundle, isolamento e avvio |
| `.runtime/` | Download, contenuti ufficiali, impronta SHA-256 locale |
| `.local/` | Configurazione, salvataggi, cache e log delle sessioni |

Per modificare la disposizione iniziale, cambia `scripts/build_maps.py` e poi:

```bash
python3 scripts/build_maps.py
python3 scripts/check.py --assets
```

Le mappe risultanti sono normali file Flare testuali. Tiled potra essere aggiunto
per un flusso di editing visuale; non serve installarlo per avviare questa prova.

## Verifica

```bash
python3 scripts/check.py            # geometria e collegamenti, anche offline
python3 scripts/check.py --assets   # include, risorse e categorie; richiede setup
```

Questi controlli non certificano fluidita, audio, resa visiva o divertimento.
La scheda per la verifica nel gioco e in [docs/PLAYTEST.md](docs/PLAYTEST.md).
L'esito effettivo e in [docs/STATUS.md](docs/STATUS.md).

Fonti, attribuzioni e licenze: [CREDITS.md](CREDITS.md).
