import streamlit as st
from Web_Mobile_Legends_Rank_Simulator import simulation_1, simulation_2, rank_selector, determine_stars
from user_guide import user_guide

######## Cache clearing ###################################################################################################################

if "cache_cleared" not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["cache_cleared"] = True

######## Main Application ###################################################################################################################

def main():

######## Title settings ###################################################################################################################

    st.title("Mobile Legends Ranked Simulator")

    st.markdown("---")

    st.subheader("👈 Need help? Expand the sidebar for a quick guide.")

    st.markdown("---")

    st.subheader("Adjust the parameters below, then click Run Simulation.")

    # Simulation Path

    simulation_label = st.selectbox(
        "Choose Simulation Type",
        options=["Simulate Single Win Rate", "Simulate Range of Win Rates"],
        index=0
    )

######## Rank selection  ###################################################################################################################

    starting_major_rank = "Epic"
    starting_division = "I"
    starting_minor_rank = 1

    target_major_rank = "Mythical Immortal"
    target_division = ""
    target_minor_rank = 100

    col1, col2 = st.columns(2)

    with col1:
        column_number = 1
        with st.expander("Starting Rank", expanded=True):
            starting_major_rank, starting_division, starting_minor_rank = rank_selector(starting_major_rank, starting_division, starting_minor_rank, column_number)

    with col2:
        column_number = 2
        with st.expander("Target Rank", expanded=True):
            target_major_rank, target_division, target_minor_rank = rank_selector(target_major_rank, target_division, target_minor_rank, column_number)

    starting_rank = determine_stars(starting_major_rank, starting_division, starting_minor_rank)
    target_stars = determine_stars(target_major_rank, target_division, target_minor_rank)

    can_run_simulation = False
    if starting_rank < target_stars: 
        can_run_simulation = True
    else: 
        st.warning("Target Rank must be higher than Starting Rank")

    st.markdown("---")

######## Simulation variables ###################################################################################################################

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
                
            simulation2_number_of_attempts = st.number_input(
                "Number of Runs",
                value=100,
                min_value=1,
                max_value=25000
            )

    st.markdown("---")

######## Sidebar settings ###################################################################################################################

    with st.sidebar:

        user_guide()

        with st.expander("⚙️ Additional Simulation Controls", expanded = False):

            max_games_to_simulate = st.number_input("Max Games to Simulate per Run", value=2500)

            with st.expander("📈 Graph Settings", expanded = False):
                
                show_player_Legend = st.checkbox("Show Legend on Graph", value=True)
                show_player_Graph = st.checkbox("Show Player Graph", value=True)

                graph_colour = st.radio(
                    'Graph Theme Colour',
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
            
            with st.expander("🧪 Advanced Game Settings", expanded = False):
                star_raising_cap = st.number_input("Star Raising Cap", value=1000)
                max_star_raising_per_game = st.number_input("Max Star Raising per Game", value=200)
                max_star_protection_per_game = st.number_input("Max Star Protection per Game", value=200)
                star_protection_cap = st.number_input("Star Protection Cap", value=1000)
                st.markdown("These are the fitting parameters for")
                st.latex(r"\frac{a}{x - b} + c")
                starting_param_a = st.number_input("Starting Parameter a", value=4000.00)
                starting_param_b = st.number_input("Starting Parameter b", value=45.50)
                starting_param_c = st.number_input("Starting Parameter c", value=10.00)

######## Simulation settings ###################################################################################################################

    if can_run_simulation == True:

        if st.button("Run Simulation"):

            st.markdown("---")

            match simulation_label:

                ######## Simulation: Range of Win Rates ###################################################################################################################

                case "Simulate Range of Win Rates":

                    st.write("Simulation 1: Series of Win Rates")
                    
                    with st.spinner("Running simulation..."):

                        range_wr_player_run_graph, range_wr_game_distribution_graph = simulation_1(
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

                    st.success("Simulation complete!")

                    st.pyplot(range_wr_player_run_graph)
                    st.pyplot(range_wr_game_distribution_graph)

                ######## Simulation: Single Win Rate ###################################################################################################################

                case "Simulate Single Win Rate":
                    
                    st.write("Simulation 2: Single Win Rate Analysis")

                    with st.spinner("Running Simulation..."):
                        single_wr_player_run_graph, single_wr_game_distribution_graph, single_wr_games_histogram, single_wr_winrate_histogram, average_games_to_target = simulation_2(
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

                    st.success("Simulation complete!")
                    
                    if average_games_to_target > max_games_to_simulate:
                        st.markdown(
                            f"Apologies, no simulated runs managed to reach "
                            f"**{target_major_rank} {target_division} {target_minor_rank}** stars from "
                            f"**{starting_major_rank} {starting_division} {starting_minor_rank}** stars within "
                            f"**{max_games_to_simulate}** games."
                        )
                    else:
                        st.markdown(
                            f"You need an average of **{average_games_to_target:.0f}** games to reach "
                            f"**{target_major_rank} {target_division} {target_minor_rank}** stars from "
                            f"**{starting_major_rank} {starting_division} {starting_minor_rank}** stars."
                        )

                        with st.spinner("Generating Graphs..."):
                            st.pyplot(single_wr_player_run_graph)
                            st.pyplot(single_wr_game_distribution_graph)
                            st.pyplot(single_wr_games_histogram)
                            st.pyplot(single_wr_winrate_histogram) 
                
                ######## Simulation not found ###################################################################################################################

                case _:

                    st.write("Invalid Simulation, Check Simulation Selection and Ensure Target Rank is Higher than Starting Rank")

if __name__ == "__main__":
    main()