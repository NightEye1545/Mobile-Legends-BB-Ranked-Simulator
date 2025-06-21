import streamlit as st
from Web_Mobile_Legends_Rank_Simulator import simulation_1, simulation_2

def main():

    st.title("Mobile Legends Ranked Simulator")

    st.markdown("---")

    st.subheader("Adjust the parameters below, then click Run Simulation.")

    # --- Simulation Path ---
    simulation_path = st.selectbox(
        "Choose Simulation Type",
        options=[1, 2],
        format_func=lambda x: f"Simulation {x}"
    )

    col1, col2= st.columns(2)
    
    with col1:
        with st.container():
            starting_rank = st.number_input("Starting Stars", value=-29)
    with col2:
        with st.container():
            target_stars = st.number_input("Target Stars", value=100)

    expected_season_end_win_rate = st.slider(
        "Expected Season End Win Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.01,
        format="%.1f"
    )    

    st.markdown("---")

    match simulation_path:

        case 1:

            win_rate_range = st.slider(
                "Simulated Win Rate Range (%)",
                0, 100, (50, 80)
            )

            min_win_rate, max_win_rate = win_rate_range

            col1, col2 = st.columns(2)
            with col1:
                simulation1_number_of_attempts_per_win_rate = st.number_input("Number of Attempts per Win Rate", value=1000)
            with col2:
                how_many_different_winrates = st.number_input("Number of Win Rate to Simulate", value=50)

        case 2:
            simulation2_number_of_attempts = st.number_input("Number of Runs", value=100)

    st.markdown("---")

    # Sidebar for Additional Settings
    with st.sidebar:

        st.header("Additional Simulation Controls")

        show_player_Legend = st.checkbox("Show Legend on Graph", value=True)
        show_player_Graph = st.checkbox("Show Player Graph", value=True)
        max_games_to_simulate = st.number_input("Max Games to Simulate per Run", value=2500)
        histogram_bin = st.number_input("Histogram Bin Count", value=50)
        
        with st.expander("Advanced Game Settings", expanded = False):
            star_raising_cap = st.number_input("Star Raising Cap", value=1000)
            max_star_raising_per_game = st.number_input("Max Star Raising per Game", value=200)
            max_star_protection_per_game = st.number_input("Max Star Protection per Game", value=200)
            star_protection_cap = st.number_input("Star Protection Cap", value=1000)

    if st.button("Run Simulation"):

        match simulation_path:

            case 1:

                simulation_1(
                    simulation1_number_of_attempts_per_win_rate,
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

            case 2:

                simulation_2(
                    simulation2_number_of_attempts,
                    expected_season_end_win_rate,
                    starting_rank,
                    target_stars,
                    star_raising_cap,
                    max_star_raising_per_game,
                    max_star_protection_per_game,
                    star_protection_cap,
                    show_player_Graph,
                    max_games_to_simulate,
                    histogram_bin
                )

            case _:

                st.write("Unknown simulation type selected.")

if __name__ == "__main__":
    main()