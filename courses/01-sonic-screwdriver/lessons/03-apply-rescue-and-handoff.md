# Lesson 03 - Apply, Rescue, And Handoff

Once a plan is reviewed, Sonic can apply it on Linux.

That execution lane should still stay explicit:

- `bash scripts/sonic-stick.sh --manifest ...`
- `bash scripts/smoke/linux-runtime-smoke.sh`

Sonic also carries a rescue mindset:

- collect evidence first
- verify layout and logs
- recover before rewriting blindly

Useful rescue surfaces include:

- `scripts/collect-logs.sh`
- `scripts/verify-usb-layout.sh`
- `modules/rescue/`

After deployment, Sonic hands control to the correct owning system:

- `uDOS` for shared family integration and Wizard-facing coordination
- `uHOME-server` for canonical `uHOME` runtime behavior
