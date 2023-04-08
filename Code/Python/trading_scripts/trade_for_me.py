"""
This script is a trading bot for the 5paisa trading platform. It is used to place call and put options for the Nifty and BankNifty indices. It makes use of the py5paisa package to interact with the 5paisa trading API. The script first downloads a CSV file containing a list of scrips and their corresponding codes from a remote URL. It then uses this CSV file to fetch the scrip code for a given scrip name. It also uses a CSV file containing a list of holidays to check whether a given date is a holiday or not. The script then places the call and put options using the py5paisa package. The expiry date for the options is set to the expiry date of the current week, which is computed based on the current date and the Indian stock market weekly expiry on every Thursday. If Thursday is a holiday, the expiry date is set to the previous day. The bot places orders for call and put options based on the last traded price of the index and the buffer margin specified in the CONSTANTS dictionary. The bot also takes into account the maximum lot size for call and put options for Nifty and BankNifty indices.
"""

import argparse
import csv
import datetime
import os
import time
from functools import partial
from typing import Optional

import pandas as pd
import requests
from config import CONSTANTS
from py5paisa import FivePaisaClient
from secret_credentials import CREDENTIALS

EXIT_SCRIPT = False
DF_PD = pd.DataFrame()
NIFTY_SYMBOL = CONSTANTS["NIFTY_SYMBOL"]
NIFTY_STEP_SIZE = CONSTANTS["NIFTY_STEP_SIZE"]
NIFTY_LOT_QUANTITY = CONSTANTS["NIFTY_LOT_QUANTITY"]
BANKNIFTY_SYMBOL = CONSTANTS["BANKNIFTY_SYMBOL"]
BANKNIFTY_STEP_SIZE = CONSTANTS["BANKNIFTY_STEP_SIZE"]
BANKNIFTY_LOT_QUANTITY = CONSTANTS["BANKNIFTY_LOT_QUANTITY"]
BUY = CONSTANTS["BUY"]
SELL = CONSTANTS["SELL"]
EXCHANGE = CONSTANTS["EXCHANGE"]
EXCHANGE_TYPE = CONSTANTS["EXCHANGE_TYPE"]
SEGMENT = CONSTANTS["SEGMENT"]
HOLIDAY_LIST_FILE_NAME = CONSTANTS["HOLIDAY_LIST_FILE_NAME"]
BUFFER_MARGIN = CONSTANTS["BUFFER_MARGIN"]
CALL_ORDER_TYPE = CONSTANTS["CALL_ORDER_TYPE"]
PUT_ORDER_TYPE = CONSTANTS["PUT_ORDER_TYPE"]
NIFTY_MAX_LOT_SIZE = CONSTANTS["NIFTY_MAX_LOT_SIZE"]
BANKNIFTY_MAX_LOT_SIZE = CONSTANTS["BANKNIFTY_MAX_LOT_SIZE"]
SCRIP_MASTER_CSV_FILE_NAME = CONSTANTS["SCRIP_MASTER_CSV_FILE_NAME"]
SCRIP_MASTER_CSV_URL = CONSTANTS["SCRIP_MASTER_CSV_URL"]
REQUESTS_TIMEOUT = CONSTANTS["REQUESTS_TIMEOUT"]


def exit_program():
    """Exit program"""
    print("Exiting...")
    global EXIT_SCRIPT
    EXIT_SCRIPT = True


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--response-token", required=True, help="5paisa response token")
    args = parser.parse_args()
    return args


def create_client(credentials) -> FivePaisaClient:
    """
    Creates a FivePaisaClient instance using the given credentials.

    Parameters:
    -----------
    credentials: dict
        A dictionary containing the login credentials for the FivePaisaClient.

    Returns:
    --------
    FivePaisaClient
        An instance of the FivePaisaClient class.
    """
    return FivePaisaClient(cred=credentials)


def download_scrip_csv(url, filename) -> None:
    """Download a CSV file from a URL and write it to a local file if not present or more than 2 days old.

    Args:
        url (str): The URL of the CSV file.
        filename (str): The name of the file to save the CSV to.

    Returns:
        None
    """
    if os.path.exists(filename):
        # check if file is older than 2 days
        filetime = os.path.getmtime(filename)
        if datetime.datetime.now() - datetime.datetime.fromtimestamp(
            filetime
        ) < datetime.timedelta(days=2):
            print(
                f"{filename} already exists and is less than 2 days old. Skipping download."
            )
            return

    # Download CSV file
    response = requests.get(url, timeout=REQUESTS_TIMEOUT)
    # Write CSV to local file while overwriting existing file
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for line in response.iter_lines():
            writer.writerow(line.decode("utf-8").split(","))


