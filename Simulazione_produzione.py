import random


# --------------------------------------------------
# RACCOLTA DEI PARAMETRI INSERITI DALL'UTENTE
# --------------------------------------------------
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


# --------------------------------------------------
# CONFIGURAZIONE DEL MODELLO
# --------------------------------------------------
def configuration():

    return {

        # Resa media espressa in Kg per ettaro
        "yield_per_hectare": {
            "Mais": 80,
            "Pomodori": 60,
            "Patate": 70
        },

        # Tempo necessario per raccogliere un Kg,
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

        # Moltiplicatore applicato alla quantità richiesta
        # nella modalità meccanizzata
        "machine_multiplier": 3,

        # Numero massimo di ore lavorabili al giorno
        # per ciascun operaio o macchina
        "standard_hours_per_day": 8
    }


# --------------------------------------------------
# GENERAZIONE DELLE QUANTITÀ DI RACCOLTO
# --------------------------------------------------
def generate_quantities(hectares, config):

    products = {}

    for product, area in hectares.items():

        # Recupera la resa media per ettaro
        base_yield = (
            config["yield_per_hectare"][product]
        )

        # Introduce una variabilità casuale
        # compresa tra l'80% e il 120%
        variability = random.uniform(0.8, 1.2)

        # Calcola la quantità prodotta
        products[product] = round(
            area * base_yield * variability,
            2
        )

    return products


# --------------------------------------------------
# DIVISIONE UNIFORME TRA LE UNITÀ OPERATIVE
# --------------------------------------------------
def split_quantity_uniformly(total_quantity, units):

    if units <= 0:
        return []

    base_quantity = round(
        total_quantity / units,
        2
    )

    quantities = [
        base_quantity
        for _ in range(units)
    ]

    # Corregge l'ultima unità per compensare
    # eventuali differenze di arrotondamento
    quantities[-1] = round(
        total_quantity - sum(quantities[:-1]),
        2
    )

    return quantities


# --------------------------------------------------
# SIMULAZIONE DELLA PRODUZIONE
# --------------------------------------------------
def simulate_production(
    products,
    config,
    method,
    units,
    planned_days,
    hectares
):

    results = {}

    if units <= 0:
        raise ValueError(
            "Il numero di operatori o macchine "
            "deve essere maggiore di zero."
        )

    if planned_days <= 0:
        raise ValueError(
            "Il numero di giorni deve essere "
            "maggiore di zero."
        )

    standard_hours_per_day = (
        config["standard_hours_per_day"]
    )

    # Monte ore complessivo disponibile
    total_available_hours = (
        planned_days *
        standard_hours_per_day *
        units
    )

    requested_quantities = {}
    required_hours = {}

    # --------------------------------------------------
    # PRIMA FASE:
    # CALCOLO DELLE QUANTITÀ RICHIESTE
    # E DELLE ORE NECESSARIE PER TUTTI I PRODOTTI
    # --------------------------------------------------
    for product, base_quantity in products.items():

        time_per_unit = (
            config["time_per_unit"][method][product]
        )

        if method == "mechanized":

            requested_quantity = (
                base_quantity *
                config["machine_multiplier"]
            )

        else:

            requested_quantity = base_quantity

        requested_quantities[product] = (
            requested_quantity
        )

        required_hours[product] = (
            requested_quantity *
            time_per_unit
        )

    # Ore necessarie per raccogliere tutti i prodotti
    total_required_hours = sum(
        required_hours.values()
    )

    # --------------------------------------------------
    # FATTORE DI RACCOLTA
    # --------------------------------------------------
    #
    # Se le ore disponibili sono sufficienti,
    # il fattore vale 1 e viene raccolto il 100%.
    #
    # Se le ore non bastano, tutti i prodotti
    # vengono ridotti nella stessa proporzione.
    # --------------------------------------------------
    if total_required_hours > 0:

        collection_factor = min(
            1,
            total_available_hours /
            total_required_hours
        )

    else:

        collection_factor = 0

    # --------------------------------------------------
    # SECONDA FASE:
    # CALCOLO DEI RISULTATI PER OGNI PRODOTTO
    # --------------------------------------------------
    used_hours = 0

    for product in products:

        time_per_unit = (
            config["time_per_unit"][method][product]
        )

        base_yield = (
            config["yield_per_hectare"][product]
        )

        cultivated_hectares = (
            hectares[product]
        )

        requested_quantity = (
            requested_quantities[product]
        )

        # Tutti i prodotti ricevono la stessa
        # percentuale del monte ore disponibile
        final_quantity = round(
            requested_quantity *
            collection_factor,
            2
        )

        total_time = round(
            final_quantity *
            time_per_unit,
            2
        )

        used_hours += total_time

        quantity_per_day = (
            final_quantity /
            planned_days
        )

        hours_per_day_per_unit = (
            total_time /
            (planned_days * units)
        )

        collection_percentage = (
            collection_factor * 100
        )

        quantities_per_unit = (
            split_quantity_uniformly(
                final_quantity,
                units
            )
        )

        hours_per_unit = [
            round(
                quantity * time_per_unit,
                2
            )
            for quantity in quantities_per_unit
        ]

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

            "Percentuale Raccolta": round(
                collection_percentage,
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

            "Ore per unità": hours_per_unit
        }

    # Calcolo delle ore residue complessive
    remaining_hours = max(
        0,
        total_available_hours - used_hours
    )

    # Salva le ore residue in ogni prodotto
    for data in results.values():

        data["Ore residue"] = round(
            remaining_hours,
            2
        )

    return results


