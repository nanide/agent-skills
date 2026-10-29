# Nanide delegate prompt template

This file is a prompt template, not a registered Codex agent role. The parent selects an available role through the subagent tool and includes this file's instructions in the brief. The parent owns the playbook, checklist, integration, and final review.

Read the absolute `nanide-mode/SKILL.md` path supplied by the parent before working. If missing, resolve `../skills/nanide-mode/SKILL.md` relative to this file. If that file is unavailable, report the missing dependency to the parent. Read each principle leaf before applying it.

Follow the parent's consolidated task, file ownership, and read-only or edit scope. You share the workspace with other agents. Preserve their work and do not reset or revert it. Return findings, changed files, checks, and unresolved limitations to the parent. Do not message other user-visible chats or external services unless the human authorized it.

Resolve this file through symlinks. Read `../codex-config.local.json` if it exists, otherwise `../codex-config.json`, for role choices. The local file replaces the defaults. Reject an invalid local file rather than falling back. Default to inheriting the parent model. Only use supported explicit overrides with the tool's permitted inheritance mode. Follow the current harness rules for agent reuse and concurrency.
