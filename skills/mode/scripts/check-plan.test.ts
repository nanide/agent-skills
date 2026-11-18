import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { expect, test } from "bun:test";

const checker = join(import.meta.dir, "check-plan.mjs");
const rule =
	"Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.";

const validPlan = `# Demo

## How to read this
One box is one unit of work and names the evidence. Check a box only when its evidence exists. See playbooks/.
${rule}

## Program checklist
### Arm the program
### Spawn owners
### PR mechanics
### Verdict and merge
### Boot recipe
\`installed skill paths\` host schedule status message

## PR 1
**Depends on.** None.
**Files.**
- [ ] Do the thing.
**Build.**
- [ ] Do the thing.
**You see.**
- [ ] Do the thing.
**Verify, unit.** ${rule}
- [ ] Check the thing.
**Verify, live.** ${rule} Ten coverage lanes on \`example-model\` at the PR head
${Array.from({ length: 10 }, (_, i) => `- [ ] Lane ${i + 1}. Save \`lane-${i + 1}.png\`. Pass when evidence exists.`).join("\n")}
**Verify, perf.** ${rule}
- [ ] Metric. Recorded.
- [ ] Probe. Recorded.
- [ ] Baseline. Recorded.
- [ ] Rule. Recorded.
**Review gate.** None.
**Merge.**
- [ ] Merge when approved.

## Close the program
Close.

## Appendix Prototype evidence
Recorded.
`;

const runDocument = (document: string, expectedExit: number) => {
	const directory = mkdtempSync(join(tmpdir(), "check-plan-test-"));
	const file = join(directory, "plan.md");
	writeFileSync(file, document);
	try {
		const result = spawnSync("node", [checker, file], { encoding: "utf8" });
		expect(result.status).toBe(expectedExit);
		return result;
	} finally {
		rmSync(directory, { recursive: true, force: true });
	}
};

const runPlan = (appendix: string, expectedExit: number) => runDocument(validPlan + appendix, expectedExit);

test("accepts ordinary, indented, and longer closing fences", () => {
	for (const indent of ["", " ", "  ", "   "])
		runPlan(`${indent}\`\`\`markdown\n## Example only\n${indent}\`\`\`\n`, 0);
	runPlan("```markdown\n## Example only\n````\n", 0);
});

test("accepts nested backticks and tilde info strings", () => {
	runPlan("````markdown\n```markdown\n## Example only\n```\n````\n", 0);
	runPlan("~~~markdown `info`\n## Example only\n ~~~\n", 0);
});

test("keeps mismatched, shorter, and suffixed closers inside the fence", () => {
	runPlan("````markdown\n~~~\n## Example only\n````\n", 0);
	runPlan("````markdown\n```\n## Example only\n````\n", 0);
	runPlan("````markdown\n``` info\n## Example only\n````\n", 0);
});

test("rejects headings and prose outside a proper close", () => {
	for (const suffix of ["  ", "\t"]) {
		const heading = runPlan(`\`\`\`markdown\n## Example only\n\`\`\`${suffix}\n## Example only\n`, 1);
		expect(heading.stderr).toContain('"## Example only" after Close the program is not an appendix');
	}

	const prose = runPlan("```markdown\nThis prose has a mid-sentence colon: inside code\n```\nThis prose has a mid-sentence colon: bad.\n", 1);
	expect(prose.stderr).toContain("mid-sentence colon");
});

test("rejects backtick info strings containing a backtick", () => {
	const result = runPlan("```markdown `invalid`\n## Example only\n```\n", 1);
	expect(result.stderr).toContain('"## Example only" after Close the program is not an appendix');
});

test("ignores prose punctuation inside matching multi-backtick code spans", () => {
	for (const count of [2, 3, 4]) {
		const delimiter = "`".repeat(count);
		runPlan(`Use ${delimiter}echo \`x\`: “quoted” — example${delimiter}.\n`, 0);
	}
});

test("checks prose following a multi-backtick span and unmatched delimiters", () => {
	const outside = runPlan("Use ``echo `x`: y``. Bad: prose.\n", 1);
	expect(outside.stderr).toContain("mid-sentence colon");
	const unmatched = runPlan("Use ``unclosed: bad` here.\n", 1);
	expect(unmatched.stderr).toContain("mid-sentence colon");
});

const cliChange = `## LIST. List installed skills
- [ ] **Depends on.** None
- [ ] **Files.** \`src/list.ts\`
- [ ] **Build.** Add the list command.
- [ ] **Result.** An empty installation prints no names.
- [ ] **Unit.** Run the empty-list test.
- [ ] **Live.** Run list in an empty installation and capture empty stdout and exit 0.
- [ ] **Performance.** N/A. This CLI feature makes no timing claim.
- [ ] **Review.** N/A. It prints text without an interactive control.
`;
const concise = "# Skill listing\n\n" + cliChange;
const measured = `**Performance.**
  - Metric. Wall-clock time from launch to the last row.
  - Probe. Run the same listing against the same 200 installed skills.
  - Baseline. Interleave runs of trunk and head, beginning with trunk.
  - Limit. Fail when the median on head exceeds trunk by 10%.`;
