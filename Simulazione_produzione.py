import random



# SEZIONE RACCOLTA PARAMETRI UTENTE

def get_initial_parameters():

    print("\nINSERIMENTO INFORMAZIONI PER LA RACCOLTA")
    print("-" * 50)

    team_size = int(
        input("Da quante persone è composta la squadra?: ")
    )

    machines = int(
        input("Quante macchine vuoi utilizzare?: ")
    )

    planned_days = int(
        input("Quanti giorni sono previsti per la raccolta?: ")
    )

    hectares = {
        "Mais": float(
            input("Quanti ettari di mais?: ")
        ),

        "Pomodori": float(
            input("Quanti ettari di pomodori?: ")
        ),

        "Patate": float(
            input("Quanti ettari di patate?: ")
        )
    }

    return team_size, machines, planned_days, hectares



# CONFIGURAZIONE DEL MODELLO

def configuration():

    return {

        # Resa media espressa in Kg per ettaro
        "yield_per_hectare": {
            "Mais": 80,
            "Pomodori": 60,
            "Patate": 70
        },

        # Tempo necessario per raccogliere un Kg
        # espresso in ore per Kg
        "time_per_unit": {

            "manual": {
                "Mais": 0.20,
                "Pomodori": 0.30,
                "Patate": 0.25
            },

            "mechanized": {
                "Mais": 0.10,
                "Pomodori": 0.15,
                "Patate": 0.12
            }
        },

        # Moltiplicatore della quantità richiesta
        # in caso di raccolta meccanizzata
        "machine_multiplier": 3,

        # Numero massimo di ore lavorabili
        # al giorno per ogni operaio o macchina
        "standard_hours_per_day": 8
    }



# GENERAZIONE DELLE QUANTITÀ DI RACCOLTO

def generate_quantities(hectares, config):

    products = {}

    for product, area in hectares.items():

        # Recupera la resa media del prodotto
        base_yield = config["yield_per_hectare"][product]

        # Introduce una variabilità casuale compresa
        # tra l'80% e il 120% della resa prevista
        variability = random.uniform(0.8, 1.2)

        # Calcola la quantità prodotta
        products[product] = round(
            area * base_yield * variability,
            2
        )

    return products



# DIVIDE UNA QUANTITÀ IN MODO UNIFORME
# TRA LE UNITÀ OPERATIVE

def split_quantity_uniformly(total_quantity, units):

    # Controllo per evitare una divisione per zero
    if units <= 0:
        return []

    # Quantità base assegnata a ogni unità
    base_quantity = round(
        total_quantity / units,
        2
    )

    quantities = [
        base_quantity
        for _ in range(units)
    ]

    # Corregge l'ultima unità per fare in modo
    # che la somma delle quantità corrisponda
    # esattamente alla quantità totale
    quantities[-1] = round(
        total_quantity - sum(quantities[:-1]),
        2
    )

    return quantities



# SIMULAZIONE DELLA PRODUZIONE

def simulate_production(
    products,
    config,
    method,
    units,
    planned_days,
    hectares
):

    results = {}

    # Controlli sui parametri principali
    if units <= 0:
        raise ValueError(
            "Il numero di operatori o macchine deve essere maggiore di zero."
        )

    if planned_days <= 0:
        raise ValueError(
            "Il numero di giorni deve essere maggiore di zero."
        )

    # Numero massimo di ore giornaliere
    # per ogni operaio o macchina
    standard_hours_per_day = (
        config["standard_hours_per_day"]
    )

    
    # Esempio:
    # 3 operai × 5 giorni × 8 ore = 120 ore totali.
    #
    # Le 120 ore devono essere utilizzate complessivamente
    # per Mais, Pomodori e Patate.
    
    
    total_available_hours = (
        planned_days *
        standard_hours_per_day *
        units
    )

    # Ore ancora disponibili durante la simulazione
    remaining_hours = total_available_hours

    # I prodotti vengono lavorati nell'ordine:
    # Mais, Pomodori, Patate
    for product, base_quantity in products.items():

        # Tempo necessario per raccogliere una unità di prodotto
        # 
        time_per_unit = (
            config["time_per_unit"][method][product]
        )

        # Resa media prevista per ettaro
        base_yield = (
            config["yield_per_hectare"][product]
        )

        # Ettari coltivati per il prodotto
        cultivated_hectares = hectares[product]

        
        # DETERMINA LA QUANTITÀ RICHIESTA
        
        if method == "mechanized":

            # Nel metodo meccanizzato viene applicato
            # il moltiplicatore configurato
            requested_quantity = (
                base_quantity *
                config["machine_multiplier"]
            )

        else:

            # Nel metodo manuale si utilizza direttamente la quantità prodotta
            # 
            requested_quantity = base_quantity

        
        # CALCOLO DELLA QUANTITÀ MASSIMA LAVORABILE CON LE ORE ANCORA DISPONIBILI
        # 
        
        if remaining_hours > 0:

            max_possible_quantity = (
                remaining_hours /
                time_per_unit
            )

        else:

            max_possible_quantity = 0

        # La quantità finale non può superare:
        # 1. la quantità richiesta;
        # 2. la quantità lavorabile con le ore residue.
        final_quantity = min(
            requested_quantity,
            max_possible_quantity
        )

        
        final_quantity = round(
            final_quantity,
            2
        )

        
        # CALCOLI PRINCIPALI
        

        # Ore totali necessarie per il prodotto
        total_time = (
            final_quantity *
            time_per_unit
        )

        
        total_time = round(
            total_time,
            2
        )

        
        # AGGIORNA IL MONTE ORE RESIDUO
        
        #
        # Le ore utilizzate per questo prodotto vengono sottratte dalle ore complessivamente disponibili.

        
        remaining_hours = max(
            0,
            remaining_hours - total_time
        )

        # Quantità totale raccolta ogni giorno
        quantity_per_day = (
            final_quantity /
            planned_days
        )

        # Ore giornaliere medie per ogni unità relative al singolo prodotto
       
        hours_per_day_per_unit = (
            total_time /
            (planned_days * units)
        )

        
        # DIVISIONE UNIFORME TRA LE UNITÀ
        
        quantities_per_unit = split_quantity_uniformly(
            final_quantity,
            units
        )

        # Calcola le ore totali assegnate a ogni singolo operaio o macchina
         
        hours_per_unit = [

            round(
                quantity * time_per_unit,
                2
            )

            for quantity in quantities_per_unit
        ]

        
        # SALVATAGGIO DEI RISULTATI
        
        results[product] = {

            "Ettari": cultivated_hectares,

            "Resa per Ettaro": base_yield,

            "Quantità Richiesta": round(
                requested_quantity,
                2
            ),

            "Quantità Totale": round(
                final_quantity,
                2
            ),

            "Tempo Totale (ore)": round(
                total_time,
                2
            ),

            "Quantità al Giorno": round(
                quantity_per_day,
                2
            ),

            "Ore al Giorno per unità": round(
                hours_per_day_per_unit,
                2
            ),

            "Quantità per unità": quantities_per_unit,

            "Ore per unità": hours_per_unit,

            "Ore residue": round(
                remaining_hours,
                2
            )
        }

    return results



