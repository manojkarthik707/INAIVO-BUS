import os

wbt_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(wbt_path, "r", encoding="utf-8") as f:
    text = f.read()

# List of PROTO nodes to remove (the misplaced signs and obstacle lights)
targets = [
    "GenericTrafficLight",
    "CrossRoadsTrafficLight",
    "CautionSign",
    "OrderSign",
    "StopSign",
    "YieldSign",
    "SpeedLimitSign"
]

def remove_nodes(content, target_names):
    result = []
    i = 0
    n = len(content)
    
    while i < n:
        # Check if any target node starts at or near i
        matched = False
        for name in target_names:
            # Check for "DEF xyz Name {" or "Name {"
            pattern_start = None
            if content[i:].startswith(name + " ") or content[i:].startswith(name + "\n") or content[i:].startswith(name + "{"):
                pattern_start = i
            elif content[i:].startswith("DEF "):
                # check if next token after DEF is name
                rest = content[i:]
                parts = rest.split(None, 3)
                if len(parts) >= 3 and parts[2] == name:
                    pattern_start = i
            
            if pattern_start is not None:
                # Find opening brace
                open_brace = content.find("{", pattern_start)
                if open_brace != -1:
                    # Count matching braces
                    depth = 1
                    j = open_brace + 1
                    while j < n and depth > 0:
                        if content[j] == '{':
                            depth += 1
                        elif content[j] == '}':
                            depth -= 1
                        j += 1
                    
                    if depth == 0:
                        # Skip this whole node
                        i = j
                        matched = True
                        break
        
        if not matched:
            result.append(content[i])
            i += 1
            
    return "".join(result)

cleaned = remove_nodes(text, targets)

# Clean excessive blank lines
import re
cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

with open(wbt_path, "w", encoding="utf-8") as f:
    f.write(cleaned)

print("Cleaned sih_mvp_traffic.wbt with perfect bracket matching!")
