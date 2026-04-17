# project-work-simulazione-produzione
Simulazione di un processo produttivo nel settore primario sviluppata in Python

## Descrizione
Questo progetto è stato realizzato nell'ambito del corso di Informatica per le Aziende Digitali.

L'obiettivo è simulare un processo produttivo nel settore primario utilizzando Python, confrontando due modalità operative:
- Produzione manuale
- Produzione meccanizzata

## Funzionalità principali
Il programma consente di:
- Generare casualmente le quantità da produrre per tre prodotti agricoli:
  - Mais
  - Pomodori
  - Patate
- Configurare i tempi di produzione per unità
- Simulare il processo produttivo per due modalità diverse
- Calcolare:
  - Tempo totale di produzione
  - Giorni necessari
- Visualizzare i risultati:
  - Tabella testuale
  - Grafico comparativo

## Struttura del codice
Il codice è organizzato in funzioni:
- `generate_quantities()` → genera quantità casuali
- `configuration()` → definisce parametri del sistema
- `simulate_production()` → calcola tempi e giorni
- `print_results()` → stampa risultati
- `plot_results()` → genera grafico

## Tecnologie utilizzate
- Python
- Librerie:
  - random
  - matplotlib

## Esecuzione del programma
Per eseguire il codice:

```bash
python simulazione_produzione.py
