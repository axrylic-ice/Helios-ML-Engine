from data_ingestion.scheduler.jobs import collect_all_data

def run_tests():

    data = collect_all_data()

    print("\n===== BAYSE =====")
    print(data.get("bayse"))

    print("\n===== FX GLOBAL =====")
    print(data.get("fx_global"))

    print("\n===== NEWS =====")
    print(data.get("news"))

    print("\n===== NAIRATODAY =====")
    print(data.get("naira_local"))
    
    print("\n===== POLY =====")
    print(data.get("polymarket"))
    
    print("\n===== eia =====")
    print(data.get("eia"))
    
if __name__ == "__main__":
    run_tests()