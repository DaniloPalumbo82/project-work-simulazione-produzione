# Modellazione e simulazione di un processo di raccolta agricola tramite Python

Simulazione di un processo produttivo nel settore primario sviluppata in Python.

## Descrizione

Questo progetto è stato realizzato nell'ambito del corso di Informatica per le Aziende Digitali.

L'obiettivo del progetto è simulare un processo produttivo agricolo utilizzando Python, confrontando due differenti modalità operative:

* Produzione manuale
* Produzione meccanizzata

Il modello rappresenta in forma semplificata un processo di raccolta agricola, introducendo elementi realistici come:

* resa per ettaro,
* disponibilità delle risorse,
* limite massimo di ore lavorabili,
* distribuzione del lavoro tra unità operative,
* variabilità casuale delle quantità prodotte.

## Funzionalità principali

Il programma consente di:

* Inserire parametri iniziali personalizzabili:

  * numero di operai,
  * numero di macchine,
  * giorni previsti per la raccolta,
  * ettari coltivati per ciascun prodotto.

* Generare quantità produttive variabili per tre prodotti agricoli:

  * Mais
  * Pomodori
  * Patate

* Calcolare la produzione considerando:

  * resa per ettaro,
  * variabilità casuale,
  * tempi di lavorazione differenti,
  * modalità manuale o meccanizzata.

* Configurare:

  * tempi di raccolta per unità di prodotto,
  * capacità produttiva del metodo meccanizzato,
  * limite massimo di 8 ore giornaliere per unità operativa.

* Simulare il processo produttivo per due modalità differenti:

  * raccolta manuale,
  * raccolta meccanizzata.

* Calcolare:

  * quantità totale raccoglibile,
  * tempo totale necessario,
  * quantità giornaliera,
  * ore giornaliere per unità,
  * distribuzione del lavoro tra operai o macchine.

* Visualizzare i risultati tramite:

  * tabella riepilogativa generale,
  * tabella di dettaglio per singola unità operativa.

## Struttura del codice

Il codice utilizza le seguenti funzioni:

* `get_initial_parameters()`
  raccoglie i parametri iniziali inseriti dall’utente.

* `configuration()`
  definisce i parametri principali del modello.

* `generate_quantities()`
  genera le quantità produttive in base a ettari, resa per ettaro e variabilità casuale.

* `split_quantity()`
  distribuisce il lavoro tra le unità operative.

* `simulate_production()`
  esegue la simulazione del processo produttivo.

* `print_results()`
  stampa i risultati in formato tabellare.

## Tecnologie utilizzate

* Python

* Librerie:

  * `random`

## Esecuzione del programma

Per eseguire il codice:

```bash
python simulazione_produzione.py
```
