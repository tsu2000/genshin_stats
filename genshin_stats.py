import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Global variables
url = 'https://raw.githubusercontent.com/tsu2000/genshin_stats/main/genshin.csv'
df = pd.read_csv(url)
dc = df.set_index('character_name')

def main():

    st.title('Genshin Impact Character Stats')
    subtitle = '### An exploration of Character Data in Genshin Impact'
    st.markdown(subtitle)

    st.markdown('This web app is for the visualisation and exploration of character data in the action role-playing game created by miHoYo, Genshin Impact. To observe and interact with the data visualisations, please select a banner from the box below.')

    topics = ['About',
              'Character Basic Information',
              'Character Base Stat Comparison', 
              'Character Ascension Information',
              'Character Talent Information',
              'Character Trivia']

    topic = st.selectbox('Select an aspect of the dataset to explore: ', topics)

    if topic == topics[0]:
        about()
    elif topic == topics[1]:
        basic()
    elif topic == topics[2]:
        level_stats()
    elif topic == topics[3]:
        spas_stats()
    elif topic == topics[4]:
        talent_stats()
    elif topic == topics[5]:
        trivia_stats()

        
        
        
        
def about(): # About the app
    
    st.components.v1.html("""<a href="https://github.com/tsu2000/genshin_stats" target="_blank"><img src="https://img.shields.io/static/v1?label=tsu2000&message=genshin_stats&color=blue&logo=github" alt="_blank"></a><a href="https://github.com/tsu2000/genshin_stats" target="_blank"><img src="https://img.shields.io/github/stars/tsu2000/genshin_stats?style=social" alt="tsu2000 - Genshin Impact Char Stats"></a>""", height=28)

    st.markdown("# Complete Dataset")
    if df is not None:
        st.dataframe(df.style.format(precision = 0))
    else:
        st.markdown('It appears the GitHub Repository hosting the dataset has some issue with the data. Please try again later.')
    st.markdown("---")
  
    st.markdown('### Resources used:')
    st.markdown('This web application uses a cleaned dataset in the form of a comma-separated values (csv) file. This dataset was originally obtained from Kaggle, a website for aggregating datasets.')
    st.markdown("- [**Genshin Impact Character Data - Information on all officially announced/released Genshin Impact characters (by Sophia Healy)**](https://www.kaggle.com/datasets/sophiahealy/genshin-impact-character-data)")
    st.markdown("### Visit Kaggle's Official Website:")
    st.markdown("- [**Kaggle: Your Home for Data Science**](https://www.kaggle.com) ")

    st.markdown("---")
                
    st.markdown('**Important Notice**: *This app is not affiliated with miHoYo. All technical details relating to current characters may be subject to change in the future. Genshin Impact and miHoYo are trademarks or registered trademarks of miHoYo. Genshin Impact © miHoYo.*')

    
