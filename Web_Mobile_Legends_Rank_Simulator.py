######## Import Libraries ###################################################################################################################################################################

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
from scipy.optimize import curve_fit

######## Reference Data ###################################################################################################################################################################

rank_dict_starting_values = {
    "Warrior": -112,
    "Elite": -103,
    "Master": -91,
    "Grandmaster": -75,
    "Epic": -50,
    "Legend": -25,
    "Mythic": 0,
    "Mythical Honor": 0,
    "Mythical Glory": 0,
    "Mythical Immortal": 0
}

rank_division_starting_values_above_master = {
    "Mythic": 0,
    "I": 20,
    "II": 15,
    "III": 10,
    "IV": 5,
    "V": 0
}

rank_division_starting_values_above_elite = {
    "I": 12,
    "II": 8,
    "III": 4,
    "IV": 0
}

rank_division_starting_values_above_warrior = {
    "I": 8,
    "II": 4,
    "III": 0,
}

rank_division_starting_values_warrior = {
    "I": 6,
    "II": 3,
    "III": 0,
}

rank_dict = {
    "Warrior": [["III", "II", "I"], 0, 3],
    "Elite": [["III", "II", "I"], 0, 4],
    "Master": [["IV", "III", "II", "I"], 0, 4],
    "Grandmaster": [["V", "IV", "III", "II", "I"], 0, 5],
    "Epic": [["V", "IV", "III", "II", "I"], 0, 5],
    "Legend": [["V", "IV", "III", "II", "I"], 0, 5],
    "Mythic": [["Mythic"], 0, 24],
    "Mythical Honor": [["Mythic"], 25, 49],
    "Mythical Glory": [["Mythic"], 50, 99],
    "Mythical Immortal": [["Mythic"], 100, 5000]
}

######## Functions ###################################################################################################################################################################

def Determine_Result (wr, stars, star_raising, star_raising_cap, max_star_raising_per_game, star_protection, star_protection_cap, max_star_protection_per_game, games_won):
    if (rnd.random() < wr): # win
        games_won += 1
        stars += 1
        star_raising += max_star_raising_per_game * wr
        if star_raising >= star_raising_cap:
            star_raising -= star_raising_cap
            stars += 1

    else: # loss              
        stars -= 1
        star_protection += max_star_protection_per_game * wr
        if star_protection >= star_protection_cap:
            star_protection -= star_protection_cap
            stars += 1

    return stars, star_raising, star_protection, games_won

def rational_model (x, a, b, c):
    return a / (x - b) + c

def rank_selector (major_rank, division, stars, column_number):

    major_rank = st.selectbox(
        'Rank',
        options = list(rank_dict.keys()),
        key=f"starting_major_rank_{column_number}"
    )
        
    division = st.radio(
        'Division',
        options = rank_dict.get(major_rank)[0],
        key=f"starting_division_rank_{column_number}",
        horizontal=True
    )
    
    if major_rank in ["Mythical Immortal"]:
        stars = st.number_input(
            "Stars",
            value=100,
            min_value=100,    
            max_value=5000      
        )
        
    elif major_rank in ["Mythic","Mythical Honor","Mythical Glory"]:
        stars = st.slider(
            "Stars",
            min_value=rank_dict.get(major_rank)[1],
            max_value=rank_dict.get(major_rank)[2],
            key=f"starting_minor_rank_{column_number}"
        )

    else:
        stars = st.radio(
            "Stars",
            options = range(rank_dict.get(major_rank)[1], rank_dict.get(major_rank)[2] + 1),
            key=f"starting_minor_rank_{column_number}",
            horizontal=True
        )

    return major_rank, division, stars

