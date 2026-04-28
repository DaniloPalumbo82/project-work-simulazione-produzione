import random


# --------------------------------------------------
# GENERA LE QUANTITÀ DI RACCOLTO
# --------------------------------------------------
# Questa funzione crea quantità casuali iniziali per ogni prodotto.
# I valori sono espressi in Kg.
def generate_quantities():
    return {
        "Mais": random.randint(50, 150),
        "Pomodori": random.randint(30, 100),
        "Patate": random.randint(40, 120)
    }


# --------------------------------------------------
# RACCOGLIE I PARAMETRI INSERITI DALL'UTENTE
# --------------------------------------------------
# Chiede:
# - quante persone lavorano manualmente
# - quante macchine vengono usate
# - in quanti giorni si vuole completare la raccolta
def get_initial_parameters():
    team_size = int(input("Da quante persone è composta la squadra?: "))
    machines = int(input("Quante macchine vuoi utilizzare?: "))
    planned_days = int(input("Quanti giorni sono previsti per la raccolta?: "))

    return team_size, machines, planned_days


# --------------------------------------------------
# CONFIGURAZIONE DEL MODELLO
# --------------------------------------------------
# time_per_unit indica quante ore servono per raccogliere 1 Kg.
#
# Esempio:
# Mais manuale = 0.20
# significa che servono 0.20 ore per raccogliere 1 Kg di mais.
#
# machine_multiplier indica quanto produce in più il metodo meccanizzato.
# standard_hours_per_day indica il massimo di ore lavorabili al giorno.
def configuration():
    return {
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
        "machine_multiplier": 3,
        "standard_hours_per_day": 8
    }


# --------------------------------------------------
# DIVIDE IL RACCOLTO TRA PERSONE O MACCHINE
# --------------------------------------------------
# Questa funzione divide una quantità totale tra più unità.
# Le quantità non sono tutte uguali, perché viene usato un peso casuale.
#
# Esempio:
# 100 Kg su 3 persone può diventare:
# Persona 1 = 31 Kg
# Persona 2 = 36 Kg
# Persona 3 = 33 Kg
def split_quantity(total_quantity, units):
    weights = [random.uniform(0.8, 1.2) for _ in range(units)]
    total_weight = sum(weights)

    return [
        round(total_quantity * weight / total_weight, 2)
        for weight in weights
    ]


# --------------------------------------------------
# SIMULA LA PRODUZIONE
# --------------------------------------------------
# Questa funzione calcola:
# - quantità totale raccolta
# - ore totali necessarie
# - quantità giornaliera
# - ore giornaliere per singola unità
# - dettaglio per persona o macchina
#
# La quantità finale viene limitata in modo che:
# Ore/Giorno per unità non superi mai 8.
def simulate_production(products, config, method, units, planned_days):
    results = {}

    standard_hours_per_day = config["standard_hours_per_day"]

    for product, base_quantity in products.items():

        # Recupera il tempo necessario per raccogliere 1 Kg
        time_per_unit = config["time_per_unit"][method][product]

        # Se il metodo è meccanizzato, aumenta la quantità producibile
        if method == "mechanized":
            requested_quantity = base_quantity * config["machine_multiplier"]
        else:
            requested_quantity = base_quantity

        # Calcola il massimo numero di ore disponibili
        # Esempio:
        # 3 giorni * 8 ore * 4 persone = 96 ore disponibili
        max_available_hours = planned_days * standard_hours_per_day * units

        # Calcola la quantità massima raccoglibile entro le ore disponibili
        max_possible_quantity = max_available_hours / time_per_unit

        # La quantità finale non può superare la quantità massima possibile
        final_quantity = min(requested_quantity, max_possible_quantity)

        # Calcola le ore totali necessarie per raccogliere la quantità finale
        total_time = final_quantity * time_per_unit

        # Calcola la quantità totale da raccogliere ogni giorno
        quantity_per_day = final_quantity / planned_days

        # Calcola le ore al giorno per ogni singola persona/macchina
        hours_per_day_per_unit = total_time / (planned_days * units)

        # Divide la quantità totale tra persone o macchine
        quantities_per_unit = split_quantity(final_quantity, units)

        # Calcola le ore totali per ogni persona o macchina
        hours_per_unit = [
            round(qty * time_per_unit, 2)
            for qty in quantities_per_unit
        ]

        # Salva tutti i risultati del prodotto
        results[product] = {
            "Quantità Totale": round(final_quantity, 2),
            "Tempo Totale (ore)": round(total_time, 2),
            "Quantità al Giorno": round(quantity_per_day, 2),
            "Ore al Giorno per unità": round(hours_per_day_per_unit, 2),
            "Quantità per unità": quantities_per_unit,
            "Ore per unità": hours_per_unit
        }

    return results


