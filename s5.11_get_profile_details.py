'''
    Script s5.11 | v1.0.0 | consult <https://catlism.github.io> for more info.
    part of Di Cristofaro, Matteo. Corpus Approaches to Language in Social Media. New York: Routledge, 2023. https://doi.org/10.4324/9781003225218.
    Copyright (C) 2023 Matteo Di Cristofaro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Import facebook_scraper module get_profile to get the profile details
from facebook_scraper import get_profile

# Define the function 'get_profile_details'
def get_profile_details(profile_id, profiles_db):
    """Extract details from a Facebook profile; input is the profile ID and the pandas dataframe to which
    downloaded details are stored. Returns a list with the following elements:

    friend_count = profile_details[0]
    follower_count = profile_details[1]
    following_count = profile_details[2]
    basic = profile_details[3]
    about = profile_details[4]

    Assumes the existence of:
    - a file named 'cookies.json' in the current path, containing Facebook cookie
    - a dataframe with 'profile_id' as index, e.g.:
    profiles_db = pd.DataFrame(
        columns=[
            "profile_id",
            "friend_count",
            "follower_count",
            "following_count",
            "basic_info",
            "about",
            ],
    ).set_index("profile_id")
    """

    # If details for the profile ID have already been downloaded:
    if profile_id in profiles_db.index:
        # Get the details from the already-downloaded data stored in the 'profiles_db' dataframe
        friend_count = profiles_db.loc[profile_id, "friend_count"]
        follower_count = profiles_db.loc[profile_id, "follower_count"]
        following_count = profiles_db.loc[profile_id, "following_count"]
        basic_info = profiles_db.loc[profile_id, "basic_info"]
        about = profiles_db.loc[profile_id, "about"]
        # Assign all the extracted details to a tuple labelled 'collected_details'
        collected_details = (
            friend_count,
            follower_count,
            following_count,
            basic_info,
            about,
        )
        # Output the list with the details
        return collected_details

    # If the details for the selected profile ID are not present in the 'profiles_db' dataframe:
    else:
        # Download the details using the 'get_profile' function from facebook-scraper; this requires Facebook cookies to be present in
        # the folder where the script is run, and passed to the function using the argument 'cookies=. Details on how to extract them
        # from the web browser are avaible in the tool's official documentation
        profile_details = get_profile(profile_id, cookies="cookies_fb.jso")
        # From the data downloaded by facebook-scraper extract only a number of details, saving each one of them to a separate variable
        friend_count = str(profile_details["Friend_count"])
        follower_count = str(profile_details["Follower_count"])
        following_count = str(profile_details["Following_count"])
        basic_info = profile_details["Basic info"]
        # Check if the data-point 'About' exists: if it does, extract the contents of the data-point 'About' and assign it to
        # the variable 'about'; if it does not assign the value 'None'instead
        about = profile_details.get("About", "None")
        # Assign all the extracted details to a tuple labelled 'collected_details'
        collected_details = (
            friend_count,
            follower_count,
            following_count,
            basic_info,
            about,
        )
        # Add the list with the downloaded details to the 'profiles_db' dataframe
        profiles_db.loc[profile_id] = collected_details
        # Output the list with the details
        return collected_details