def determine_stars (rank, division, stars):
    if rank in ["Warrior"]:
        stars_from_rank = rank_dict_starting_values.get(rank)
        stars_from_division = rank_division_starting_values_warrior.get(division)
    elif rank in ["Elite"]:
        stars_from_rank = rank_dict_starting_values.get(rank)
        stars_from_division = rank_division_starting_values_above_warrior.get(division)
    elif rank in ["Master"]:
        stars_from_rank = rank_dict_starting_values.get(rank)
        stars_from_division = rank_division_starting_values_above_elite.get(division)        
    else:
        stars_from_rank = rank_dict_starting_values.get(rank)
        stars_from_division = rank_division_starting_values_above_master.get(division)
        
    return stars_from_rank + stars_from_division + stars

###################################################################################################################################################################

def simulation_1 (
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
):
    plt.rcParams['text.color'] = graph_colour         # For text (titles, labels, etc.)
    plt.rcParams['axes.labelcolor'] = graph_colour    # For axis labels
    plt.rcParams['xtick.color'] = graph_colour        # For x-axis ticks
    plt.rcParams['ytick.color'] = graph_colour        # For y-axis ticks
    plt.rcParams['axes.edgecolor'] = graph_colour     # For axis borders
    plt.rcParams['figure.facecolor'] = 'none'   # Transparent figure background
    plt.rcParams['axes.facecolor'] = 'none'     # Transparent axes background

    # This simulation assumes you actually are able to play at the level that you are simulating.

    win_rate_list = [] # list of win rates, x values of the final plot
    actual_win_rate_list = []
    games_to_target = [] # list of games to target stars, y value of the final plot

    win_rate = np.linspace(min_win_rate,max_win_rate, how_many_different_winrates)

    simulation_1_player_runs_graph = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_1_player_runs_graph.patch.set_alpha(0.0)
    ax1 = simulation_1_player_runs_graph.add_subplot(111)

    simulation_1_game_distribution_graph = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_1_game_distribution_graph.patch.set_alpha(0.0)
    ax2 = simulation_1_game_distribution_graph.add_subplot(111)

    for winrate in win_rate:

        wr = winrate / 100
        all_plotting_values = []

        for _ in range(0,simulation1_number_of_attempts_per_win_rate):

            plotting_values = []

            # Player Variables
            games = 0
            stars = starting_rank
            star_raising = 0  
            star_protection = 0
            games_won = 0
            over_number_of_interested_games = False
            
            # Mythic Variables
            entered_mythic_once = False # Checks if you need to go through trial
            mythic_trial_matches = 0 # These are the 10 matches that you get
            mythic_wins = 0 
            mythic_extra_stars = 0 # You can only get up to 5 extra start from these

            while (stars < target_stars and over_number_of_interested_games == False):
                
                if (games >= max_games_to_simulate):
                    over_number_of_interested_games = True

                games += 1

                if stars >= 0 and entered_mythic_once == False:
                    mythic_trial_matches += 1
                    
                    if (rnd.random() < wr):
                        games_won += 1
                        mythic_wins += 1
                        if mythic_extra_stars < 5:
                            mythic_extra_stars += 1

                    if mythic_trial_matches == 10:
                        entered_mythic_once = True
                        stars += mythic_wins + mythic_extra_stars

                else:
                    stars, star_raising, star_protection, games_won = Determine_Result (wr, stars, star_raising, star_raising_cap, max_star_raising_per_game, star_protection, star_protection_cap, max_star_protection_per_game, games_won)

                plotting_values.append([games, stars])
            
            if (not(over_number_of_interested_games)):
                win_rate_list.append(winrate)
                actual_win_rate_list.append(games_won/games*100)
                games_to_target.append(games)

            all_plotting_values.append(plotting_values)
        
        list_of_max_number_of_games = [max(item[0] for item in run) for run in all_plotting_values]

        sorted_indices = np.argsort(list_of_max_number_of_games)
        median_index = sorted_indices[len(sorted_indices) // 2]
        median_run = all_plotting_values[median_index]
        median_games = [item[0] for item in median_run]
        median_stars = [item[1] for item in median_run]

        ax1.plot(median_games, median_stars, label=f'{winrate:.1f}% win rate played an average of {max(median_games)} games')

    if show_player_Graph == True:
        ax1.grid(True)
        ax1.set_title(f"Number of Games Required to Return to {target_stars} stars")
        ax1.axhline(target_stars, color='r', label=f'{target_stars} stars threshold')
        ax1.set_xlabel("Number of games")
        ax1.set_ylabel("Number of stars")
        if (show_player_Legend == True): ax1.legend()

    if(len(games_to_target) != 0):

        # Chat GPT Generated 
        ax2.scatter(win_rate_list, games_to_target, label='Data per Win Rate')
        ax2.scatter(actual_win_rate_list, games_to_target, label='Actual data per Adjusted Win Rate')

        # Your data
        x_data = np.array(actual_win_rate_list)
        y_data = np.array(games_to_target)

        # Fit the model
        params, _ = curve_fit(rational_model, x_data, y_data, p0=[starting_param_a, starting_param_b, starting_param_c], maxfev=10000)  # p0 is the initial guess

        # Generate smooth curve
        x_fit = np.linspace(min(x_data), max(x_data), 500)
        y_fit = rational_model(x_fit, *params)
        ax2.plot(x_fit, y_fit, color='green', label=f'Best Rational Fit: {params[0]:.2f}/(x-{params[1]:.2f})+{params[2]:.2f}')

        ax2.set_title(f"Win Rate vs Number of Games Needed for {target_stars} stars")
        ax2.set_xlabel("Win Rate (%)")
        ax2.set_ylabel("Number of games")
        ax2.grid(True)
        ax2.legend()

    else:
        st.write(f"Apologies, but for the chosen range between {min_win_rate}% and {max_win_rate}%, none of the attempts have managed to reach {target_stars} stars within {max_games_to_simulate} games")

    return simulation_1_player_runs_graph, simulation_1_game_distribution_graph
###################################################################################################################################################################

def simulation_2 (
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
):
    plt.rcParams['text.color'] = graph_colour         # For text (titles, labels, etc.)
    plt.rcParams['axes.labelcolor'] = graph_colour    # For axis labels
    plt.rcParams['xtick.color'] = graph_colour        # For x-axis ticks
    plt.rcParams['ytick.color'] = graph_colour        # For y-axis ticks
    plt.rcParams['axes.edgecolor'] = graph_colour     # For axis borders
    plt.rcParams['figure.facecolor'] = 'none'   # Transparent figure background
    plt.rcParams['axes.facecolor'] = 'none'     # Transparent axes background

    simulation_2_player_runs_graph = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_2_player_runs_graph.patch.set_alpha(0.0)
    ax1 = simulation_2_player_runs_graph.add_subplot(111)

    simulation_2_game_distribution_graph = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_2_game_distribution_graph.patch.set_alpha(0.0)
    ax2 = simulation_2_game_distribution_graph.add_subplot(111)

    simulation_2_games_histogram = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_2_games_histogram.patch.set_alpha(0.0)
    ax3 = simulation_2_games_histogram.add_subplot(111)

    simulation_2_win_rate_histogram = plt.figure(figsize=(figure_size_x, figure_size_y))
    simulation_2_win_rate_histogram.patch.set_alpha(0.0)
    ax4 = simulation_2_win_rate_histogram.add_subplot(111)

    # This simulation assumes you actually are able to play at the level that you are simulating.

    actual_win_rate_list = []
    games_to_target = [] # list of games to target stars, y value of the final plot

    for iterator in range (0, simulation2_number_of_attempts):

        wr = expected_season_end_win_rate / 100

        plotting_values = []

        # Player Variables
        games = 0
        stars = starting_rank
        star_raising = 0  
        star_protection = 0
        games_won = 0
        over_number_of_interested_games = False
        
        # Mythic Variables
        entered_mythic_once = False # Checks if you need to go through trial
        mythic_trial_matches = 0 # These are the 10 matches that you get
        mythic_wins = 0 
        mythic_extra_stars = 0 # You can only get up to 5 extra start from these

        while (stars < target_stars and over_number_of_interested_games == False):
            
            if (games >= max_games_to_simulate):
                over_number_of_interested_games = True

            games += 1

            if stars >= 0 and entered_mythic_once == False:
                mythic_trial_matches += 1
                
                if (rnd.random() < wr):
                    games_won += 1
                    mythic_wins += 1
                    if mythic_extra_stars < 5:
                        mythic_extra_stars += 1

                if mythic_trial_matches == 10:
                    entered_mythic_once = True
                    stars += mythic_wins + mythic_extra_stars

            else:
                stars, star_raising, star_protection, games_won = Determine_Result (wr, stars, star_raising, star_raising_cap, max_star_raising_per_game, star_protection, star_protection_cap, max_star_protection_per_game, games_won)

            plotting_values.append([games, stars])
        
        if (not(over_number_of_interested_games)):
            actual_win_rate_list.append(games_won/games*100)
            games_to_target.append(games)

        x = [item[0] for item in plotting_values]
        y = [item[1] for item in plotting_values]
        ax1.plot(x, y,color=graph_colour)

    if show_player_Graph == True:
        ax1.grid(True)
        ax1.set_title(f"Number of Games Required to Return to {target_stars} stars")
        ax1.axhline(target_stars, color='r', label=f'{target_stars} stars threshold')
        ax1.set_xlabel("Number of games")
        ax1.set_ylabel("Number of stars")   

    average_games_to_target = 100000000

    if(len(games_to_target) != 0):

        # Chat GPT Generated 
        ax2.scatter(actual_win_rate_list, games_to_target, label='Actual data per Adjusted Win Rate')

        # Your data
        x_data = np.array(actual_win_rate_list)
        y_data = np.array(games_to_target)

        # Fit the model
        params, _ = curve_fit(rational_model, x_data, y_data, p0=[starting_param_a, starting_param_b, starting_param_c], maxfev=10000)  # p0 is the initial guess
        average_games_to_target = rational_model(expected_season_end_win_rate, *params)

        # Generate smooth curve
        x_fit = np.linspace(min(x_data), max(x_data), 500)
        y_fit = rational_model(x_fit, *params)
        ax2.plot(x_fit, y_fit, color='green', label=f'Best Rational Fit: {params[0]:.2f}/(x-{params[1]:.2f})+{params[2]:.2f}')

        ax2.set_title(f"Win Rate vs Number of Games Needed for {target_stars} stars")
        ax2.set_xlabel("Win Rate (%)")
        ax2.set_ylabel("Number of games")
        ax2.grid(True)
        ax2.legend()

        # Histogram for expected win rate 

        ax3.hist(games_to_target, bins= 1 if len(games_to_target) < histogram_bin else histogram_bin)
        ax3.set_xlabel(f'Number of games to {target_stars} stars')
        ax3.set_ylabel('Frequency')
        ax3.set_title(f"You need an average of {average_games_to_target:.0f} games to reach {target_stars} stars with {expected_season_end_win_rate:.1f}% win rate starting from {starting_rank} stars")

        ax4.hist(actual_win_rate_list, bins= 1 if len(actual_win_rate_list) < histogram_bin else histogram_bin)
        ax4.set_xlabel(f'Win Rate after reaching {target_stars} stars / %')
        ax4.set_ylabel('Frequency')
        ax4.set_title(f"This is the distribution of win rate after you reach {target_stars} stars playing as a {expected_season_end_win_rate:.1f}% wr player")

    return simulation_2_player_runs_graph, simulation_2_game_distribution_graph, simulation_2_games_histogram, simulation_2_win_rate_histogram, average_games_to_target

###################################################################################################################################################################