# --------------------------------------------------
# STAMPA I RISULTATI
# --------------------------------------------------
# Questa funzione stampa:
# - una tabella riepilogativa
# - una tabella di dettaglio per persona o macchina
#
# unit_name può essere:
# - "persona"
# - "macchina"
def print_results(title, results, unit_name, units, planned_days):

    # ------------------------------
    # TABELLA RIEPILOGO
    # ------------------------------
    print(f"\n{title} - RIEPILOGO")
    print("-" * 110)
    print(
        f"{'Prodotto':^12} "
        f"{'Quantità Totale':^18} "
        f"{'Ore Totali':^15} "
        f"{'Kg/Giorno':^15} "
        f"{'Ore/Giorno per unità':^22}"
    )
    print("-" * 110)

    for product, data in results.items():
        print(
            f"{product:^12} "
            f"{data['Quantità Totale']:^18.2f} "
            f"{data['Tempo Totale (ore)']:^15.2f} "
            f"{data['Quantità al Giorno']:^15.2f} "
            f"{data['Ore al Giorno per unità']:^22.2f}"
        )

    # ------------------------------
    # TABELLA DETTAGLIO
    # ------------------------------
    # La tabella di dettaglio viene stampata solo se ci sono più unità.
    # Esempio:
    # più persone oppure più macchine.
    if units > 1:
        print(f"\n{title} - DETTAGLIO PER {unit_name.upper()}")
        print("-" * 120)
        print(
            f"{unit_name.capitalize():^12} "
            f"{'Prodotto':^12} "
            f"{'Kg Totali':^15} "
            f"{'Ore Totali':^15} "
            f"{'Kg/Giorno':^15} "
            f"{'Ore/Giorno':^15}"
        )
        print("-" * 120)

        for i in range(units):
            for product, data in results.items():

                # Calcola quanto raccoglie ogni persona/macchina al giorno
                quantity_per_day_unit = data["Quantità per unità"][i] / planned_days

                # Calcola quante ore lavora ogni persona/macchina al giorno
                hours_per_day_unit = data["Ore per unità"][i] / planned_days

                unit_label = f"{unit_name.capitalize()} {i + 1}"

                print(
                    f"{unit_label:^12} "
                    f"{product:^12} "
                    f"{data['Quantità per unità'][i]:^15.2f} "
                    f"{data['Ore per unità'][i]:^15.2f} "
                    f"{quantity_per_day_unit:^15.2f} "
                    f"{hours_per_day_unit:^15.2f}"
                )


# --------------------------------------------------
# PROGRAMMA PRINCIPALE
# --------------------------------------------------
# Qui viene eseguito il programma:
# 1. genera le quantità
# 2. carica la configurazione
# 3. chiede i parametri all'utente
# 4. calcola produzione manuale
# 5. calcola produzione meccanizzata
# 6. stampa i risultati
products = generate_quantities()
config = configuration()

team_size, machines, planned_days = get_initial_parameters()

manual_results = simulate_production(
    products,
    config,
    "manual",
    team_size,
    planned_days
)

mechanized_results = simulate_production(
    products,
    config,
    "mechanized",
    machines,
    planned_days
)

print_results(
    "Produzione Manuale",
    manual_results,
    "persona",
    team_size,
    planned_days
)

print_results(
    "Produzione Meccanizzata",
    mechanized_results,
    "macchina",
    machines,
    planned_days
)
