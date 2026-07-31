import pdfplumber
import re
import json

# Final list jismein saara parsed data dictionary format mein store hoga
final_data = []

# Context manager use karke PDF file open karna
with pdfplumber.open("data/ee_sem5.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += "\n" + page_text

    # 1. Poore text ko Subject Blocks mein split karna
    subject_pattern = r"(?=Name of the course)"
    subject_blocks = re.split(subject_pattern, full_text, flags=re.IGNORECASE)
    subject_blocks = [block.strip() for block in subject_blocks if block.strip()]

    print(f"Total blocks found: {len(subject_blocks)}")

    # Main patterns jo loop ke andar use honge
    name_pattern = r"Name of the course\s*[:|-]?\s*([^\n]+)"
    unit_split_pattern = r"(?<=\n)(?=\d+\s[A-Z])"
    
    # Primary Pattern: Ismein colon (:) hona compulsory hai title filter karne ke liye
    unit_parse_pattern = r"(\d+)\s+(.*?):\s*(.*)"
    
    # Fallback Pattern: Agar colon nahi mila, toh number ke baad ka sab kuch content hoga
    fallback_parse_pattern = r"(\d+)\s+(.*)"

    # 2. Har subject block par loop chalana
    for block in subject_blocks:
        # Step A: Intro/invalid block filter
        if "name of the course" not in block.lower():
            print("Skipping intro/invalid block...")
            continue
            
        # Step B: Subject ka naam extract karna
        name_match = re.search(name_pattern, block, flags=re.IGNORECASE)
        if name_match:
            subject_name = name_match.group(1).strip()
            print(f"Processing Subject: {subject_name}")
        else:
            subject_name = "Unknown Subject"
            print("Warning: Subject name pattern not matched, using default.")

        # Step C: Is specific subject block ke andar units ko split karna
        unit_chunks = re.split(unit_split_pattern, block)
        
        subject_units = []  # Is subject ki saari units yahan save hongi

        # Step D: Har unit-chunk se serial_no, title, aur content nikaalna
        for idx, chunk in enumerate(unit_chunks):
            chunk = chunk.strip()
            if not chunk:
                continue
                
            # 🚀 Sabse simple tareeka: Pehla element (Index 0) metadata hai, ise skip karo
            if idx == 0:
                continue
                
            # Sabse pehle Primary Pattern (Colon waala) try karo
            unit_match = re.match(unit_parse_pattern, chunk, flags=re.DOTALL)
            
            if unit_match:
                serial_no = unit_match.group(1).strip()
                title = unit_match.group(2).strip()
                content = unit_match.group(3).strip()
                
                unit_data = {
                    "unit_no": serial_no,
                    "title": title,
                    "content": content
                }
                subject_units.append(unit_data)
                
            else:
                # Fallback Logic: Agar colon nahi mila, toh doosra pattern try karo
                fallback_match = re.match(fallback_parse_pattern, chunk, flags=re.DOTALL)
                
                if fallback_match:
                    serial_no = fallback_match.group(1).strip()
                    # Colon nahi hai, isliye title ko khaali ya None rakhenge
                    title = "" 
                    content = fallback_match.group(2).strip()
                    
                    print(f"  ℹ️ Fallback triggered for Unit {serial_no} (No colon found)")
                    
                    unit_data = {
                        "unit_no": serial_no,
                        "title": title,
                        "content": content
                    }
                    subject_units.append(unit_data)
                else:
                    # Agar dono mein se koi bhi match nahi hua (Very rare edge case)
                    print(f"  ⚠️ Could not parse chunk at all in '{subject_name}': {chunk[:60]}...")

        # Step E: Subject level par dictionary banana aur final_data list mein append karna
        subject_dict = {
            "subject_name": subject_name,
            "units": subject_units
        }
        final_data.append(subject_dict)

# 3. End mein, final_data ko JSON file mein save karna
output_file = "data/parsed_ee_sem5.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(final_data, json_file, indent=4, ensure_ascii=False)

print(f"\n Success! Data cleanly saved to '{output_file}'")