def fetch_scrip_code_from_csv(df_pd, to_match):
    """
    Get the scrip code for a given name from a CSV file loaded into a pandas DataFrame.

    Args:
    - df_pd: pandas DataFrame containing the CSV file data.
    - to_match: the name of the scrip for which to find the scrip code.

    Returns:
    - Scrip code of the matching scrip name in the DataFrame.

    Raises:
    - ValueError: If the scrip code for the given name is not found in the DataFrame.
    """
    # Filter rows based on column value
    row = df_pd.loc[df_pd["Name"] == to_match]
    # Access column values for the matched row
    if not row.empty:
        scrip_code = row["Scripcode"].iat[0]
        return scrip_code
    raise ValueError(f"Scripcode for {to_match} not found.")


def is_holiday(date) -> bool:
    """
    Check if a given date is a holiday based on the list of holidays stored in a CSV file.

    Args:
    date (str): Date in the format "YYYY-MM-DD"

    Returns:
    bool: True if the date is a holiday, False otherwise
    """
    with open(HOLIDAY_LIST_FILE_NAME, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["DATE"] == date:
                return True
        return False


def get_current_week_expiry_date():
    """
    Returns the expiry date of the current week based on the current date and the Indian stock market weekly expiry
    on every Thursday. If Thursday is a holiday, expiry date is set to the previous day.

    Returns:
    str: A string representing the expiry date in 'YYYY-MM-DD' format.
    """
    today = datetime.date.today()
    thursday = today + datetime.timedelta((3 - today.weekday()) % 7)
    if is_holiday(thursday.strftime("%d-%b-%Y")):
        expiry_date = thursday - datetime.timedelta(days=1)
    else:
        expiry_date = thursday
    return expiry_date.strftime("%Y-%m-%d")


def get_last_rate(client, symbol) -> Optional[float]:
    """
    Fetches the last traded price for a given symbol from the market feed using the provided `FivePaisaClient` instance.

    Args:
    - client (FivePaisaClient): An instance of `FivePaisaClient` to use for making requests to the market feed API.
    - symbol (str): The symbol for which to fetch the last traded price.

    Returns:
    - float or None: The last traded price for the symbol, or None if the API response indicates an error or an empty result.
    """
    req_list = [{"Exch": "N", "ExchType": "C", "Symbol": symbol}]
    response = client.fetch_market_feed(req_list)
    if response["Status"] == 0 and len(response["Data"]) > 0:
        return response["Data"][0]["LastRate"]
    return None


def get_client_margin(client) -> float:
    """
    Returns the current margin available in the user's trading account.

    Args:
    client: FivePaisaClient object that is used to interact with the 5paisa API.

    Returns:
    float: The current margin available in the user's trading account, after deducting the buffer margin.
    """
    margin_response = client.margin()
    current_margin = margin_response[0]["AvailableMargin"]
    return current_margin - BUFFER_MARGIN


def strike_price_for_option(
    current_date, current_expiry, step_size, current_rate
) -> float:
    """
    Calculates the strike price for the option.

    Parameters:
    current_date (str): Current date in the format 'YYYY-MM-DD'.
    current_expiry (str): Current expiry date of the option in the format 'YYYY-MM-DD'.
    step_size (float): Step size for the strike price.
    current_rate (float): Current rate of the underlying asset.

    Returns:
    float: The calculated strike price.

    """
    # Create strike price
    if current_date == current_expiry:
        strike_price = (current_rate // step_size) * step_size
    else:
        strike_price = (current_rate // step_size) * step_size + step_size
    return strike_price


def fetch_option_price(
    client,
    current_rate,
    symbol,
    step_size,
    current_date,
    current_expiry,
    option_type,
):
    """
    Fetches the last rate and strike price for a given option.

    Args:
    - client: The trading client instance.
    - symbol: The underlying asset symbol for the option.
    - step_size: The step size of the option.
    - option_type: The type of the option (CE or PE).
    - current_date: The current date in YYYY-MM-DD format.
    - current_expiry: The current expiry date in YYYY-MM-DD format.
    - current_rate: The current market rate of the asset.

    Returns:
    - A tuple containing the last rate and strike price for the option.
    """
    # <py5paisa.py5paisa.FivePaisaClient object at 0x7f9e50e36980> 41041 BANKNIFTY 25 2023-04-08 2023-04-13 PE
    # Create strike price
    strike_price = strike_price_for_option(
        current_date, current_expiry, step_size, current_rate
    )
    # Convert current_expiry to datetime objects
    current_expiry_dt = datetime.datetime.strptime(current_expiry, "%Y-%m-%d").date()
    # Create option data dictionary
    option_data = [
        {
            "Exch": "N",
            "ExchType": "D",
            "Symbol": f"{symbol} {current_expiry_dt.strftime('%d %b %Y').upper()} {option_type} {strike_price:.2f}",
            "Expiry": current_expiry_dt.strftime("%Y%m%d"),
            "StrikePrice": f"{strike_price:.0f}",
            "OptionType": option_type,
        }
    ]
    # Return the option data dictionary as a list
    last_rate = client.fetch_market_feed(option_data)["Data"][0]["LastRate"]
    return last_rate, strike_price


def lots_to_purchase(available_margin, symbol_lot_quantity, option_price) -> int:
    """
    Calculate the lots of options to purchase based on the available margin, symbol step size, and option price.

    :param available_margin: float representing the available margin
    :param symbol_lot_quantity: float representing the quantity size of 1 lot of the symbol
    :param option_price: float representing the option price
    :return: integer representing the lots of options to purchase
    """

    return available_margin // (symbol_lot_quantity * option_price)


# Build buy order
def buy_put_or_call(client, current_date, current_expiry, symbol, option_type):
    """
    This function buys a put or call option for the given symbol and option type on the specified expiry date.

    Args:
        client: An instance of the client for trading.
        current_date: A string representing the current date in "YYYY-MM-DD" format.
        current_expiry: A string representing the expiry date in "YYYY-MM-DD" format.
        symbol: A string representing the symbol of the underlying asset.
        option_type: A string representing the type of option, i.e., "CE" for call option and "PE" for put option.

    Raises:
        ValueError: If an invalid combination of symbol and option type is provided.

    Returns:
        None
    """

    if symbol == NIFTY_SYMBOL:
        step_size = NIFTY_STEP_SIZE
        symbol_lot_size = NIFTY_LOT_QUANTITY
    elif symbol == BANKNIFTY_SYMBOL:
        step_size = BANKNIFTY_STEP_SIZE
        symbol_lot_size = BANKNIFTY_LOT_QUANTITY
    else:
        raise ValueError("Invalid params {symbol} and {option_type}")

    exchange = EXCHANGE
    exchange_type = EXCHANGE_TYPE
    order_type = BUY
    current_rate = get_last_rate(client, symbol)

    option_price, strike_price = fetch_option_price(
        client,
        current_rate,
        symbol,
        step_size,
        current_date,
        current_expiry,
        option_type,
    )

    # Inflate the option price a bit to create a buffer for limit prices
    if symbol == NIFTY_SYMBOL:
        option_price = option_price + 1
    else:
        option_price = option_price + 5

    available_margin = get_client_margin(client)

    to_purchase = lots_to_purchase(available_margin, symbol_lot_size, option_price)

    buy_sell_function(
        client,
        symbol,
        strike_price,
        current_expiry,
        order_type,
        exchange,
        exchange_type,
        option_type,
        to_purchase,
        symbol_lot_size,
        option_price,
    )


def buy_sell_function(
    client,
    symbol,
    option_strike,
    expiry_date,
    order_type,
    exchange,
    exchange_type,
    option_type,
    to_purchase,
    symbol_lot_size,
    inflated_option_price,
):
    """Places a buy or sell order for the given option contract.

    Args:
        client (object): The client object used to place the order.
        symbol (str): The underlying asset symbol.
        option_strike (float): The strike price of the option contract.
        expiry_date (str): The expiry date of the option contract in the format "YYYY-MM-DD".
        order_type (str): The type of order to place (BUY or SELL).
        exchange (str): The exchange to place the order on.
        exchange_type (str): The exchange type to place the order on.
        option_type (str): The type of option contract (CALL or PUT).
        lot_size (int): The number of lots to purchase/sell.
        step_size (float): The step size for the symbol.

    Returns:
        None.
    """
    if symbol == NIFTY_SYMBOL:
        max_lot_size = NIFTY_MAX_LOT_SIZE
    elif symbol == BANKNIFTY_SYMBOL:
        max_lot_size = BANKNIFTY_MAX_LOT_SIZE
    else:
        raise ValueError("Invalid symbol")
    expiry_date_dt = datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date()
    total_lots = to_purchase
    to_match = f"{symbol} {expiry_date_dt.strftime('%d %b %Y')} {option_type} {option_strike:.2f}"
    scrip_code = int(fetch_scrip_code_from_csv(DF_PD, to_match))
    while total_lots > 0:
        current_lot_size = min(total_lots, max_lot_size)
        quantity = current_lot_size * symbol_lot_size
        client.place_order(
            OrderType=order_type,
            Exchange=exchange,
            ExchangeType=exchange_type,
            ScripCode=scrip_code,
            Qty=quantity,
            Price=inflated_option_price,
        )
        total_lots -= current_lot_size


# Build sell order
def sell_all_positions(client):
    """
    Closes all open positions of the client.

    Args:
    - client: the client object that contains the open positions.

    Returns:
    - None.
    """
    client.squareoff_all()


# Display positions
def display_all_positions(client):
    """
    Displays all the current positions held by the client.

    Args:
        client: The client object used to fetch the holdings.

    Returns:
        None.
    """
    holdings = client.holdings()
    for holding in holdings:
        print(f"Symbol: {holding['Symbol']}, Quantity: {holding['Quantity']}")


def main():
    """
    The main function which displays the menu options for the user and invokes the corresponding functions based on the user input.

    Args:
        None

    Returns:
        None
    """
    args = parse_arguments()
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    client = create_client(CREDENTIALS)
    client.get_access_token(args.response_token)
    current_expiry = get_current_week_expiry_date()
    download_scrip_csv(SCRIP_MASTER_CSV_URL, SCRIP_MASTER_CSV_FILE_NAME)
    global DF_PD
    DF_PD = pd.read_csv(SCRIP_MASTER_CSV_FILE_NAME)
    DF_PD.set_index("Name")

    options_dict = {
        "1": partial(
            buy_put_or_call,
            client,
            current_date,
            current_expiry,
            NIFTY_SYMBOL,
            CALL_ORDER_TYPE,
        ),
        "2": partial(
            buy_put_or_call,
            client,
            current_date,
            current_expiry,
            NIFTY_SYMBOL,
            PUT_ORDER_TYPE,
        ),
        "3": partial(
            buy_put_or_call,
            client,
            current_date,
            current_expiry,
            BANKNIFTY_SYMBOL,
            CALL_ORDER_TYPE,
        ),
        "4": partial(
            buy_put_or_call,
            client,
            current_date,
            current_expiry,
            BANKNIFTY_SYMBOL,
            PUT_ORDER_TYPE,
        ),
        "5": partial(display_all_positions, client),
        "6": partial(sell_all_positions, client),
        "7": partial(
            print,
            f"\nYour available margin balance is INR: {float(get_client_margin(client)) + float(10000)}\n",
        ),
        "8": partial(exit_program),
    }

    while True and EXIT_SCRIPT != True:
        start = time.process_time()

        print("Options Menu")
        print("1. BUY NIFTY50 CALL")
        print("2. BUY NIFTY50 PUT")
        print("3. BUY BANKNIFTY CALL")
        print("4. BUY BANKNIFTY PUT")
        print("5. DISPLAY ALL POSITIONS")
        print("6. SELL ALL POSITIONS")
        print("7. DISPLAY AVAILABLE MARGIN")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")
        print("\n")
        if choice in options_dict:
            start = time.process_time()
            options_dict[choice]()
            print(
                f"\nTime taken to execute choice:{choice} - {round(time.process_time() - start,10)} seconds.\n"
            )
        else:
            print("Invalid choice. Please enter a choice between 1-8.")


if __name__ == "__main__":
    main()