# --------------------------------------------------
# STAMPA DEI RISULTATI
# --------------------------------------------------
def print_results(
    title,
    results,
    unit_name,
    units,
    planned_days
):

    # --------------------------------------------------
    # RIEPILOGO GENERALE
    # --------------------------------------------------
    summary_width = 96

    print(f"\n{title} - RIEPILOGO")
    print("-" * summary_width)

    print(
        f"{'Prodotto':<12}"
        f"{'Ettari':>8}"
        f"{'Resa/ha':>10}"
        f"{'Kg richiesti':>15}"
        f"{'Kg raccolti':>15}"
        f"{'% raccolta':>12}"
        f"{'Ore':>11}"
        f"{'Kg/giorno':>13}"
    )

    print("-" * summary_width)

    for product, data in results.items():

        print(
            f"{product:<12}"
            f"{data['Ettari']:>8.2f}"
            f"{data['Resa per Ettaro']:>10.2f}"
            f"{data['Quantità Richiesta']:>15.2f}"
            f"{data['Quantità Totale']:>15.2f}"
            f"{data['Percentuale Raccolta']:>11.2f}%"
            f"{data['Tempo Totale (ore)']:>11.2f}"
            f"{data['Quantità al Giorno']:>13.2f}"
        )

    print("-" * summary_width)

    # --------------------------------------------------
    # DETTAGLIO PER OPERAIO O MACCHINA
    # --------------------------------------------------
    if units > 1:

        detail_width = 82

        print(f"\n{title} - DETTAGLIO")
        print("-" * detail_width)

        print(
            f"{'Unità':<14}"
            f"{'Prodotto':<12}"
            f"{'Kg totali':>14}"
            f"{'Ore totali':>14}"
            f"{'Kg/giorno':>14}"
            f"{'Ore/giorno':>14}"
        )

        print("-" * detail_width)

        for i in range(units):

            for product, data in results.items():

                quantity_per_day_unit = (
                    data["Quantità per unità"][i] /
                    planned_days
                )

                hours_per_day_unit = (
                    data["Ore per unità"][i] /
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
                    f"{unit_label:<14}"
                    f"{product:<12}"
                    f"{data['Quantità per unità'][i]:>14.2f}"
                    f"{data['Ore per unità'][i]:>14.2f}"
                    f"{quantity_per_day_unit:>14.2f}"
                    f"{hours_per_day_unit:>14.2f}"
                )

        print("-" * detail_width)

        # --------------------------------------------------
        # TOTALE GIORNALIERO PER UNITÀ
        # --------------------------------------------------
        total_width = 45

        print(
            f"\n{title} - TOTALE GIORNALIERO PER UNITÀ"
        )

        print("-" * total_width)

        print(
            f"{'Unità':<20}"
            f"{'Ore/giorno totali':>25}"
        )

        print("-" * total_width)

        for i in range(units):

            total_hours_unit = sum(
                data["Ore per unità"][i]
                for data in results.values()
            )

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

        print("-" * total_width)


# --------------------------------------------------
# PROGRAMMA PRINCIPALE
# --------------------------------------------------

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
