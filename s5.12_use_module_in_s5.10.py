# Assuming that script [s5.11] has been saved locally to a file name 'get_profile_details.py
# it can be implemented into script [s5.10] by adding the following lines where indicated in the comments

# Add the following imports at the bottom of the 'import' section, to use pandas dataframes, and the get_profile_details module
import pandas as pd
from get_profile_details import get_profile_details

# Add the following lines after the import section to create a pandas dataframe for storing the downloaded details.
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

# Whenever details from a profile need to be extracted, the function 'get_profile_details' can be applied to the extracted
# 'profile_id'. For example, to download details regarding the author of a comment:
commenter_details = get_profile_details(comment["commenter_id"])

# Each detail can then be extracted to an XML attribute using e.g.:
comment_tag.attrib["author_friends"] = commenter_details[0]
comment_tag.attrib["author_current_place"] = commenter_details[3]