import streamlit as st
from Web_Mobile_Legends_Rank_Simulator import simulation_1, simulation_2

##################
# Reference Data #
##################

rank_dict = {
    "Warrior": (0,3),
    "Elite": (0,4),
    "Master": (0,4),
    "Grandmaster": (0,5),
    "Epic": (0,5),
    "Legend": (0,5),
    "Mythic": (0,24),
    "Mythical Honor": (25,49),
    "Mythical Glory": (50,99),
    "Mythical Immortal": (100,1000)
}

def main():

    st.title("Mobile Legends Ranked Simulator")

    st.markdown("---")

    st.subheader("Adjust the parameters below, then click Run Simulation.")

    # --- Simulation Path ---
    simulation_label = st.selectbox(
        "Choose Simulation Type",
        options=["Simulate Range of Win Rates", "Simulate Single Win Rate"]
    )

    col1, col2 = st.columns(2)

    with col1:
        starting_major_rank = st.selectbox(
            'Starting Rank',
            options = list(rank_dict.keys()),
        )
        
        if starting_major_rank != "Mythical Immortal":
            starting_minor_rank = st.selectbox(
                "Number of Stars",
                options = range(rank_dict.get(starting_major_rank)[0], rank_dict.get(starting_major_rank)[1] + 1)
            )
        
        else:
            starting_minor_rank = st.number_input(
                "Starting Stars",
                value=100,
                min_value=100,    
                max_value=5000      
            )

    with col2:
        target_major_rank = st.selectbox(
            'Target Rank',
            options = list(rank_dict.keys()),
        )
        
        if target_major_rank != "Mythical Immortal":
            target_minor_rank = st.selectbox(
                "Number of Stars",
                options = range(rank_dict.get(target_major_rank)[0], rank_dict.get(target_major_rank)[1] + 1)
            )
        
        else:
            target_minor_rank = st.number_input(
                "Starting Stars",
                value=100,
                min_value=100,    
                max_value=5000      
            )
    
    starting_rank = 0
    target_stars = 0

    col1, col2= st.columns(2)
    
    with col1:
        with st.container():
            starting_rank = st.number_input("Starting Stars", value=-29)
    with col2:
        with st.container():
            target_stars = st.number_input("Target Stars", value=100) 

    st.markdown("---")

    match simulation_label:

        case "Simulate Range of Win Rates":

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

        case "Simulate Single Win Rate":

            expected_season_end_win_rate = st.slider(
                "Expected Season End Win Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=50.0,
                step=0.01,
                format="%.1f"
            )   
                
            simulation2_number_of_attempts = st.number_input("Number of Runs", value=100)

    st.markdown("---")

    # Sidebar for Additional Settings
    with st.sidebar:

        st.header("Additional Simulation Controls")

        max_games_to_simulate = st.number_input("Max Games to Simulate per Run", value=2500)

        with st.expander("Graph Settings", expanded = False):
            
            show_player_Legend = st.checkbox("Show Legend on Graph", value=True)
            show_player_Graph = st.checkbox("Show Player Graph", value=True)

            graph_colour = st.radio(
                'Select the Graph Theme Colour',
                options = ["white","black"]
            )

            figure_size_x = st.slider(
                "Horizontal Figure Size",
                min_value=1,
                max_value=25,
                value=15,
                step=1,
            )    

            figure_size_y = st.slider(
                "Vertical Figure Size",
                min_value=1,
                max_value=25,
                value=10,
                step=1,
            )    

            histogram_bin = st.number_input("Histogram Bin Count", value=30)
        
        with st.expander("Advanced Game Settings", expanded = False):
            star_raising_cap = st.number_input("Star Raising Cap", value=1000)
            max_star_raising_per_game = st.number_input("Max Star Raising per Game", value=200)
            max_star_protection_per_game = st.number_input("Max Star Protection per Game", value=200)
            star_protection_cap = st.number_input("Star Protection Cap", value=1000)
            starting_param_a = st.number_input("Starting Parameter a", value=4000.00)
            starting_param_b = st.number_input("Starting Parameter b", value=45.50)
            starting_param_c = st.number_input("Starting Parameter c", value=10.00)

    if st.button("Run Simulation"):

        st.markdown("---")

        match simulation_label:

            case "Simulate Range of Win Rates":

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
                    how_many_different_winrates,
                    starting_param_a,
                    starting_param_b,
                    starting_param_c,
                    graph_colour,
                    figure_size_x,
                    figure_size_y           
                )

            case "Simulate Single Win Rate":

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
                    histogram_bin,
                    starting_param_a,
                    starting_param_b,
                    starting_param_c,
                    graph_colour,
                    figure_size_x,
                    figure_size_y
                )

            case _:

                st.write("Unknown simulation type selected.")

if __name__ == "__main__":
    main()