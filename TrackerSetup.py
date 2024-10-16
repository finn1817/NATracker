import argparse

def main():
    parser = argparse.ArgumentParser(description='Simple Journal Tracker Setup')
    parser.add_argument('--dir', type=str, help='Directory to track', required=True)
    parser.add_argument('--remove', type=bool, help='Remove previous tracking')

    args = parser.parse_args()
    

    

if __name__ == "__main__":
    main()