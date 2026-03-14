
# Sonic Deployment Model

Sonic works through a manifest driven model.

Step 1 — profile selection  
Step 2 — manifest generation  
Step 3 — verification  
Step 4 — staging  
Step 5 — apply  

Example flow:

profile
  ↓
sonic plan
  ↓
manifest.json
  ↓
verify
  ↓
stage payloads
  ↓
deploy to device
