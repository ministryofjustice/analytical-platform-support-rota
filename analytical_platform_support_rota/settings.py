google_calendar_api = {
    "client_secret_file": "analytical_platform_support_rota_creds.json",
    "api_name": "calendar",
    "api_version": "v3",
    "scopes": ["https://www.googleapis.com/auth/calendar"],
    "calendar_ids": {
        "dev-1": "c_f2dcb7a498c93027d1a5c50cb15a9d1dc28ac15ae593850d52241704b746542a@group.calendar.google.com",
        "dev-2": "c_dc9ab22c55d7dd6fd1d91ca46ec650d0efc4f128b6ca8769be6400a3c2812522@group.calendar.google.com",
        "prod": "c_c1d6ed6c01045fa38a1e777576e0623c6b1bd38361fcd75e78d75d0f1ecccc58@group.calendar.google.com",
    },
    "calendar": "prod",
}

support_team = {
    "start_cycle_with": "list_2",
    "list_1": [
        "Abdel",
        "John",
        "Julia",
        "Richard",
        "Ross",
        "Yikang",
    ],
    "list_2": [
        "Andy",
        "Bogdan",
        "Brian",
        "Louise",
        "Tom",
    ],
}


date_range = {
    "start_date": "2023-01-18",
    "n_cycles": 1,
}
