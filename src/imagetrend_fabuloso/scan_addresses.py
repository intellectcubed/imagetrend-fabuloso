import argparse

from imagetrend import ImageTrend


args = None

def parse_args():
    global args

    parser = argparse.ArgumentParser(description="Parse command line arguments.")
    #add a boolean argument login:
    parser.add_argument(
        "--login",
        action="store_true",
        help="Login to the application.",
    )
    parser.add_argument(
        "--get_incidents",
        action="store_true",
        help="get indidents",
    )

    args = parser.parse_args()

def login(imagetrend=None):
    if not imagetrend:
        imagetrend = ImageTrend()

    imagetrend.connect_to_existing_chrome()
    imagetrend.login()


def get_incidents(imagetrend=None):
    if not imagetrend:
        imagetrend = ImageTrend()
        imagetrend.connect_to_existing_chrome()

    imagetrend.list_incidents()

    # Assuming you have a method in ImageTrend to get incidents

def main():
    parse_args()

    if args.login:

        # Assuming you have a function to handle the login process
        print("Logging in...")
        login()
        # login_function()  # Replace with your actual login function
    
    if args.get_incidents:
        get_incidents()


if __name__ == "__main__":
    main()