# Outlook test setup (template)

Account, tenant, and flow identifiers are intentionally not stored in this repository. Record them in your own notes, not here.

## What was proven

A manually triggered Power Automate flow (**Manually trigger a flow → Office 365 Outlook: Send an email (V2)**) sent a test message to a controlled recipient. Run history showed success and the message appeared in the Inbox. This verified sending and receipt only. No scheduled campaign, lead source, follow-up action, or reply-stop logic was configured or verified.

## Reuse boundary

A past successful test does not authorize another send. For a future test, use the recipient and purpose in the current request, inspect the saved flow first (its recipients and actions may have changed), and use a unique subject marker so an earlier message cannot be mistaken for new delivery.