# STAMPA DEI RISULTATI

def print_results(
    title,
    results,
    unit_name,
    units,
    planned_days
):

    
    # RIEPILOGO TOTALE (Dettaglio dopo)
    
    print(f"\n{title} - RIEPILOGO")

    print("-" * 110)

    print(
        f"{'Prodotto':<12}"
        f"{'Ettari':>10}"
        f"{'Resa/ha':>12}"
        f"{'Quantità richiesta':>22}"
        f"{'Quantità raccolta':>22}"
        f"{'Ore Totali':>15}"
        f"{'Kg/Giorno':>15}"
    )

    print("-" * 110)

    for product, data in results.items():

        print(
            f"{product:<12}"
            f"{data['Ettari']:>10.2f}"
            f"{data['Resa per Ettaro']:>12.2f}"
            f"{data['Quantità Richiesta']:>22.2f}"
            f"{data['Quantità Totale']:>22.2f}"
            f"{data['Tempo Totale (ore)']:>15.2f}"
            f"{data['Quantità al Giorno']:>15.2f}"
        )

    
    # DETTAGLIO PER OPERAIO O MACCHINA
    
    if units > 1:

        print(f"\n{title} - DETTAGLIO")

        print("-" * 95)

        print(
            f"{'Unità':<15}"
            f"{'Prodotto':<12}"
            f"{'Kg Totali':>15}"
            f"{'Ore Totali':>15}"
            f"{'Kg/Giorno':>15}"
            f"{'Ore/Giorno':>15}"
        )

        print("-" * 95)

        for i in range(units):

            for product, data in results.items():

                # Quantità giornaliera assegnata alla singola unità
                 
                quantity_per_day_unit = (
                    data["Quantità per unità"][i] /
                    planned_days
                )

                # Ore giornaliere relative al singolo prodotto
                 
                hours_per_day_unit = (
                    data["Ore per unità"][i] /
                    planned_days
                )

                # Determina l'etichetta da visualizzare
                if unit_name == "persona":

                    unit_label = (
                        f"Operaio {i + 1}"
                    )

                else:

                    unit_label = (
                        f"Macchina {i + 1}"
                    )

                print(
                    f"{unit_label:<15}"
                    f"{product:<12}"
                    f"{data['Quantità per unità'][i]:>15.2f}"
                    f"{data['Ore per unità'][i]:>15.2f}"
                    f"{quantity_per_day_unit:>15.2f}"
                    f"{hours_per_day_unit:>15.2f}"
                )

        
        # TOTALE GIORNALIERO PER OGNI UNITÀ
        
        print(
            f"\n{title} - TOTALE GIORNALIERO PER UNITÀ"
        )

        print("-" * 55)

        print(
            f"{'Unità':<20}"
            f"{'Ore/Giorno Totali':>25}"
        )

        print("-" * 55)

        for i in range(units):

            # Somma delle ore dell'unità su tutti i prodotti
             
            total_hours_unit = sum(

                data["Ore per unità"][i]

                for data in results.values()
            )

            # Ore giornaliere complessive
            total_hours_per_day_unit = (
                total_hours_unit /
                planned_days
            )

            if unit_name == "persona":

                unit_label = (
                    f"Operaio {i + 1}"
                )

            else:

                unit_label = (
                    f"Macchina {i + 1}"
                )

            print(
                f"{unit_label:<20}"
                f"{total_hours_per_day_unit:>25.2f}"
            )






# Carica la configurazione
config = configuration()

# Richiede i dati all'utente
team_size, machines, planned_days, hectares = (
    get_initial_parameters()
)

# Genera le quantità disponibili
products = generate_quantities(
    hectares,
    config
)

# Simulazione della produzione manuale
manual_results = simulate_production(
    products,
    config,
    "manual",
    team_size,
    planned_days,
    hectares
)

# Simulazione della produzione meccanizzata
mechanized_results = simulate_production(
    products,
    config,
    "mechanized",
    machines,
    planned_days,
    hectares
)

# Stampa i risultati della raccolta manuale
print_results(
    "Produzione Manuale",
    manual_results,
    "persona",
    team_size,
    planned_days
)

# Stampa i risultati della raccolta meccanizzata
print_results(
    "Produzione Meccanizzata",
    mechanized_results,
    "macchina",
    machines,
    planned_days
)
