from ast import match_case
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load datasets
matches_df = pd.read_csv('matches.csv')
deliveries_df = pd.read_csv('deliveries.csv')

# Merge datasets on match_id
combined_df = pd.merge(deliveries_df, matches_df, left_on='match_id', right_on='id')

def app():
    st.title('🏏 IPL Data Analysis Dashboard')
    st.markdown("""
        <style>
        .main { background-color: #f5f5f5; }
        h1 { color: #2c3e50; font-weight: bold; }
        h2, h3 { color: #34495e; }
        </style>
    """, unsafe_allow_html=True)

    # Display data for all seasons together
    st.header('📊 All Seasons Data')
    all_seasons_winning_teams = matches_df['winner'].value_counts()
    st.subheader('🏆 Total Wins by Teams Across All Seasons')
    st.write(all_seasons_winning_teams)

    # Visualize total wins across all seasons
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=all_seasons_winning_teams.values, y=all_seasons_winning_teams.index, palette='coolwarm', ax=ax1)
    ax1.set_title('Total Wins by Teams Across All Seasons', fontsize=22, fontweight='bold', color='#2c3e50')
    ax1.set_xlabel('Number of Wins', fontsize=16, fontweight='bold', color='#34495e')
    ax1.set_ylabel('Teams', fontsize=16, fontweight='bold', color='#34495e')
    ax1.tick_params(axis='x', labelsize=14, labelcolor='#7f8c8d')
    ax1.tick_params(axis='y', labelsize=14, labelcolor='#7f8c8d')
    ax1.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig1)

    # Select a season
    st.header('📅 Season Selection')
    seasons = matches_df['season'].unique()
    selected_season = st.selectbox('Select Season', sorted(seasons))

    # Filter data for the selected season
    season_matches = matches_df[matches_df['season'] == selected_season]
    season_match_ids = season_matches['id']
    season_deliveries = deliveries_df[deliveries_df['match_id'].isin(season_match_ids)]

    # Team Performance Analysis
    st.header(f'📈 Team Performance in {selected_season}')
    team_performance = season_matches['winner'].value_counts()
    st.subheader('🏆 Total Wins by Teams')
    st.write(team_performance)

    # Plot team performance
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=team_performance.values, y=team_performance.index, palette='mako', ax=ax2)
    ax2.set_title(f'Total Wins by Teams in {selected_season}', fontsize=22, fontweight='bold', color='#2c3e50')
    ax2.set_xlabel('Number of Wins', fontsize=16, fontweight='bold', color='#34495e')
    ax2.set_ylabel('Teams', fontsize=16, fontweight='bold', color='#34495e')
    ax2.tick_params(axis='x', labelsize=14, labelcolor='#7f8c8d')
    ax2.tick_params(axis='y', labelsize=14, labelcolor='#7f8c8d')
    ax2.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig2)

    # Batter Performance Analysis
    st.header(f'🏏 Batter Performance in {selected_season}')
    if 'batter' in season_deliveries.columns and 'batsman_runs' in season_deliveries.columns:
        batter_runs = season_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)
        st.subheader('Top 10 Batters by Total Runs')
        st.write(batter_runs.head(10))

        # Plot top batters horizontally with different colors
        fig3, ax3 = plt.subplots(figsize=(14, 8))
        sns.barplot(x=batter_runs.head(10).values, y=batter_runs.head(10).index, palette='Spectral', ax=ax3, orient='h')
        ax3.set_title(f'Top 10 Batters by Runs in {selected_season}', fontsize=22, fontweight='bold', color='#2c3e50')
        ax3.set_xlabel('Total Runs', fontsize=16, fontweight='bold', color='#34495e')
        ax3.set_ylabel('Batter', fontsize=16, fontweight='bold', color='#34495e')
        ax3.tick_params(axis='x', labelsize=14, labelcolor='#7f8c8d')
        ax3.tick_params(axis='y', labelsize=14, labelcolor='#7f8c8d')
        ax3.grid(axis='x', linestyle='--', alpha=0.7)
        st.pyplot(fig3)
    else:
        st.error("Required columns 'batter' or 'batsman_runs' are missing in deliveries.csv")

    # Bowler Performance Analysis
    st.header(f'🎯 Bowler Performance in {selected_season}')
    if 'bowler' in season_deliveries.columns and 'dismissal_kind' in season_deliveries.columns:
        bowler_wickets = season_deliveries[season_deliveries['dismissal_kind'].notna()].groupby('bowler').size().sort_values(ascending=False)
        st.subheader('Top 10 Bowlers by Total Wickets')
        st.write(bowler_wickets.head(10))

        # Plot top bowlers
        fig4, ax4 = plt.subplots(figsize=(14, 8))
        sns.barplot(x=bowler_wickets.head(10).values, y=bowler_wickets.head(10).index, palette='cubehelix', ax=ax4)
        ax4.set_title(f'Top 10 Bowlers by Wickets in {selected_season}', fontsize=22, fontweight='bold', color='#2c3e50')
        ax4.set_xlabel('Total Wickets', fontsize=16, fontweight='bold', color='#34495e')
        ax4.set_ylabel('Bowler', fontsize=16, fontweight='bold', color='#34495e')
        ax4.tick_params(axis='x', labelsize=14, labelcolor='#7f8c8d')
        ax4.tick_params(axis='y', labelsize=14, labelcolor='#7f8c8d')
        ax4.grid(axis='x', linestyle='--', alpha=0.7)
        st.pyplot(fig4)
    else:
        st.error("Required columns 'bowler' or 'dismissal_kind' are missing in deliveries.csv")

    # Venue Performance Analysis
    st.header('📍 Venue Performance Analysis')
    venues = matches_df['venue'].unique()
    selected_venue = st.selectbox('Select Venue', sorted(venues))

    # Filter data for the selected venue
    venue_matches = matches_df[matches_df['venue'] == selected_venue]

    # Display matches played at the selected venue
    st.subheader(f'Matches Played at {selected_venue}')
    st.write(venue_matches[['team1', 'team2', 'winner']])

    # Visualize winning teams at the selected venue
    venue_winning_teams = venue_matches['winner'].value_counts().astype(int)  # Ensure integer values
    fig5, ax5 = plt.subplots(figsize=(14, 8))
    sns.barplot(x=venue_winning_teams.values, y=venue_winning_teams.index, palette='coolwarm', ax=ax5)
    ax5.set_title(f'Winning Teams at {selected_venue}', fontsize=22, fontweight='bold', color='#2c3e50')
    ax5.set_xlabel('Number of Wins', fontsize=16, fontweight='bold', color='#34495e')
    ax5.set_ylabel('Teams', fontsize=16, fontweight='bold', color='#34495e')
    ax5.tick_params(axis='x', labelsize=14, labelcolor='#7f8c8d')
    ax5.tick_params(axis='y', labelsize=14, labelcolor='#7f8c8d')
    ax5.grid(axis='x', linestyle='--', alpha=0.7)
    ax5.set_xticks(range(0, venue_winning_teams.max() + 1))  # Ensure x-axis ticks are integers
    st.pyplot(fig5)

    # Head-to-Head Results
    st.header('🤝 Head-to-Head Results Across All Seasons')
    team1 = st.selectbox('Select Team 1', matches_df['team1'].unique())
    team2 = st.selectbox('Select Team 2', matches_df['team2'].unique())

    # Filter matches for the selected teams
    head_to_head_matches = matches_df[((matches_df['team1'] == team1) & (matches_df['team2'] == team2)) |
                                       ((matches_df['team1'] == team2) & (matches_df['team2'] == team1))]

    if not head_to_head_matches.empty:
        st.subheader(f'Head-to-Head Results: {team1} vs {team2}')
        head_to_head_wins = head_to_head_matches['winner'].value_counts().astype(int)  # Ensure integer values
        st.write('Match Results:')
        st.write(head_to_head_wins)

        # Visualize head-to-head results
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=head_to_head_wins.values, y=head_to_head_wins.index, palette='coolwarm', ax=ax)
        ax.set_title(f'Head-to-Head Wins: {team1} vs {team2}', fontsize=16, fontweight='bold', color='#2c3e50')
        ax.set_xlabel('Number of Wins', fontsize=12, fontweight='bold', color='#34495e')
        ax.set_ylabel('Teams', fontsize=12, fontweight='bold', color='#34495e')
        ax.tick_params(axis='x', labelsize=10, labelcolor='#7f8c8d')
        ax.tick_params(axis='y', labelsize=10, labelcolor='#7f8c8d')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_xticks(range(0, head_to_head_wins.max() + 1))  # Ensure x-axis ticks are integers
        st.pyplot(fig)

        # Select a specific match
        st.subheader('Select a Specific Match')
        match_options = head_to_head_matches[['id', 'team1', 'team2', 'date']].apply(
            lambda x: f"{x['team1']} vs {x['team2']} on {x['date']}", axis=1
        )
        selected_match = st.selectbox('Select Match', match_options)

        # Get match ID for the selected match
        match_id = head_to_head_matches.loc[
            match_options == selected_match, 'id'
        ].values[0]

        # Filter deliveries for the selected match
        match_data = combined_df[combined_df['match_id'] == match_id]

        # Display match details
        st.subheader(f'Match Details: {selected_match}')
        st.write(f"**Match ID:** {match_id}")
        st.write(f"**Teams:** {team1} vs {team2}")
        st.write(f"**Date:** {head_to_head_matches.loc[head_to_head_matches['id'] == match_id, 'date'].values[0]}")
        st.write(f"**Winner:** {head_to_head_matches.loc[head_to_head_matches['id'] == match_id, 'winner'].values[0]}")

        # Separate match details by teams
        for team in [team1, team2]:
            st.subheader(f'{team} Performance in Match {match_id}')

            # Top 5 Batters
            st.write(f"**Top 5 Batters for {team}:**")
            team_batter_data = match_data[match_data['batting_team'] == team]
            batter_stats = team_batter_data.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)
            batter_stats = batter_stats.astype(int)  # Ensure runs are integers
            st.write(batter_stats)

            # Visualize top 5 batters horizontally with proper runs
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=batter_stats.values, y=batter_stats.index, palette='Spectral', ax=ax, orient='h')
            ax.set_title(f'Top 5 Batters for {team} in Match {match_id}', fontsize=16, fontweight='bold', color='#2c3e50')
            ax.set_xlabel('Runs', fontsize=12, fontweight='bold', color='#34495e')
            ax.set_ylabel('Batter', fontsize=12, fontweight='bold', color='#34495e')
            ax.tick_params(axis='x', labelsize=10, labelcolor='#7f8c8d')
            ax.tick_params(axis='y', labelsize=10, labelcolor='#7f8c8d')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            ax.set_xticks(range(0, batter_stats.max() + 1, max(1, batter_stats.max() // 5)))  # Properly spaced x-axis ticks
            st.pyplot(fig)

            # Top 5 Bowlers
            st.write(f"**Top 5 Bowlers for {team}:**")
            team_bowler_data = match_data[match_data['bowling_team'] == team]
            bowler_stats = team_bowler_data[team_bowler_data['dismissal_kind'].notna()].groupby('bowler').size().sort_values(ascending=False).head(5)
            bowler_stats = bowler_stats.astype(int)  # Ensure wickets are integers
            st.write(bowler_stats)

            # Visualize top 5 bowlers horizontally with integer values
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=bowler_stats.values, y=bowler_stats.index, palette='coolwarm', ax=ax, orient='h')
            ax.set_title(f'Top 5 Bowlers for {team} in Match {match_id}', fontsize=16, fontweight='bold', color='#2c3e50')
            ax.set_xlabel('Wickets', fontsize=12, fontweight='bold', color='#34495e')
            ax.set_ylabel('Bowler', fontsize=12, fontweight='bold', color='#34495e')
            ax.tick_params(axis='x', labelsize=10, labelcolor='#7f8c8d')
            ax.tick_params(axis='y', labelsize=10, labelcolor='#7f8c8d')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            ax.set_xticks(range(0, bowler_stats.max() + 1))  # Ensure x-axis ticks are integers
            st.pyplot(fig)

    else:
        st.error(f"No matches found between {team1} and {team2}.")

    # Summary Section
    st.header('📜 Summary and Key Insights')

    # Option to select a season for the most successful team
    st.subheader('🏆 Most Successful Team by Season (Final Winner)')
    selected_season_team = st.selectbox('Select Season for Most Successful Team', sorted(matches_df['season'].unique()))
    season_team_data = matches_df[matches_df['season'] == selected_season_team]
    if not season_team_data.empty:
        final_match = season_team_data[season_team_data['id'] == season_team_data['id'].max()]  # Get the final match
        final_winner = final_match['winner'].values[0] if not final_match.empty else "No Winner"
        st.write(f"**{final_winner}** won the final in **{selected_season_team}**.")

    # Option to select a season for top batters
    st.subheader('🏏 Top Batter by Season')
    selected_season_batter = st.selectbox('Select Season for Top Batter', sorted(matches_df['season'].unique()))
    season_batter_data = deliveries_df[deliveries_df['match_id'].isin(matches_df[matches_df['season'] == selected_season_batter]['id'])]
    if 'batsman_runs' in season_batter_data.columns:
        top_batter = season_batter_data.groupby('batter')['batsman_runs'].sum().idxmax()
        top_batter_runs = season_batter_data.groupby('batter')['batsman_runs'].sum().max()
        st.write(f"**{top_batter}** with **{top_batter_runs} runs** in **{selected_season_batter}**.")

    # Option to select a season for top bowlers
    st.subheader('🎯 Top Bowler by Season')
    selected_season_bowler = st.selectbox('Select Season for Top Bowler', sorted(matches_df['season'].unique()))
    season_bowler_data = deliveries_df[deliveries_df['match_id'].isin(matches_df[matches_df['season'] == selected_season_bowler]['id'])]
    if 'dismissal_kind' in season_bowler_data.columns:
        top_bowler = season_bowler_data[season_bowler_data['dismissal_kind'].notna()].groupby('bowler').size().idxmax()
        top_bowler_wickets = season_bowler_data[season_bowler_data['dismissal_kind'].notna()].groupby('bowler').size().max()
        st.write(f"**{top_bowler}** with **{top_bowler_wickets} wickets** in **{selected_season_bowler}**.")

    st.subheader('📊 Additional Insights')
    total_matches = matches_df.shape[0]
    total_teams = matches_df['team1'].nunique()
    total_seasons = matches_df['season'].nunique()
    st.write(f"- Total Matches Played: **{total_matches}**")
    st.write(f"- Total Teams Participated: **{total_teams}**")
    st.write(f"- Total Seasons Analyzed: **{total_seasons}**")

    st.write("Thank you for exploring the IPL Data Analysis Dashboard! 🎉")

if __name__ == '__main__':
    app()

