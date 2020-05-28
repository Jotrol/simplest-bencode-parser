def BDecode(data: bytes):
    offset = 0      # global iterator for data
    def parseInt():
        nonlocal offset
        offset += 1
        end_pos = data.find(b'e', offset)
        integer = int(data[offset : end_pos])
        offset = end_pos + 1
        return integer
    def parseString():
        nonlocal offset
        end_len = data.find(b':', offset)
        str_len = int(data[offset : end_len])
        end_pos = end_len + str_len + 1
        string = data[end_len + 1 : end_pos]
        offset = end_pos
        return string
    def parseList():
        nonlocal offset
        offset += 1
        values = []
        while offset < len(data):
            if data[offset] == ord("e"):
                offset += 1
                return values
            else:
                values.append(parse())
        raise ValueError("Unexpected EOF, expected list contents")
    def parseDict():
        nonlocal offset
        offset += 1
        values = {}
        while offset < len(data):
            if data[offset] == ord('e'):
                offset += 1
                return values
            else:
                key, val = parse(), parse()
                values[key] = val
        raise ValueError("Unexpected EOF, expected dict contents")
    def parse():
        nonlocal offset
        if data[offset] == ord('i'):
            return parseInt()
        elif data[offset] == ord('l'):
            return parseList()
        elif data[offset] == ord('d'):
            return parseDict()
        elif data[offset] in b'123456789':
            return parseString()
        raise ValueError(f'Unknown type specifiers: "{chr(data[offset])}"')
    result = parse()
    if offset != len(data):
        raise ValueError(f"Expected EOF, got {len(data) - offset} bytes left")
    return result
def BEncode(data):
    result = b''
    if isinstance(data, str):
        result += str(len(data)).encode() + b':' + data.encode()
    elif isinstance(data, bytes):
        result += str(len(data)).encode() + b':' + data
    elif isinstance(data, int):
        result += b'i' + str(data).encode() + b'e'
    elif isinstance(data, list):
        result += b'l'
        for val in data:
            result += BEncode(val)
        result += b'e'
    elif isinstance(data, dict):
        result += b'd'
        for key in sorted(data.keys()):
            result += BEncode(key)
            result += BEncode(data[key])
        result += b'e'
    else:
        raise ValueError("bencode only supports bytes, int, list and dict")
    return result
def tests():
    encode_test_int = 123
    encode_test_str = "Hello World!"
    print(BEncode(encode_test_int))    # integer test
    print(BEncode(encode_test_str))    # string test

    encode_test_list1 = [123, 123]
    encode_test_list2 = [123, 'Hello World!', 767867, 8787, -773, 'hello']
    encode_test_list3 = [123, ["Hello World!"]]
    print(BEncode(encode_test_list1))  # simple list test
    print(BEncode(encode_test_list2))  # different types list test
    print(BEncode(encode_test_list3))  # list in the list test

    encode_test_dict1 = {1 : "Hello World!"}
    encode_test_dict2 = {1 : "Hello World!", 2 : "hello"}
    encode_test_dict3 = {1 : ["Hello World!", 1234, "hello", 12], 2 : ["Hello World!", 1234] }
    encode_test_dict4 = {1 : ["Hello World!", [1234, ["hello", 123]]], 2 : ["Hello World", 1234]}
    encode_test_dict5 = {1 : {2 : ["Hello World!", [1234, ["hello", 123]]], 3 : 123}, 4 : [1, [2, [3, 4]]]}
    print(BEncode(encode_test_dict1))  # simple dict test
    print(BEncode(encode_test_dict2))  # two-keys dict test
    print(BEncode(encode_test_dict3))  # dict with lists   
    print(BEncode(encode_test_dict4))  # dict with lists in lists
    print(BEncode(encode_test_dict5))  # pretty complicated dict

    decode_test_int = b'i123e'
    decode_test_str = b'12:Hello World!'
    print(BDecode(decode_test_int))     # integer test
    print(BDecode(decode_test_str))     # string test

    decode_test_list1 = b'li123ei123ee'
    decode_test_list2 = b'li123e12:Hello World!i767867ei8787ei-773e5:helloe'
    decode_test_list3 = b'li123el12:Hello World!ee'
    print(BDecode(decode_test_list1))   # simple list test
    print(BDecode(decode_test_list2))   # different types list test
    print(BDecode(decode_test_list3))   # list in the list test

    decode_test_dict1 = b'di1e12:Hello World!e'
    decode_test_dict2 = b'di1e12:Hello World!i2e5:helloe'
    decode_test_dict3 = b'di1el12:Hello World!i1234e5:helloi12eei2el12:Hello World!i1234eee'
    decode_test_dict4 = b'di1el12:Hello World!li1234el5:helloi123eeeei2el11:Hello Worldi1234eee'
    decode_test_dict5 = b'di1edi2el12:Hello World!li1234el5:helloi123eeeei3ei123eei4eli1eli2eli3ei4eeeee'
    print(BDecode(decode_test_dict1))   # simple dict test
    print(BDecode(decode_test_dict2))   # two-keys dict test
    print(BDecode(decode_test_dict3))   # dict with lists
    print(BDecode(decode_test_dict4))   # dict with lists in lists
    print(BDecode(decode_test_dict5))   # pretty complicated dict

if __name__ == '__main__':
    tests()
    