
import random


# --------------------------------------------------
# RACCOGLIE I PARAMETRI INSERITI DALL'UTENTE
# --------------------------------------------------
def get_initial_parameters():

    print("\nINSERIMENTO INFORMAZIONI PER LA RACCOLTA")
    print("-" * 50)

    team_size = int(input("Da quante persone è composta la squadra?: "))
    machines = int(input("Quante macchine vuoi utilizzare?: "))
    planned_days = int(input("Quanti giorni sono previsti per la raccolta?: "))

    hectares = {
        "Mais": float(input("Quanti ettari di mais?: ")),
        "Pomodori": float(input("Quanti ettari di pomodori?: ")),
        "Patate": float(input("Quanti ettari di patate?: "))
    }

    return team_size, machines, planned_days, hectares


# --------------------------------------------------
# CONFIGURAZIONE DEL MODELLO
# --------------------------------------------------
def configuration():

    return {
        "yield_per_hectare": {
            "Mais": 80,
            "Pomodori": 60,
            "Patate": 70
        },

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
# GENERA LE QUANTITÀ DI RACCOLTO
# --------------------------------------------------
def generate_quantities(hectares, config):

    products = {}

    for product, area in hectares.items():

        base_yield = config["yield_per_hectare"][product]

        variability = random.uniform(0.8, 1.2)

        products[product] = round(
            area * base_yield * variability,
2
        )

    return products


# --------------------------------------------------
# DIVIDE IL RACCOLTO TRA UNITÀ OPERATIVE
# --------------------------------------------------
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
def simulate_production(
    products,
    config,
    method,
    units,
    planned_days,
    hectares
):

    results = {}

    standard_hours_per_day = config["standard_hours_per_day"]

    for product, base_quantity in products.items():

        time_per_unit = config["time_per_unit"][method][product]

        base_yield = config["yield_per_hectare"][product]

        cultivated_hectares = hectares[product]

        # Metodo meccanizzato
        if method == "mechanized":

            requested_quantity = (
                base_quantity *
                config["machine_multiplier"]
            )

        else:

            requested_quantity = base_quantity

        # Ore massime disponibili
        max_available_hours = (
            planned_days *
            standard_hours_per_day *
            units
        )

        # Quantità massima raccoglibile
        max_possible_quantity = (
            max_available_hours /
            time_per_unit
        )

        # Quantità finale lavorabile
        final_quantity = min(
            requested_quantity,
            max_possible_quantity
        )

        # Calcoli principali
        total_time = (
            final_quantity *
            time_per_unit
        )

        quantity_per_day = (
            final_quantity /
            planned_days
        )

        hours_per_day_per_unit = (
            total_time /
            (planned_days * units)
        )

        # Divisione tra unità
        quantities_per_unit = split_quantity(
            final_quantity,
            units
        )

        hours_per_unit = [

            round(qty * time_per_unit, 2)

            for qty in quantities_per_unit
        ]

        # Salvataggio risultati
        results[product] = {

            "Ettari": cultivated_hectares,

            "Resa per Ettaro": base_yield,

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

            "Ore per unità": hours_per_unit
        }

    return results


# --------------------------------------------------
# STAMPA I RISULTATI
# --------------------------------------------------
def print_results(
    title,
    results,
    unit_name,
    units,
    planned_days
):

    # --------------------------------------------------
    # RIEPILOGO
    # --------------------------------------------------
    print(f"\n{title} - RIEPILOGO")

    print("-" * 95)

    print(

        f"{'Prodotto':<12}"
        f"{'Ettari':>10}"
        f"{'Resa/ha':>12}"
        f"{'Quantità Totale Kg':>22}"
        f"{'Ore Totali':>15}"
        f"{'Kg/Giorno':>15}"
    )

    print("-" * 95)

    for product, data in results.items():

        print(

            f"{product:<12}"
            f"{data['Ettari']:>10.2f}"
            f"{data['Resa per Ettaro']:>12.2f}"
            f"{data['Quantità Totale']:>22.2f}"
            f"{data['Tempo Totale (ore)']:>15.2f}"
            f"{data['Quantità al Giorno']:>15.2f}"
        )

    # --------------------------------------------------
    # DETTAGLIO
    # --------------------------------------------------
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

                quantity_per_day_unit = (

                    data["Quantità per unità"][i] /
                    planned_days
                )

                hours_per_day_unit = (

                    data["Ore per unità"][i] /
                    planned_days
                )

                # Nome unità
                if unit_name == "persona":

                    unit_label = f"Operaio {i + 1}"

                else:

                    unit_label = f"Macchina {i + 1}"

                print(

                    f"{unit_label:<15}"
                    f"{product:<12}"
                    f"{data['Quantità per unità'][i]:>15.2f}"
                    f"{data['Ore per unità'][i]:>15.2f}"
                    f"{quantity_per_day_unit:>15.2f}"
                    f"{hours_per_day_unit:>15.2f}"
                )


# --------------------------------------------------
# PROGRAMMA PRINCIPALE
# --------------------------------------------------

config = configuration()

team_size, machines, planned_days, hectares = (
    get_initial_parameters()
)

products = generate_quantities(
    hectares,
    config
)

manual_results = simulate_production(
    products,
    config,
    "manual",
    team_size,
    planned_days,
    hectares
)

mechanized_results = simulate_production(
    products,
    config,
    "mechanized",
    machines,
    planned_days,
    hectares
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
