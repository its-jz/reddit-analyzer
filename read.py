import streamlit as st
from pathlib import Path
import json
st.title('Reddit Analyzer Visualizer')

st.text("If you have a log file, you can view it here. If not, run `app.py` to generate one.")

# Single select dropdown
log_path = st.selectbox(
    "Which log would you like to read?",
    [str(p) for p in Path("runs").rglob("*.log")],
    )

with open(log_path, "r") as f:
    log_contents = f.read()

data = [json.loads(line) for line in log_contents.split("\n") if line]

tags = {} # tag -> set[entry.fullname]
for entry in data:
    for label in entry["labels"]:
        if label not in tags:
            tags[label] = set()
        tags[label].add(entry["fullname"])
# display the tags in descending order of frequency
sorted_tags = sorted(tags.items(), key=lambda x: len(x[1]), reverse=True)
st.header("Trends:")
for tag, entries in sorted_tags:
    st.write(f"Tag: {tag}, Count: {len(entries)}")
        

st.header("Log contents:")
    
# write each line in a separate block
for line in log_contents.split("\n"):
    st.json(json.loads(line))
    st.divider()