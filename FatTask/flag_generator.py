import random
import struct
def hex_uses_codes():
    yield "00"
    for x in [range(48, 58), range(65, 91), range(97, 123), (95,)]:
        for j in x:
            yield hex(j)[2:]

def generate_address_space():
    for first_position in hex_uses_codes():
        for second_position in hex_uses_codes():
            value  = first_position + second_position
            if value != "0000":
                yield value

def  possible_address(symbol):
    symbol = hex(ord(symbol))[2:]
    return "00"+ symbol, symbol + "00"

def generate_unique_flag(length = 32, prefix = "RUCTF2017_"):
    address_space = { address : False for address in generate_address_space()}
    addresses_list = []
    value_seted = False
    value_acum = ""
    for symbol in prefix:
        if not value_acum:
            for address in possible_address(symbol):
                if not address_space[address]:
                    addresses_list.append(address)
                    address_space[address] = True
                    value_seted = True
                    break
            if not value_seted:
                value_acum += symbol
            else:
                value_seted = False
        else:
            address = hex(ord(value_acum))[2:] + hex(ord(symbol))[2:]
            if not address_space[address]:
                addresses_list.append(address)
                address_space[address] = True
                value_acum = ""
            else:
                raise  AttributeError("Bad Prefix Selected")
    free_addresses = []
    for key in address_space.keys():
        if not address_space[key]:
            free_addresses.append(key)
    postfix = generate_unique_flag_postfix(where = free_addresses ,length = length - len(prefix))
    final_addresses = addresses_list + postfix
    return final_addresses

def decode_flag_from_addresses_list(addresses_list):
    flag_symbols = []
    for address in addresses_list:
        first_part  = int(address[0:2], 16)
        second_part = int(address[2:], 16)
        if first_part != 0:
            flag_symbols.append(chr(first_part))
        if second_part !=0:
            flag_symbols.append(chr(second_part))
    return "".join(flag_symbols)

def encode_to_cluster_numbers(addresses):
    for x in addresses:
        yield int(x, 16)

def generate_unique_flag_postfix(where = None, length = 32):
    if where is None:
        where = [x for x in generate_address_space()]
    return random.sample(where, length)

addresses = generate_unique_flag()
flag = decode_flag_from_addresses_list(addresses)
