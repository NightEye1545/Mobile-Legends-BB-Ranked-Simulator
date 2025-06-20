import streamlit as st
from Web_Mobile_Legends_Rank_Simulator import simulation_1, simulation_2

def main():
    st.title("Star Progression Simulator")

    st.markdown("Adjust the parameters below, then click **Run Simulation**.")

    # --- Simulation Path ---
    simulation_path = st.selectbox(
        "Choose Simulation Type",
        options=[1, 2],
        format_func=lambda x: f"Simulation {x}"
    )

    # --- Main Parameters ---
    expected_season_end_win_rate = st.slider("Expected Win Rate (%)", 0, 100, 50)
    starting_rank = st.number_input("Starting Stars", value=-29)
    target_stars = st.number_input("Target Stars", value=100)

    # --- Simulation Settings ---
    simulation1_number_of_attempts_per_win_rate = st.number_input("Simulation 1: Attempts per Win Rate", value=1000)
    simulation2_number_of_attempts = st.number_input("Simulation 2: Attempts", value=100)
    histogram_bin = st.number_input("Histogram Bin Count", value=50)

    # --- Game Mechanics ---
    star_raising_cap = st.number_input("Star Raising Cap", value=1000)
    max_star_raising_per_game = st.number_input("Max Star Raising per Game", value=200)
    max_star_protection_per_game = st.number_input("Max Star Protection per Game", value=200)
    star_protection_cap = st.number_input("Star Protection Cap", value=1000)

    # --- Graph Settings ---
    show_player_Legend = st.checkbox("Show Legend on Graph", value=True)
    show_player_Graph = st.checkbox("Show Player Graph", value=True)
    max_games_to_simulate = st.number_input("Max Games to Simulate", value=10000)
    min_win_rate = st.slider("Minimum Simulated Win Rate (%)", 0, 100, 90)
    max_win_rate = st.slider("Maximum Simulated Win Rate (%)", 0, 100, 100)
    how_many_different_winrates = st.number_input("Different Win Rates to Simulate", value=50)

    # --- Run Simulation ---
    if st.button("Run Simulation"):
        if simulation_path == 1:
            simulation_1(
                simulation1_number_of_attempts_per_win_rate,
                histogram_bin,
                simulation_path,
                expected_season_end_win_rate,
                starting_rank,
                target_stars,
                star_raising_cap,
                max_star_raising_per_game,
                max_star_protection_per_game,
                star_protection_cap,
                show_player_Legend,
                show_player_Graph,
                max_games_to_simulate,
                min_win_rate,
                max_win_rate,
                how_many_different_winrates
            )
        elif simulation_path == 2:
            simulation_2(
                simulation2_number_of_attempts,
                simulation_path,
                expected_season_end_win_rate,
                starting_rank,
                target_stars,
                star_raising_cap,
                max_star_raising_per_game,
                max_star_protection_per_game,
                star_protection_cap,
                show_player_Legend,
                show_player_Graph,
                max_games_to_simulate,
                min_win_rate,
                max_win_rate,
                how_many_different_winrates
            )

if __name__ == "__main__":
    main()
