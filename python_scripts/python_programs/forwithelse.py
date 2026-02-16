# Essential gadgets needed for the conference
essential_gadgets = ["laptop", "charger", "adapter", "USB drive"]
packed_items = ["laptop", "USB drive", "notebooks", "pens"]


for gadget in essential_gadgets:
    found = False
    for packed in packed_items:
        if packed == gadget:
            # TODO: Found missing gadget, stop searching
            found = True
            break
    # TODO: Print missing gadget if there is one
    if not found:
        print("Missing gadget:", gadget)
    
    
    