# NAME: Ryan Chang # ID: 1765407533
# DATE: 2023-04-23
# DESCRIPTION: <The program is a social networking system that allows users to interact with each other by adding friends and getting
#               recommendations for new friends based on mutual friends. The program reads two input files, one
#               containing the profiles of members and the other containing their friendship connections. It then
#               creates a graph based on the friendship connections and calculates the similarity scores between
#               members. Users can perform various actions such as displaying member information, showing the number
#               of friends of a member, displaying a list of a member's friends, adding/removing friends, and getting
#               friend recommendations. The program also allows users to save their changes to the friend
#               connections file.>


from Graph import *
from typing import Tuple, List, IO, Dict

PROGRAMMER = "Ryan Chang"
MEMBER_INFO = "1"
NUM_OF_FRIENDS = "2"
LIST_OF_FRIENDS = "3"
RECOMMEND = "4"
SEARCH = "5"
ADD_FRIEND = "6"
REMOVE_FRIEND = "7"
SHOW_GRAPH = "8"
SAVE = "9"

LINE = "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"


class Member:
    def __init__(self, member_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 country: str):
        """
        Initializes the member's information and creates an empty list of friends.
        """
        # Variables are initialized
        self.ID_ = member_id
        self.firstname_ = first_name
        self.lastname_ = last_name
        self.email_ = email
        self.country_ = country
        self.friends_id_list = []

    def add_friend(self, friend_id) -> None:
        """
        Adds a friend to the member's list of friends.
        """
        # Check if the friend is in the list
        if friend_id not in self.friends_id_list:
            # Add the friend to the list
            self.friends_id_list.append(friend_id)
            self.friends_id_list.sort()

    # Check if the friend is in the list
    def remove_friend(self, friend_id) -> None:
        """
        Removes a friend from the member's list of friends.
        """
        # Check if the friend is in the list
        if friend_id in self.friends_id_list:
            # Remove the friend from the list
            self.friends_id_list.remove(friend_id)

    # Complete according to the output sample in the handout
    def __str__(self) -> str:
        """
        Returns a string representation of the member's information.
        """
        # Create a string with the member's information
        member_info = self.firstname_ + " " + self.lastname_ + '\n' + self.email_ + "\nFrom " + self.country_ + "Has " + str(
            len(self.friends_id_list)) + " friends.\n"

        return member_info

    # Must return the complete name
    def display_name(self) -> str:
        """
        Returns the member's name.
        """
        # Create a string with the member's name
        name = self.firstname_ + " " + self.lastname_
        return name


# Do not change
def open_file(file_type: str) -> IO:
    """
    Opens a file and returns a file pointer.
    """
    # Uncomment during code development.
    # Remove before submission
    # if file_type == "profile":
    #     file_name = "profile_10.csv"
    # else:
    #     file_name = "connection_10.txt"
    file_pointer = None
    while file_pointer is None:
        # Comment during the code development. Uncomment before submission.
        file_name = input("Enter the " + file_type + " filename:\n")
        try:
            file_pointer = open(file_name, 'r')
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")

    return file_pointer


# Do not change
def create_network(fp: IO) -> Dict[int, List[int]]:
    """
    Creates a network of members and their friends.
    """
    size = int(fp.readline())
    network = {}

    for i in range(size):
        network[i] = []

    for line in fp:
        split_line = line.strip().split(" ")
        member_id1 = int(split_line[0])
        member_id2 = int(split_line[1])
        network[member_id1].append(member_id2)
        network[member_id2].append(member_id1)

    return network


# Do not change
def common_degree(list1: List, list2: List) -> int:
    """
    Returns the number of common elements between two lists.
    """
    degree = 0
    for i in range(len(list1)):
        if list1[i] in list2:
            degree += 1

    return degree


# Do not change
def init_matrix(size: int) -> List[List[int]]:
    """
    Initializes a matrix of size x size with 0s.
    """
    matrix = []
    for row in range(size):
        matrix.append([])
        for column in range(size):
            matrix[row].append(0)

    return matrix


def calc_similarity_scores(network: Dict[int, List[int]]) -> List[List[int]]:
    """
    Calculates the similarity scores between members.
    """
    similarity_matrix = init_matrix(len(network))

    for i in range(len(network)):
        for j in range(i, len(network)):
            degree = common_degree(network[i], network[j])
            similarity_matrix[i][j] = degree
            similarity_matrix[j][i] = degree

    return similarity_matrix


# Do not change
def recommend(member_id: int, friend_list: List[int], similarity_list: List[int]) -> int:
    """
    Returns the member ID of the member with the highest similarity score.
    """
    max_similarity_val = -1
    max_similarity_pos = -1

    for i in range(len(similarity_list)):
        if i not in friend_list and i != member_id:
            if max_similarity_val < similarity_list[i]:
                max_similarity_pos = i
                max_similarity_val = similarity_list[i]

    return max_similarity_pos


