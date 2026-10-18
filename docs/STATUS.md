# 2026-10-18 — Stato della vertical slice

## Implementato

- Mod locale separata dai materiali ufficiali Flare 1.15.
- Tre sale collegate, sette nemici di cui un Guardiano, forziere, arma, obiettivo,
  uscita condizionata e rifugio con finale.
- Script di installazione locale, avvio e controllo.
- Isolamento previsto di configurazione e salvataggi; nessuna cancellazione automatica.

## Eseguito

- `python3 scripts/check.py`: superato. 293 caselle calpestabili collegate;
  sette posizioni nemiche raggiungibili; transizioni e vincolo di vittoria validi.
- `bash -n setup.sh play.sh`: superato.
- `python3 -m py_compile scripts/*.py`: superato.
- Bundle ufficiale 1.15 scaricato dall'utente ed estratto nel progetto; versione
  dell'eseguibile confermata con `./play.sh --version`.
- `python3 scripts/check.py --assets`: superato, 22 file referenziati. Verificati
  anche gli ID delle tile utilizzate, le categorie dei nemici e l'ID dell'arma.
- Avvio nativo con SDL dummy e renderer software, con profilo separato in
  `.local/qa/`: menu, creazione Custode e ingresso nella cripta verificati tramite
  immagini del rendering effettivo, senza accesso al desktop.
- Apertura del forziere e inventario: Lama ID 5000 e due pozioni aggiuntive
  presenti. Stato `ember_chest` salvato. Evidenza: `.local/qa/chest-avatar.txt`
  e `.local/qa/chest-inventory.png`.
- Uscita con Guardiano vivo: bloccata, messaggio visibile. Evidenza:
  `.local/qa/exit-locked.png`.
- Combattimento contro il Guardiano e attivazione dell'uscita: verificati nel
  motore. Salvataggio nel rifugio con `ember_guardian_dead`, `ember_boss_reward`
  ed `ember_finished`; XP ottenuta 50 (Guardiano piu un nemico comune).
  Evidenza: `.local/qa/victory-avatar.txt`.
- Caricamento della sequenza finale verificato; schermata in `.local/qa/victory.png`.
- Morte per danni dei nemici, menu Game Over e pulsante Continua verificati:
  il personaggio torna vivo al punto salvato. Immagini `.local/qa/death.png` e
  `.local/qa/restart.png`, log `.local/qa/death-engine.log`.
- Ultimo avvio e sequenza finale senza errori nel log `.local/qa/final-engine.log`;
  controllati anche i comandi effettivi generati da Flare (pozioni Q/E).

Le prove nei settori del livello usano posizioni iniziali controllate in copie
del salvataggio di QA. Non costituiscono una partita continua dall'ingresso al
finale, ne una misura della durata o della difficolta per un giocatore.

Il 2026-10-18 il giocatore ha confermato di avere testato e vinto la partita
sul proprio desktop. Durata, frame rate e audio non sono stati misurati.

## Correzioni emerse dalla prova

- Parametri CLI Flare nel formato `--opzione=valore`.
- Preferenza alle librerie di sistema compatibili, con fallback alle librerie
  del bundle: risolve il conflitto fra JACK/PipeWire di Arch e il bundle.
- Tile del forziere, muri e pavimento corretti sui materiali del bundle.
- Testo del registro, posizione del log a schermo e margini del finale corretti.
- Raggio di ingaggio e danni da mischia degli arcieri ridotti per questa prova.
- Fallback grafico del menu di morte aggiunto da un asset ufficiale invariato.

## Da approfondire con il giocatore

- Audio reale, renderer sul desktop, fluidita e sensazione dei comandi.
- Difficolta percepita e durata effettiva.

Il terminale dell'agente non dispone di rete o accesso al display del desktop.
Il download e stato effettuato dall'utente; le verifiche del motore usano SDL
dummy e rendering software. Nessun pacchetto di sistema modificato. I profili
di QA e di gioco sono separati; i salvataggi dell'utente restano in `.local/`.

## Preparazione della pubblicazione — 2026-10-18

- Destinazione pubblica indicata dal proprietario:
  `gianmarco-venditti/embercrypt`, branch previsto `main`.
- Remote autorizzato: `git@github-embercrypt:gianmarco-venditti/embercrypt.git`.
- Identita Git prevista: `bishop <gianmarco.bishop@gmail.com>`.
- Alias SSH verificato tramite `ssh -F ~/.ssh/config -G github-embercrypt`:
  host GitHub, utente `git`, chiave dedicata, `IdentitiesOnly yes`.
  Chiave privata presente fuori dal progetto con permessi `600`.
- Collegamenti delle quattro mod verificati nel nuovo percorso `embercrypt`;
  controlli su mappe, 22 riferimenti ad asset, sintassi Python/shell e comando
  di versione Flare 1.15 superati dopo la rinomina.
- Runtime, salvataggi, log e cache esclusi da `.gitignore`. I file candidati
  alla pubblicazione sono circa 361 KiB; il maggiore e il fallback grafico
  attribuito in `CREDITS.md`, circa 313 KiB.
- Nessun segnale di credenziali trovato dalla scansione testuale dei sorgenti.
  Non e disponibile uno scanner dedicato: la scansione non e una certificazione.
- Il proprietario ha eseguito dal proprio terminale lo script locale
  `.local/publication/prepare-first-commit.sh`, escluso dalla pubblicazione:
  autenticazione GitHub confermata per `gianmarco-venditti/embercrypt`, remoto
  senza riferimenti e inizializzazione Git riuscita. La sessione dell'agente
  continua a vedere `.git` in sola lettura e non dispone di risoluzione DNS.
- Lo script si e fermato prima del commit: `git diff --cached --check` ha
  segnalato una riga vuota finale nelle due mappe. Il generatore ora normalizza
  la fine dei file e le mappe sono state rigenerate.
- Agente SSH e portachiavi non sono verificabili da questa sessione; non e stata
  importata una chiave nel portachiavi.
- Prossimo passo: aggiornare i file nell'indice Git dal terminale del proprietario,
  creare il primo commit ed eseguire il dry run del push. Il push reale richiede
  una successiva autorizzazione sul commit risultante.