def basic():
    
    st.markdown('---')
    
    st.header('Character Basic Information Table')   
    
    # Improve readability of results
    dc['rarity'] = dc['rarity'].fillna(0)
    dc['rarity'] = dc['rarity'].astype(int)
    dc['rarity'] = dc['rarity'].astype(str) + '*'
    
    dc['rarity'].replace('0*', 'Unknown', inplace = True)
    
    dc['playable'].replace('Y', 'Yes', inplace = True)
    dc['playable'].replace('N', 'No', inplace = True)
    
    basic_stats = dc.loc[dc.index, ['playable', 'rarity', 'vision', 'region', 'weapon_type']]
    
    fig = go.Figure(data = [go.Table(columnwidth = [5, 2.5, 2.5, 2.5, 2.5, 2.5],
                                     header = dict(values = ['<b>Character<b>', 
                                                             '<b>Playable?<b>',
                                                             '<b>Rarity<b>',
                                                             '<b>Vision<b>',
                                                             '<b>Region<b>',
                                                             '<b>Weapon Type<b>'],
                                                   fill_color = 'violet',
                                                   line_color = 'darkslategray',
                                                   align = 'center',
                                                   font = dict(color = 'black', size = 14)),
                                     cells = dict(values = [dc.index,
                                                            basic_stats['playable'],
                                                            basic_stats['rarity'],
                                                            basic_stats['vision'],
                                                            basic_stats['region'],
                                                            basic_stats['weapon_type']], 
                                                  fill_color = 'thistle',
                                                  line_color = 'darkslategray',
                                                  align = ['left', 'center'],
                                                  font = dict(color = ['black', 'purple'], size = [14, 14]),
                                                  height = 25))])
    fig.update_layout(height = 2000, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
    st.plotly_chart(fig, use_container_width = True)
    
    st.markdown('### View original source from csv file:')
    st.dataframe(basic_stats)
        
    st.markdown('---')
    
    
    
    
    
def level_stats(): 
    st.markdown('---')
    st.header('Character Base Stat Comparison')
   
    chars = st.multiselect("Which characters do you want to compare? (Select at most 12 characters)", dc.index)
    stat_proper = st.selectbox('Which main stat would you like to view?', ['Attack', 'Defense', 'HP'])
    button = st.button("View Plot", disabled = False)

    if button:
        if len(chars) <= 12:
            
            # Parsing data
            if stat_proper == 'Attack':
                stat = 'atk'
            elif stat_proper == 'Defense':
                stat = 'def'
            else:
                stat = 'hp'

            stat_list = [f'{stat}_1_20', f'{stat}_20_20', f'{stat}_20_40', f'{stat}_40_40', f'{stat}_40_50', f'{stat}_50_50',
                    f'{stat}_50_60', f'{stat}_60_60', f'{stat}_60_70', f'{stat}_70_70', f'{stat}_70_80', f'{stat}_80_80',
                    f'{stat}_80_90', f'{stat}_90_90']

            level_stats = dc.loc[chars, stat_list]
            
            # Sort plots for ordered legends
            entity_sort = list(level_stats[f'{stat}_90_90'].sort_values(ascending = False).index)
            ord_list = []
            for item in entity_sort:
                if item in chars:
                    ord_list.append(chars.index(item))
            
            # PLOT
            plt.style.use('seaborn-whitegrid')
            fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)
            
            for i in chars:
                plt.plot(stat_list, level_stats.loc[i], label = i, marker = 'o')

            plt.title('Comparison between {} for selected characters'.format(stat_proper), fontsize = 15)
            plt.ylabel(f'{stat_proper}', fontsize = 15, labelpad = 15)
            plt.xlabel('Stat at each level', fontsize = 15, labelpad = 15)
            plt.xticks(rotation = 25)


            handles, labels = plt.gca().get_legend_handles_labels()
            order = ord_list
            legend = plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc = 'upper left', 
                       title = r"$\bfCharacters$", frameon = 1, framealpha = 1, fontsize = 10)
            frame = legend.get_frame()
            frame.set_facecolor('white')
            frame.set_edgecolor('black')

            st.pyplot(fig)
            
            # Data Frame for comparison
            st.markdown('### Data Frame')
            st.dataframe(level_stats.style.format(precision = 0))
            
            st.markdown('### FAQ:')
            st.markdown('**What do the values on the x-axis mean?**')
            st.markdown("- These are the levels a character is at. The number on the *left* refers to the **current level** the character is leveled to, while the number on the *right* refers to the **current level cap** of the character. The reason for this distinction is because a character's stats increases when they ascend despite not leveling up, (E.g. Stats at level 70 with cap at level 70 and cap at level 80 are different) and hence the need for such a distinction.")
            st.markdown('**Why do the number of characters sometimes not correspond with the number of lines shown on the graph?**')
            st.markdown("- This is because some characters have the exact same stat progression as each other and one of the characters' lines is overlapping the others. (E.g. Amber & Kaeya) For greater clarity on this, it is highly recommended you check the data frame shown right below the plot to check which characters have the exact same stat progression. Furthermore, some characters may not have any statistical data at all, so it is not possible to draw a line for the character.")

        else:
            st.warning("You can only select a maximum of 12 characters!")
            
    st.markdown('---')

    
    
    
    
