with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    lines = f.readlines()

open_braces = 0
close_braces = 0
open_brackets = 0
close_brackets = 0

stack = []

for line_no, line in enumerate(lines, 1):
    # Remove strings and comments
    clean_line = ""
    in_str = False
    for ch in line:
        if ch == '"':
            in_str = not in_str
        elif not in_str:
            if ch == '#':
                break
            clean_line += ch
    
    for ch in clean_line:
        if ch == '{':
            open_braces += 1
            stack.append(('{', line_no))
        elif ch == '}':
            close_braces += 1
            if stack and stack[-1][0] == '{':
                stack.pop()
            else:
                print(f"Mismatched '}}' at line {line_no}")
        elif ch == '[':
            open_brackets += 1
            stack.append(('[', line_no))
        elif ch == ']':
            close_brackets += 1
            if stack and stack[-1][0] == '[':
                stack.pop()
            else:
                print(f"Mismatched ']' at line {line_no}")

print(f"Total lines: {len(lines)}")
print(f"Open braces {{: {open_braces}, Close braces }}: {close_braces}, Diff: {open_braces - close_braces}")
print(f"Open brackets [: {open_brackets}, Close brackets ]: {close_brackets}, Diff: {open_brackets - close_brackets}")

if stack:
    print(f"Unclosed items count: {len(stack)}")
    for item in stack[-10:]:
        print(f"Unclosed {item[0]} opened at line {item[1]}: {lines[item[1]-1].strip()}")