def create_members_list(profile_fp: IO) -> List[Member]:
    """
    Creates a list of members from the profile file.
    """
    profiles = []
    profile_fp.readline()
    line = profile_fp.readline()
    profile_list = line.split(',')
    while line is not None and len(profile_list) == 5:
        # Create a member object
        ID = int(profile_list[0])
        firstname = profile_list[1]
        lastname = profile_list[2]
        email = profile_list[3]
        country = profile_list[4]
        mem = Member(ID, firstname, lastname, email, country)
        # Add the member to the list
        profiles.append(mem)
        # Read the next line
        line = profile_fp.readline()
        profile_list = line.split(',')
    return profiles


def display_menu():
    """
    Displays the menu of options.
    """
    print("\nPlease select one of the following options.\n")
    # Complete according to the output sample in the handout
    print(MEMBER_INFO + ". Show a member's information \n" +
          NUM_OF_FRIENDS + ". Show a member's number of friends\n" +
          LIST_OF_FRIENDS + ". Show a member's list of friends\n" +
          RECOMMEND + ". Recommend a friend for a member\n" +
          SEARCH + ". Search members by country\n" +
          ADD_FRIEND + ". Add friend\n" +
          REMOVE_FRIEND + ". Remove friend\n" +
          SHOW_GRAPH + ". Show graph\n" +
          SAVE + ". Save changes"
          )
    return input("Press any other key to exit.\n")


def receive_verify_member_id(size: int):
    """
    Receives a member id from the user and verifies that it is valid.
    """
    valid = False
    while not valid:
        # Ask the user for a member id
        ID_ = input(f"Please enter a member id between 0 and {size - 1}:\n")
        if not ID_.isdigit():
            # If the input is not a number, print an error message
            print("This is not a valid entry.")
        elif not 0 <= int(ID_) < size:
            # If the input is not in the range, print an error message
            print("This member id does not exist")
        else:
            valid = True

    return int(ID_)


def add_friend(profile_list: List[Member],
               similarity_matrix: List[List[int]]) -> None:
    """
    Adds a friend to a member's list of friends.
    """
    size = len(profile_list)
    # Ask the user for two member ids
    print("For the first friend: ")
    member1 = receive_verify_member_id(size)
    print("For the second friend: ")
    member2 = receive_verify_member_id(size)
    if member1 == member2:
        # If the two ids are the same, print an error message
        print("You need to enter two different ids. Please try again.")
    elif member1 in profile_list[member2].friends_id_list:
        # If the two members are already friends, print an error message
        print("These two members are already friends. Please try again.")
    else:
        for f_id in profile_list[member2].friends_id_list:
            # Update the similarity matrix
            similarity_matrix[member1][f_id] += 1
            similarity_matrix[f_id][member1] += 1

        for f_id in profile_list[member1].friends_id_list:
            # Update the similarity matrix
            similarity_matrix[member2][f_id] += 1
            similarity_matrix[f_id][member2] += 1

        # Update the friend lists
        profile_list[member1].add_friend(member2)
        profile_list[member2].add_friend(member1)

        # Update the similarity matrix
        similarity_matrix[member1][member1] += 1
        similarity_matrix[member2][member2] += 1

        print("The connection is added. Please check the graph.")


def remove_friend(profile_list: List[Member],
                  similarity_matrix: List[List[int]]) -> None:
    """
    Removes a friend from a member's list of friends.
    """
    size = len(profile_list)
    # Ask the user for two member ids
    print("For the first friend: ")
    member1 = receive_verify_member_id(size)
    print("For the second friend: select from the following list: " + str(profile_list[member1].friends_id_list))
    member2 = receive_verify_member_id(size)
    if member1 == member2:
        # If the two ids are the same, print an error message
        print("You need to enter two different ids. Please try again.")
    elif member1 not in profile_list[member2].friends_id_list:
        # If the two members are not friends, print an error message
        print("These two members are not friends. Please try again.")
    else:
        for f_id in profile_list[member2].friends_id_list:
            # Update the similarity matrix
            similarity_matrix[member1][f_id] -= 1
            similarity_matrix[f_id][member1] -= 1

        for f_id in profile_list[member1].friends_id_list:
            # Update the similarity matrix
            similarity_matrix[member2][f_id] -= 1
            similarity_matrix[f_id][member2] -= 1

        # Update the friend lists
        profile_list[member1].add_friend(member2)
        profile_list[member2].add_friend(member1)

        # Update the similarity matrix
        similarity_matrix[member1][member1] -= 1
        similarity_matrix[member2][member2] -= 1

        print("The connection is removed. Please check the graph.")