const interactive = `**Review.** Have the operator select a skill and confirm its detail view opens.
  - Evidence. Save the interaction recording and resulting detail view.`;

test("accepts a complete CLI plan with terminal receipts", () => {
	expect(runDocument(concise, 0).stdout).toContain("1 PR sections, 0 problems");
});

test("checks every unit and requires dependencies in execution order", () => {
	const child = cliChange.replace("## LIST.", "## PICK.").replace("**Depends on.** None", "**Depends on.** LIST");
	expect(runDocument(concise + child, 0).stdout).toContain("2 PR sections, 0 problems");
	expect(runDocument(concise + cliChange, 1).stderr).toContain("duplicate change ID");
	expect(runDocument("# Skills\n" + child + cliChange, 1).stderr).toContain('dependency "LIST"');
	expect(runDocument(concise + child.replace("**Depends on.** LIST", "**Depends on.** MISSING"), 1).stderr)
		.toContain('dependency "MISSING"');
});

test("rejects missing results and verification procedures, including fenced examples", () => {
	for (const field of ["Result", "Unit", "Live"]) {
		const removed = concise.split("\n").filter((line) => !line.includes(`**${field}.**`)).join("\n");
		const padded = removed + "\n```markdown\n" + cliChange + "\n```\n";
		expect(runDocument(padded, 1).stderr).toContain(`supply ${field}`);
	}
});

test("requires reasons for inapplicable performance and interaction review", () => {
	for (const field of ["Performance", "Review"]) {
		const missing = concise.replace(new RegExp(`(\\*\\*${field}\\.\\*\\*)[^\\n]+`), "$1 N/A.");
		expect(runDocument(missing, 1).stderr).toContain(`explain why ${field}`);
	}
});

test("accepts a measured change and rejects a missing probe, baseline or numeric limit", () => {
	const plan = concise.replace(/\*\*Performance\.\*\*.*/, measured);
	runDocument(plan, 0);
	for (const field of ["Metric", "Probe", "Baseline", "Limit"]) {
		const invalid = plan.split("\n").filter((line) => !line.startsWith(`  - ${field}.`)).join("\n");
		expect(runDocument(invalid, 1).stderr).toContain(`performance ${field.toLowerCase()}`);
	}
	expect(runDocument(plan.replace("10%", "too much"), 1).stderr).toContain("numerical failure threshold");
});

test("requires both an interaction to review and its receipt", () => {
	const plan = concise.replace(/\*\*Review\.\*\*.*/, interactive);
	runDocument(plan, 0);
	expect(runDocument(plan.replace(/  - Evidence\..*/, ""), 1).stderr).toContain("interaction review evidence");
	expect(runDocument(plan.replace(/\*\*Review\.\*\*.*/, "**Review.**"), 1).stderr)
		.toContain("describe the interaction");
});

test("reports CLI usage and unreadable files", () => {
	expect(spawnSync("node", [checker]).status).toBe(2);
	expect(spawnSync("node", [checker, join(tmpdir(), "absent-plan-directory", "missing.md")]).status).toBe(1);
});

test("a skipped unit or live check cannot stand in for a procedure", () => {
	for (const field of ["Unit", "Live"]) {
		const missing = concise.replace(new RegExp(`(\\*\\*${field}\\.\\*\\*)[^\\n]+`), "$1 N/A. Another change covers this.");
		expect(runDocument(missing, 1).stderr).toContain(`supply ${field}`);
	}
});

test("ordinary review prose starting with None still needs evidence", () => {
	const plan = concise.replace(/\*\*Review\.\*\*.*/, "**Review.** None of the users can currently select an item.");
	expect(runDocument(plan, 1).stderr).toContain("interaction review evidence");
});

test("an empty field cannot borrow details from another heading", () => {
	for (const unrelated of ["**Notes.** Collected yesterday.", "### Background\nThe fixture is local."]) {
		const plan = concise.replace(/\*\*Live\.\*\*.*/, "**Live.**\n" + unrelated);
		expect(runDocument(plan, 1).stderr).toContain("supply Live");
	}
});

test("legacy verification needs an actionable procedure", () => {
	for (const placeholder of ["TBD.", "N/A."]) {
		const plan = validPlan.replace(/- \[ \] Lane 1\.[\s\S]*?(?=\*\*Verify, perf)/, `- [ ] ${placeholder}\n`);
		expect(runDocument(plan, 1).stderr).toContain("supply Live");
	}
});

test("legacy performance and interaction reviews retain their evidence requirements", () => {
	const missing = validPlan.replace(/- \[ \] Metric\.[\s\S]*?(?=\*\*Review gate)/, "- [ ] N/A.\n");
	expect(runDocument(missing, 1).stderr).toContain("supply the performance metric");
	expect(runDocument(validPlan.replace("**Review gate.** None.", "**Review gate.** TBD."), 1).stderr)
		.toContain("describe the operator review");
});

test("legacy headings cannot supply missing verification details", () => {
	const plan = validPlan.replace("- [ ] Check the thing.", "### Owner notes\nDiscussed yesterday.");
	expect(runDocument(plan, 1).stderr).toContain("supply Unit");
	runDocument(plan.replace("Discussed yesterday.", "Discussed yesterday.\n- [ ] Run the unit check."), 0);
});
