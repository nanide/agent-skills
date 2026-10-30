---
name: make-bot-ui
description: Build a custom UI for an explicitly configured bot service, or assess whether host scheduling can meet a requested bot workflow.
---

# Build a bot UI

Start by identifying the user action, payload, backend, and expected result. The data shape is a small validated JSON request and a response that distinguishes accepted work from completed work.

## Check the execution service

Read the active [provider adapter](../../providers/README.md) and inspect the available scheduling tools. A scheduler does not imply a webhook receiver, secret manager, or event-triggered wake API. Do not invent endpoints or claim unsupported capabilities.

If scheduled work meets the user’s request, use supported scheduling only when the user requests it. Inspect existing schedules before creating a duplicate. Preserve notification preferences. Report unavailable scheduling and continue independently useful authorized work.

If a button must invoke a bot immediately, require a separately configured service with a documented endpoint and authentication contract. Read that service's documentation and use its real API. If none is available, build any independently useful local UI and payload validation within scope, and report the missing backend. Do not pretend a mock response proves delivery.

## Keep credentials on the server

Use the host's supported secret manager or environment configuration. Never request a key in chat, embed it in browser JavaScript, print it, or commit it. If a secret-entry tool is unavailable, explain the required local configuration without asking for the value.

Have the browser call a local server. That server validates allowed actions, authenticates requests as needed, and calls only the configured backend. Use the documented headers, timeout, and retry semantics. Do not copy service-specific authentication headers from another provider. Add idempotency when retries could duplicate work.

## Verify the UI and service

Use available browser or computer tools and applicable repository checks. Verify a harmless action through the actual backend before calling the integration live. Distinguish transport acceptance from task completion. Show useful failure state when the backend is unavailable. Keep logs free of credentials and sensitive payloads.

## Expose it only as requested

Bind to localhost by default. External exposure, a tunnel, or Tailscale setup must match the user's requested scope. Reuse existing infrastructure and inspect its configuration before changing it. Do not install services, authenticate a device, or change network exposure merely because the UI exists.

When remote access is authorized, follow current platform documentation, use verified addresses, and test the intended route. Report the actual URL and any unresolved access limitations.