def spas_stats(): 
    
    st.markdown('---')
    
    st.header('Character Ascension Information')
    asc_char = st.selectbox('Which character would you like to view ascension stats for?', dc.index)
    st.markdown('### Ascension Stat Table')
    
    asc_stats = dc.loc[asc_char, ['ascension', 'ascension_specialty', 'ascension_talent_mat', 'ascension_boss_mat', 'special_0', 'special_1', 'special_2', 'special_3', 'special_4', 'special_5', 'special_6']].astype(str)
    
    if 'Hurricane Seed' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Anemo Hypostasis'
        
    if 'Lightning Prism' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Electro Hypostasis'

    if 'Basalt Pillar' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Geo Hypostasis'
        
    if 'Hoarfrost Core' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Cryo Regisvine'
        
    if 'Everflame Seed' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Pyro Regisvine'
        
    if 'Cleansing Heart' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Rhodeia of Loch'

    if 'Juvenile Jade' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Primo Geovishap'
        
    if 'Crystalline Bloom' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Cryo Hypostasis'
        
    if 'Marionette Core' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Maguu Kenki'
        
    if 'Perpetual Heart' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Perpetual Mechanical Array'

    if 'Smoldering Pearl' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Pyro Hypostasis'
        
    if 'Dew of Repudiation' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Hydro Hypostasis'
        
    if 'Storm Beads' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Thunder Manifestation'
        
    if 'Riftborn Regalia' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Golden Wolflord'

    if "Dragonheir's False Fin" in asc_stats['ascension_boss_mat']:
        asc_boss = 'Coral Defenders'
        
    if 'Runic Fang' in asc_stats['ascension_boss_mat']:
        asc_boss = 'Ruin Serpent'
    
    if 'nan' in asc_stats['ascension_boss_mat']:
        asc_boss = 'nan'
        
    if 'Traveler' in asc_char:
        asc_boss = 'None'
  
    fig = go.Figure(data = [go.Table(columnwidth = [4, 1.75],
                                     header = dict(values = [f'<b>Ascension Stats for {asc_char}<b>', '<b>Attributes<b>'],
                                                   fill_color = 'paleturquoise',
                                                   line_color = 'darkslategray',
                                                   font = dict(color = 'black', size = 16)),
                                     cells = dict(values = [['Special Ascension Stat',
                                                             'Base Special Ascension Stat at Ascension Level 0',
                                                             'Base Special Ascension Stat at Ascension Level 1',
                                                             'Base Special Ascension Stat at Ascension Level 2',
                                                             'Base Special Ascension Stat at Ascension Level 3',
                                                             'Base Special Ascension Stat at Ascension Level 4',
                                                             'Base Special Ascension Stat at Ascension Level 5',
                                                             'Base Special Ascension Stat at Ascension Level 6',
                                                             'Ascension Regional Specialty',
                                                             'Ascension Regular Material',
                                                             'Ascension Boss',
                                                             'Ascension Boss Material'],
                                                            [asc_stats['ascension'],
                                                             asc_stats['special_0'],
                                                             asc_stats['special_1'],
                                                             asc_stats['special_2'],
                                                             asc_stats['special_3'],
                                                             asc_stats['special_4'],
                                                             asc_stats['special_5'],
                                                             asc_stats['special_6'],
                                                             asc_stats['ascension_specialty'],
                                                             asc_stats['ascension_talent_mat'], 
                                                             asc_boss,
                                                             asc_stats['ascension_boss_mat']]], 
                                                  fill_color = 'lightcyan',
                                                  line_color = 'darkslategray',
                                                  align = ['left', 'center'],
                                                  font = dict(color = ['black', 'darkslateblue'], size = [14, 14]),
                                                  height = 25))])
    fig.update_layout(height = 700, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
    st.plotly_chart(fig, use_container_width = True)

    st.markdown('### View original source from csv file:')
    st.dataframe(asc_stats)
    
    st.markdown('### FAQ:')
    st.markdown('**What do the Ascension Levels refer to?**')
    st.markdown("- The Character Ascension Levels refers to the current level cap of the characters. In order to increase your level, you have to ascend, which means you will spend resources to increase your level cap to the next Ascension Level. The Ascension Levels and their corresponding character level caps are shown below:")
    st.markdown('<div style="text-align: center;">Ascension Level 0: &emsp;<b>Lvl 20</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 1: &emsp;<b>Lvl 40</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 2: &emsp;<b>Lvl 50</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 3: &emsp;<b>Lvl 60</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 4: &emsp;<b>Lvl 70</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 5: &emsp;<b>Lvl 80</b></div>', unsafe_allow_html = True)
    st.markdown('<div style="text-align: center;">Ascension Level 6: &emsp;<b>Lvl 90</b></div>', unsafe_allow_html = True)
    st.markdown('###')
    st.markdown("**What is a Special Ascencsion Stat?**")
    st.markdown("- Every playable character in Genshin Impact is given a Special Ascension Stat, which is basically a boost to one of their particular stat upon reaching a certain Ascension Level. This boost to their stat increases as their ascension level increases. These stats can be considered separate from their Base Stats (HP, Attack, Defense) and thus have been categorised under the section of 'Character Ascension Information'.")
    
    st.markdown('---')
    
    
    
    

def talent_stats(): 
    
    st.markdown('---')
    
    st.header('Character Talent Information')
    talent_char = st.selectbox('Which character would you like to view talent stats for?', dc.index)
    st.markdown('### Talent Stat Table')
    
    talent_stats = dc.loc[talent_char, ['talent_book_1', 'talent_book_2', 'talent_book_3', 'talent_weekly']]
    
    # Domain for Talents
    if 'Freedom' in talent_stats[0] or 'Resistance' in talent_stats[0] or 'Ballad' in talent_stats[0]:
        domain_loc = 'Forsaken Rift'
           
    if 'Prosperity' in talent_stats[0] or 'Diligence' in talent_stats[0] or 'Gold' in talent_stats[0]:
        domain_loc = 'Taishan Mansion'
     
    if 'Transience' in talent_stats[0] or 'Elegance' in talent_stats[0] or 'Light' in talent_stats[0]:
        domain_loc = 'Violet Court'
        
    # Days for Talents
    if 'Transience' in talent_stats[0] or 'Prosperity' in talent_stats[0] or 'Freedom' in talent_stats[0]:
        days = 'Monday, Thursday'

    if 'Elegance' in talent_stats[0] or 'Diligence' in talent_stats[0] or 'Resistance' in talent_stats[0]:
        days = 'Tuesday, Friday'

    if 'Light' in talent_stats[0] or 'Gold' in talent_stats[0] or 'Ballad' in talent_stats[0]:
        days = 'Wednesday, Saturday'
    
    # Weekly Boss Material for Talents
    if "Dvalin's" in talent_stats[3]:
        boss = 'Dvalin'
        
    if 'Boreas' in talent_stats[3]:
        boss = 'Andrius'
        
    if "Dragon Lord's Crown" in talent_stats[3] or 'Shard of a Foul Legacy' in talent_stats[3] or 'Shadow of the Warrior' in talent_stats[3]:
        boss = 'Childe'
        
    if 'Tusk of Monoceros Caeli' in talent_stats[3] or 'Bloodjade Branch' in talent_stats[3] or 'Gilded Scale' in talent_stats[3]:
        boss = 'Azhdaha'
        
    if 'Molten Moment' in talent_stats[3] or 'Hellfire Butterfly' in talent_stats[3] or 'Ashen Heart' in talent_stats[3]:
        boss = 'La Signora'
        
    if 'Mudra of the Malefic General' in talent_stats[3] or 'Tears of the Calamitous God' in talent_stats[3] or 'The Meaning of Aeons' in talent_stats[3]:
        boss = 'Magatsu Mitake Narukami no Mikoto'

    if 'Traveler' in talent_char:
        domain_loc = 'Forsaken Rift, Taishan Mansion, Violet Court'
        days = 'All days'
        boss = 'Dvalin, Azhdaha'
        
    fig = go.Figure(data = [go.Table(columnwidth = [4, 1.75],
                                     header = dict(values = [f'<b>Talent Stats for {talent_char}<b>', '<b>Attributes<b>'],
                                                   fill_color = 'lightsalmon',
                                                   line_color = 'darkslategray',
                                                   font = dict(color = 'black', size = 16)),
                                     cells = dict(values = [['2* Talent Material', 
                                                             '3* Talent Material',
                                                             '4* Talent Material',
                                                             'Domain Location',
                                                             'Days with Talent Availability*',
                                                             'Weekly Boss',
                                                             'Weekly Boss Talent Material'],
                                                            [talent_stats[0],
                                                             talent_stats[1],
                                                             talent_stats[2],
                                                             domain_loc,
                                                             days,
                                                             boss,
                                                             talent_stats[3]]], 
                                                  fill_color = 'bisque',
                                                  line_color = 'darkslategray',
                                                  align = ['left', 'center'],
                                                  font = dict(color = ['black', 'maroon'], size = [14, 14]),
                                                  height = 25))])
    fig.update_layout(height = 500, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
    st.plotly_chart(fig, use_container_width = True)
    st.markdown('*All Talent Books are available at all domains on Sunday.')
        
    st.markdown('### View original source from csv file:')
    st.dataframe(talent_stats)
    
    
    
    st.markdown('---')
    
    
    
    
    
def trivia_stats(): 
    
    st.markdown('---')

    st.header('Character Trivia')
    triv_char = st.selectbox('View various non-essential trivia about a particular Genshin Impact character:', dc.index)
    st.markdown('### Trivia Table')
    
    triv_stats = dc.loc[triv_char, ['model', 'constellation', 'birthday', 'special_dish', 'voice_eng', 
                                    'voice_cn', 'voice_jp', 'voice_kr', 'release_date']].astype(str)
  
    fig = go.Figure(data = [go.Table(columnwidth = [4, 1.75],
                                    header = dict(values = [f'<b>{triv_char} Trivia<b>', '<b>Attributes<b>'],
                                                   fill_color = 'yellowgreen',
                                                   line_color = 'darkslategray',
                                                   font = dict(color = 'black', size = 16)),
                                     cells = dict(values = [['Character Model Build', 
                                                             'Character Constellation',
                                                             'Character Birthday',
                                                             'Character Special Dish',
                                                             'Character Voice Actor - English',
                                                             'Character Voice Actor - 中文',
                                                             'Character Voice Actor - 日本語',
                                                             'Character Voice Actor - 한글',
                                                             'Date of Release (DD-MM-YY)'],
                                                            triv_stats.values], 
                                                  fill_color = 'honeydew',
                                                  line_color = 'darkslategray',
                                                  align = ['left', 'center'],
                                                  font = dict(color = ['black', 'darkolivegreen'], size = [14, 14]),
                                                  height = 25))])
    fig.update_layout(height = 500, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
    st.plotly_chart(fig, use_container_width = True)

    st.markdown('### View original source from csv file:')
    st.dataframe(triv_stats)
    
    st.markdown('---')
    
    
    
    
    
if __name__ == "__main__":
    main()
    
