import json
import re

with open("c:/Users/Yasir/Pictures/world-of-comfort/mkteapper/sections/header-group.json", "r", encoding="utf-8") as f:
    content = f.read()

# Remove comments at the top
match = re.search(r'\{', content)
if match:
    content = content[match.start():]

data = json.loads(content)

# Extract blocks from topbar
topbar = data["sections"].get("topbar_3YD96h")
if topbar:
    trust_bar = data["sections"]["trust_bar_AHMrnh"]
    
    # We will copy link_list, text, and language_country blocks
    new_blocks = {}
    new_block_order = list(trust_bar["block_order"]) # Existing USPs
    
    for block_id, block_data in topbar.get("blocks", {}).items():
        if block_data["type"] in ["link_list", "text", "language_country"]:
            # Clean up topbar specific settings that we don't need
            if block_data["type"] == "text":
                block_data["settings"] = { "text": block_data["settings"].get("text", "") }
            elif block_data["type"] == "link_list":
                block_data["settings"] = { "menu": block_data["settings"].get("menu", "main-menu") }
            elif block_data["type"] == "language_country":
                block_data["settings"] = { 
                    "show_language_selector": block_data["settings"].get("show_language_selector", False),
                    "show_country_selector": block_data["settings"].get("show_country_selector", True)
                }
            
            trust_bar["blocks"][block_id] = block_data
            new_block_order.append(block_id)
            
    # Also add the link_list at the beginning, language_country at the end, texts in middle
    link_lists = [bid for bid in new_block_order if trust_bar["blocks"][bid]["type"] == "link_list"]
    usps_and_texts = [bid for bid in new_block_order if trust_bar["blocks"][bid]["type"] in ["usp", "text"]]
    language_countries = [bid for bid in new_block_order if trust_bar["blocks"][bid]["type"] == "language_country"]
    
    trust_bar["block_order"] = link_lists + usps_and_texts + language_countries
    
    # Remove topbar from sections
    del data["sections"]["topbar_3YD96h"]
    
    # Remove from order
    if "topbar_3YD96h" in data["order"]:
        data["order"].remove("topbar_3YD96h")
        
    with open("c:/Users/Yasir/Pictures/world-of-comfort/mkteapper/sections/header-group.json", "w", encoding="utf-8") as f:
        # Re-add the comments
        f.write("/*\n * ------------------------------------------------------------\n * IMPORTANT: The contents of this file are auto-generated.\n *\n * This file may be updated by the Shopify admin theme editor\n * or related systems. Please exercise caution as any changes\n * made to this file may be overwritten.\n * ------------------------------------------------------------\n */\n")
        json.dump(data, f, indent=2, ensure_ascii=False)
        print("Updated header-group.json")
else:
    print("Topbar not found.")