def search(profile_list: List[Member]) -> None:
    """
    Searches the list of members by country.
    """
    # Ask the user for a country name
    country = input("Please enter a country name: ")
    results = []
    # Search the list of members for the country name
    for mem in profile_list:
        if mem.country_.strip() == country:
            # If the country name is found, add the member to the results list
            results.append(mem)
    if results:
        # If there are results, print the results
        for mem in results:
            print(mem.firstname_, mem.lastname_)
    else:
        print("No results")


# Do not change.
def add_friends_to_profiles(profile_list: List[Member],
                            network: Dict[int, List[int]]) -> None:
    """
    Adds the friends to the profiles.
    """
    for i in range(len(profile_list)):
        profile_list[i].friends_id_list = network[i]


def select_action(profile_list: List[Member],
                  network: Dict[int, List[int]],
                  similarity_matrix: List[List[int]]) -> str:
    """
    Asks the user to select an action.
    """
    response = display_menu()

    print(LINE)
    size = len(profile_list)

    if response in [MEMBER_INFO, NUM_OF_FRIENDS, LIST_OF_FRIENDS, RECOMMEND]:
        member_id = receive_verify_member_id(size)

    if response == MEMBER_INFO:
        # Print the member's information
        print(profile_list[member_id].__str__())
    elif response == NUM_OF_FRIENDS:
        # Print the number of friends
        print(profile_list[member_id].firstname_ + " has " + str(len(profile_list[member_id].friends_id_list)) + " Friends.")
    elif response == LIST_OF_FRIENDS:
        # Print the list of friends
        output = ""
        for friend_id in profile_list[member_id].friends_id_list:
            friend = str(profile_list[friend_id].ID_) + " " + profile_list[friend_id].firstname_ + " " + profile_list[friend_id].lastname_
            output = output + friend + "\n"
        print(output)
    elif response == RECOMMEND:
        # Print the recommended friend
        recFriend = recommend(member_id, profile_list[member_id].friends_id_list, similarity_matrix[member_id])
        print(f"The suggested friend for {profile_list[member_id].display_name()} is {profile_list[recFriend].display_name()} with id {recFriend}")
    elif response == SEARCH:
        # Search for a country
        search(profile_list)
    elif response == ADD_FRIEND:
        # Add a friend
        add_friend(profile_list, similarity_matrix)
    elif response == REMOVE_FRIEND:
        # Remove a friend
        remove_friend(profile_list, similarity_matrix)
    elif response == SHOW_GRAPH:
        tooltip_list = []
        for profile in profile_list:
            tooltip_list.append(profile)
        graph = Graph(PROGRAMMER, [*range(len(profile_list))], tooltip_list, network)
        graph.draw_graph()
        print("Graph is ready. Please check your browser.")
    elif response == SAVE:
        # Save the changes
        save_changes(profile_list)
    else:
        return "Exit"

    print(LINE)

    return "Continue"


def save_changes(profile_list: List[Member]) -> None:
    """
    Saves the changes to the files.
    """
    # User is prompted to submit a filename. The file is opened and the number of members is written to the file.
    inputfile = input("Please enter the filename: ")
    ofile = open(inputfile, "w")
    print(f"{len(profile_list)}\n")
    for mem in profile_list:
        for friend in mem.friends_id_list:
            if friend in profile_list:
                if friend > mem.ID_:
                    # The ID of the member and the ID of the friend are written to the file.
                    ofile.write(f"{mem.ID_}, {friend}\n")
    ofile.close()
    print("All changes are saved in " + inputfile)


# Do not change
def initialization() -> Tuple[List[Member], Dict[int, List[int]], List[List[int]]]:
    """
    Initializes the program.
    """
    profile_fp = open_file("profile")
    profile_list = create_members_list(profile_fp)

    connection_fp = open_file("connection")
    network = create_network(connection_fp)
    if len(network) != len(profile_list):
        input("Both files must have the same number of members.\n"
              "Please try again.")
        exit()

    add_friends_to_profiles(profile_list, network)
    similarity_matrix = calc_similarity_scores(network)

    profile_fp.close()
    connection_fp.close()

    return profile_list, network, similarity_matrix


# Do not change
def main():
    """
    Runs the program.
    """
    print("Welcome to the network program.")
    print("We need two data files.")
    profile_list, network, similarity_matrix = initialization()

    action = "Continue"
    while action != "Exit":
        action = select_action(profile_list, network, similarity_matrix)

    input("Thanks for using this program.")


if __name__ == "__main__":
    main()
