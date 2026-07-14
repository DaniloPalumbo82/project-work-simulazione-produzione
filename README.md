# Modellazione e simulazione di un processo di raccolta agricola tramite Python

Simulazione di un processo produttivo nel settore primario sviluppata in Python.

## Descrizione

Questo progetto è stato realizzato nell'ambito del corso di **Informatica per le Aziende Digitali**.

L'obiettivo del progetto è simulare un processo produttivo agricolo utilizzando Python, confrontando due differenti modalità operative:

- **Produzione manuale**
- **Produzione meccanizzata**

Il modello rappresenta una versione semplificata ma realistica di un processo di raccolta agricola, introducendo elementi tipici della pianificazione delle risorse, quali:

- resa per ettaro;
- disponibilità di operatori e macchine;
- limite massimo di ore lavorabili;
- distribuzione del lavoro tra le unità operative;
- variabilità casuale della produzione;
- gestione del monte ore disponibile durante l'intero processo di raccolta.

---

## Funzionalità principali

Il programma consente di:

- inserire parametri iniziali personalizzabili:
  - numero di operai;
  - numero di macchine;
  - giorni previsti per la raccolta;
  - ettari coltivati per ciascun prodotto.

- generare quantità produttive variabili per tre colture:
  - Mais;
  - Pomodori;
  - Patate.

- simulare due differenti modalità di raccolta:
  - manuale;
  - meccanizzata.

- configurare facilmente:
  - resa per ettaro;
  - tempi di raccolta per chilogrammo;
  - capacità produttiva delle macchine;
  - ore massime lavorabili giornalmente.

- calcolare automaticamente:
  - quantità totale raccoglibile;
  - tempo totale necessario;
  - quantità raccolta giornalmente;
  - ore di lavoro giornaliere;
  - distribuzione del lavoro tra operai o macchine.

- verificare il rispetto della capacità produttiva disponibile attraverso un **monte ore complessivo**, riducendo automaticamente la quantità raccoglibile quando le risorse non sono sufficienti.

---

## Logica della simulazione

Il modello segue il seguente flusso operativo:

1. Acquisizione dei parametri iniziali inseriti dall'utente.

2. Generazione delle quantità producibili introducendo una variabilità casuale compresa tra l'80% e il 120% della resa prevista.

3. Calcolo della quantità richiesta per ciascun prodotto.

4. Calcolo del monte ore massimo disponibile secondo la formula:

   **Numero di unità × Giorni di lavoro × 8 ore**

5. Calcolo del tempo complessivamente necessario per raccogliere tutte le colture.

6. Se il monte ore disponibile non è sufficiente, il programma riduce proporzionalmente la quantità raccoglibile di tutti i prodotti.

7. La produzione viene distribuita uniformemente tra tutte le unità operative, garantendo una ripartizione equilibrata del carico di lavoro.

8. I risultati vengono presentati sia in forma aggregata sia nel dettaglio di ciascun operaio o macchina, riportando anche il totale delle ore giornaliere assegnate.

---

## Struttura del codice

Il progetto è organizzato nelle seguenti funzioni.

### **`get_initial_parameters()`**

Raccoglie tutti i parametri iniziali inseriti dall'utente necessari per l'esecuzione della simulazione.

### **`configuration()`**

Definisce i principali parametri configurabili del modello, tra cui:

- resa per ettaro;
- tempi di raccolta;
- moltiplicatore della raccolta meccanizzata;
- numero massimo di ore lavorabili giornalmente.

### **`generate_quantities()`**

Genera le quantità producibili per ciascuna coltura introducendo una variabilità casuale rispetto alla resa teorica.

### **`split_quantity_uniformly()`**

Distribuisce uniformemente la quantità di prodotto tra tutte le unità operative.

Questa funzione sostituisce la precedente distribuzione casuale, garantendo una ripartizione equilibrata del lavoro.

### **`simulate_production()`**

Rappresenta il cuore della simulazione.

La funzione:

- calcola il monte ore complessivamente disponibile;
- determina il tempo necessario per l'intera produzione;
- riduce proporzionalmente le quantità quando la capacità disponibile non è sufficiente;
- calcola tempi e quantità di produzione;
- distribuisce uniformemente il lavoro tra le unità operative;
- memorizza tutti i risultati della simulazione.

### **`print_results()`**

Visualizza i risultati mediante:

- tabella riepilogativa generale;
- dettaglio della produzione per ogni operaio o macchina;
- totale delle ore giornaliere assegnate a ciascuna unità operativa.

---

## Esecuzione del programma

Per eseguire il programma:

```bash
python simulazione_produzione.py
```

---

## Conclusioni

Il progetto mostra come sia possibile utilizzare Python per modellare e simulare un processo produttivo agricolo, applicando concetti di pianificazione delle risorse, gestione della capacità produttiva e distribuzione del lavoro.

L'introduzione di un **monte ore complessivo disponibile** rende il modello più aderente a uno scenario reale, poiché il programma confronta il tempo richiesto dall'intera produzione con la capacità operativa disponibile e, se necessario, riduce proporzionalmente la quantità raccoglibile di tutte le colture. Inoltre, la distribuzione uniforme del lavoro tra le unità operative consente di rappresentare un'organizzazione più equilibrata delle attività, facilitando il confronto tra raccolta manuale e raccolta meccanizzata.
