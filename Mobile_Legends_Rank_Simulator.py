import numpy as np
import matplotlib.pyplot as plt
import random as rnd
from scipy.optimize import curve_fit

## This is a test line for GIT, never used it properly before.

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

def simulation_1 (
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
):
    print("Simulation 1: Series of Win Rates")
    # This simulation assumes you actually are able to play at the level that you are simulating.

    win_rate_list = [] # list of win rates, x values of the final plot
    actual_win_rate_list = []
    games_to_target = [] # list of games to target stars, y value of the final plot

    win_rate = np.linspace(min_win_rate,max_win_rate, how_many_different_winrates + 1)

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

        plt.plot(median_games, median_stars, label=f'{winrate:.1f}% win rate played an average of {max(median_games)} games')

    if show_player_Graph == True:
        plt.grid(True)
        plt.title(f"Number of Games Required to Return to {target_stars} stars")
        plt.axhline(target_stars, color='r', label=f'{target_stars} stars threshold')
        plt.xlabel("Number of games")
        plt.ylabel("Number of stars")
        if (show_player_Legend == True): plt.legend()
        plt.show()    

    if(len(games_to_target) != 0):

        ################### Chat GPT Generated ##################################################################################################################################################

        plt.scatter(win_rate_list, games_to_target, label='Data per Win Rate')
        plt.scatter(actual_win_rate_list, games_to_target, label='Actual data per Adjusted Win Rate')

        # Your data
        x_data = np.array(actual_win_rate_list)
        y_data = np.array(games_to_target)

        # Fit the model
        params, _ = curve_fit(rational_model, x_data, y_data, p0=[1000, 40, 100])  # p0 is the initial guess

        # Generate smooth curve
        x_fit = np.linspace(min(x_data), max(x_data), 500)
        y_fit = rational_model(x_fit, *params)
        plt.plot(x_fit, y_fit, color='green', label=f'Best Rational Fit: {params[0]}/(x-{params[1]})+{params[2]}')

        plt.title(f"Win Rate vs Number of Games Needed for {target_stars} stars")
        plt.xlabel("Win Rate (%)")
        plt.ylabel("Number of games")
        plt.grid(True)
        plt.legend()
        plt.show()

        ################### Histogram for expected win rate ###########################################################################################################################

        filtered_pairs = [(xv, yv) for xv, yv in zip(win_rate_list, games_to_target) if xv == expected_season_end_win_rate]

        if filtered_pairs:
            filtered_x, filtered_y = zip(*filtered_pairs)
            filtered_x = list(filtered_x)
            filtered_y = list(filtered_y)
            plt.hist(list(filtered_y), bins= 1 if len(filtered_y) < histogram_bin else histogram_bin)
            plt.xlabel(f'Games to {target_stars} stars')
            plt.ylabel('Frequency')
            plt.title(f"You need {rational_model(expected_season_end_win_rate, *params)} games to reach {target_stars} stars with {expected_season_end_win_rate}% win rate starting from {starting_rank} stars")
            plt.show()
        else:
            print(f"You need and average of {rational_model(expected_season_end_win_rate, *params)} games to reach {target_stars} stars with {expected_season_end_win_rate}% win rate, starting from Epic I 1 Star")

    else:
        print(f"Apologies, but for the chosen range between {min_win_rate}% and {max_win_rate}%, none of the attempts have managed to reach {target_stars} stars within {max_games_to_simulate} games")
    
def simulation_2 (
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
):

    print("Simulation 2: Single Win Rate Analysis")

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
        plt.plot(x, y,color='black')

    if show_player_Graph == True:
        plt.grid(True)
        plt.title(f"Number of Games Required to Return to {target_stars} stars")
        plt.axhline(target_stars, color='r', label=f'{target_stars} stars threshold')
        plt.xlabel("Number of games")
        plt.ylabel("Number of stars")
        plt.show()    

    if(len(games_to_target) != 0):

        ################### Chat GPT Generated ##################################################################################################################################################

        plt.scatter(actual_win_rate_list, games_to_target, label='Actual data per Adjusted Win Rate')

        # Your data
        x_data = np.array(actual_win_rate_list)
        y_data = np.array(games_to_target)

        # Fit the model
        params, _ = curve_fit(rational_model, x_data, y_data, p0=[1000, 40, 100])  # p0 is the initial guess

        # Generate smooth curve
        x_fit = np.linspace(min(x_data), max(x_data), 500)
        y_fit = rational_model(x_fit, *params)
        plt.plot(x_fit, y_fit, color='green', label=f'Best Rational Fit: {params[0]}/(x-{params[1]})+{params[2]}')

        plt.title(f"Win Rate vs Number of Games Needed for {target_stars} stars")
        plt.xlabel("Win Rate (%)")
        plt.ylabel("Number of games")
        plt.grid(True)
        plt.legend()
        plt.show()

        ################### Histogram for expected win rate ###########################################################################################################################

        plt.hist(games_to_target, bins= 1 if len(games_to_target) < histogram_bin else histogram_bin)
        plt.xlabel(f'Games to {target_stars} stars')
        plt.ylabel('Frequency')
        plt.title(f"You need {rational_model(expected_season_end_win_rate, *params)} games to reach {target_stars} stars with {expected_season_end_win_rate}% win rate starting from {starting_rank} stars")
        plt.show()

        plt.hist(actual_win_rate_list, bins= 1 if len(actual_win_rate_list) < histogram_bin else histogram_bin)
        plt.xlabel(f'Win Rate after reaching {target_stars} stars / %')
        plt.ylabel('Frequency')
        plt.title(f"This is the distribution of win rate after you reach {target_stars} stars playing if you're a {expected_season_end_win_rate}% wr player")
        plt.show()

    else:
        print(f"Apologies, but for the chosen range between {min_win_rate}% and {max_win_rate}%, none of the attempts have managed to reach {target_stars} stars within {max_games_to_simulate} games")


############# Control Panel ##########################################################################################################################################################

# Global Variables
simulation_path = 2
expected_season_end_win_rate = 55 # what win rate % to figure out how many games to reach the ceiling
starting_rank = -29
target_stars = 100 # 0 stars means zero star in mythic, or 5 start in legend 1

# Simulation 1 Variables
simulation1_number_of_attempts_per_win_rate = 1000 # how many times does a player with a certain win rate need to play?
histogram_bin = 50 # Determines how many paitns in each bar bars of the final esimate histogram you want, only shows if expected_season_end_win_rate is in the simulation range

# Simulation 2 Variables
simulation2_number_of_attempts = 1000

# Game Variables
star_raising_cap = 1000 # 1000 gets you extra star
max_star_raising_per_game = 200
max_star_protection_per_game = 200
star_protection_cap = 1000 # 1000 saves you from losing star

# Player Graph Settings
show_player_Legend = True
show_player_Graph = True
max_games_to_simulate = 10000
min_win_rate = 0
max_win_rate = 100
how_many_different_winrates = 50

################### Simulations ######################################################################################################################################################

match(simulation_path):

    ################### Simulation 1 ######################################################################################################################################################

    case 1: 
        simulation_1 (
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
        
    case 2: 
        simulation_2 (
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

