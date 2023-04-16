"""
This script is designed to generate arguments required to buy/sell derivative in 5paisa trading platform. 
It uses argparse module to create a command-line interface and accept user inputs. 

The accepted arguments are:
    --client/-c: 5paisa client to use
    --order-type/-o: Order type, buy/sell
    --exchange/-e: Exchange to use
    --exchange-type/-t: Exchange Type
    --scrip-code/-s: 5paisa scrip code
    --quantity/-q: Quantity
    --inflated-option-price/-p: Option price

It then calls the function 'place_my_order' with the arguments passed, which places an order on the trading platform. 

Note: The script uses base64 and pickle module to serialize and deserialize the client object. 
This script is platform-specific and may require modifications to run on non-Linux systems. 

"""


import argparse
import base64
import pickle


def parse_my_args():
    """
    Parses command line arguments.

    Returns:
        Namespace: A namespace object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate arguments required to buy / sell derivative."
    )
    parser.add_argument("--client", "-c", help="5paisa client to use")
    parser.add_argument("--order-type", "-o", help="Order type, buy / sell")
    parser.add_argument("--exchange", "-e", help="Exchange to use")
    parser.add_argument("--exchange-type", "-t", help="Exchange Type")
    parser.add_argument("--scrip-code", "-s", help="5paisa scrip code")
    parser.add_argument(
        "--quantity",
        "-q",
        help="Quantity",
    )
    parser.add_argument("--inflated-option-price", "-p", help="Option price")
    return parser.parse_args()


def place_my_oder(
    client_int,
    order_type_int,
    exchange_int,
    exchange_type_int,
    scrip_code_int,
    quantity_int,
    inflated_option_price_int,
):
    """
    Places order using the 5paisa client object.

    Args:
        client_int (object): 5paisa client object
        order_type_int (str): Order type, buy / sell
        exchange_int (str): Exchange to use
        exchange_type_int (str): Exchange Type
        scrip_code_int (int): 5paisa scrip code
        quantity_int (float): Quantity
        inflated_option_price_int (float): Option price

    Returns:
        None
    """
    client_int.place_order(
        OrderType=order_type_int,
        Exchange=exchange_int,
        ExchangeType=exchange_type_int,
        ScripCode=scrip_code_int,
        Qty=quantity_int,
        Price=inflated_option_price_int,
    )


if __name__ == "__main__":
    args = parse_my_args()
    deserialized_client = pickle.loads(base64.b64decode(args.client))
    order_type = args.order_type
    exchange = args.exchange
    exchange_type = args.exchange_type
    scrip_code = args.scrip_code
    quantity = args.quantity
    inflated_option_price = args.inflated_option_price
    place_my_oder(
        deserialized_client,
        order_type,
        exchange,
        exchange_type,
        int(scrip_code),
        float(quantity),
        float(inflated_option_price),
    )
