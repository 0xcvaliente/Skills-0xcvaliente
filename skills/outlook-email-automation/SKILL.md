---
name: outlook-email-automation
description: Set up, inspect, and browser-test Outlook email automation with Power Automate, including low-cost tool selection and sales follow-up workflows. Use when the user wants Outlook sending or follow-up automation configured or verified. Needs a browser-automation capability; honors the user's preferred browser (this user prefers Helium).
---

# Outlook Email Automation

Turn the requested Outlook workflow into a saved automation and verify the behavior actually requested. The proven baseline is a manual Power Automate flow with the standard Office 365 Outlook connector. A successful send test establishes sending and delivery; it does not establish prospecting, scheduled follow-ups, or reply suppression.

Read [references/tested-setup.md](references/tested-setup.md) when working with this user's existing account or test flow. Inspect that flow before creating a duplicate. Treat the saved account, recipient, and run result as historical context, not continuing authorization for email sends or mailbox access.

## Choose the service and browser

- Preserve an explicitly chosen service. If none is specified, consider Power Automate for a Microsoft 365 work account before adding another subscription. Confirm the account's entitlement; a signed-in Power Automate session alone does not prove free use.
- If recommending Make or another service, verify current official prices, monthly versus annual billing, credit limits, and connector availability. A Make walkthrough requires its own session; Power Automate success does not verify Make.
- For this user's browser execution, prefer Helium and honor any newer browser choice. Use whatever browser-automation capability the host session actually has (for example a browser extension, a Playwright or computer-use MCP server, or a built-in browser pane) and its documented methods; do not assume one exists. If none is available, give the user the exact steps and say the flow is unverified. Helium is Chromium-based, but check that the available tool can actually drive it; if it can only drive a different browser, say so and ask before switching. On this Mac, Helium's bundle ID is `net.imput.helium`.
- Inspect the current browser tabs and signed-in account. Reuse the relevant Outlook and Power Automate tabs. Read the updated UI after actions and derive fresh element references (accessibility indices or refs) from the current page; saved references are not selectors.

## Build or reuse the manual send test

Use the current user-specified recipient. If none is available or authorized for this test, ask for an address the user controls before sending. Keep the test flow manually triggered and its recipients confined to the requested test.

For a new flow, the verified UI path is:

1. **My flows → New flow → Instant cloud flow—from blank**.
2. Name it **Outlook automation test - manual only**, select **Manually trigger a flow**, and choose **Create**.
3. Insert **Office 365 Outlook → Send an email (V2)**. Use Office 365 Outlook for a Microsoft 365 work mailbox; distinguish it from the separate Outlook.com connector.
4. Reuse the appropriate connection, or have the user sign in with the matching work account (do not type their password). Inspect new consent prompts and follow the current tool's requirements before granting additional mailbox access.
5. Set **To**, a distinctive subject containing the current date and a unique run marker, and a brief body identifying it as the user's requested automation test. Verify the resolved recipient chip and text before saving.
6. **Save → Test → Manually → Test → Continue → Run flow**. Interface labels may change; follow the observed UI rather than assuming this exact layout.

For the saved flow, inspect the trigger, connection, recipients, and actions first. Reuse it if it still matches the request. Update its test subject and body for the new run; do not silently replace a production workflow with a test.

## Verify the result

If the optional `valiente` MCP server is connected, check delivery and replies with its Outlook tools instead of the browser; see [Valiente MCP](references/valiente-mcp.md).

**Run successfully started** is an intermediate result. Open run history and check the final status. Then search Outlook using `subject:"the exact unique test subject"`, open the matching message, and confirm its recipient, body, time, and Inbox location. Searching all folders can also find the Sent Items copy, so that copy alone does not prove receipt.

If the run result is ambiguous, inspect run history and Outlook before retrying to avoid duplicate sends. Report a concrete error or blocker if verification cannot finish. Leave the manual test available and report the saved flow link, the observed result, and any requested features still unverified.

## Extend to sales follow-ups when requested

Define the recipient source, message copy, delay, maximum follow-ups, and stop conditions before enabling a campaign. Use a durable contact record with recipient, status, next-send time, last-send time, and message or conversation identifiers. Check due time and stop status immediately before each send, and select due records before imposing a batch limit.

Match replies to the contact and relevant thread, and distinguish outgoing messages, automatic replies, and genuine responses. A test sent to the sender's own mailbox can falsely look like a reply when detection checks only the sender address. Use a suitable owned test mailbox or clearly report that reply detection remains unverified.

Account for partial failures: sending can succeed while updating the contact record fails. Inspect delivery and reconcile state before retrying. Test only the requested branches using authorized test recipients; configure schedules and prospect sends only within the user's current requested scope.

## Official references

- [Power Automate licensing FAQs](https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/faqs): check Microsoft 365 entitlement and standard versus premium connectors.
- [Office 365 Outlook connector](https://learn.microsoft.com/en-us/connectors/office365/): check supported actions and connector limitations.
- [Power Automate pricing](https://www.microsoft.com/en-us/power-platform/products/power-automate/pricing) and [Make pricing](https://www.make.com/en/pricing): verify live prices when cost is part of the request.
